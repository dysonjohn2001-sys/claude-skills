"""PostgreSQL access for the worker.

Deliberately hand-written SQL rather than an ORM: the queries here are few,
long-lived and performance-sensitive, and the job-claim query in particular
depends on `FOR UPDATE SKIP LOCKED` semantics an ORM would obscure.
"""

from __future__ import annotations

import json
import logging
from contextlib import contextmanager
from datetime import datetime
from typing import Any, Iterator

import psycopg
from psycopg.rows import dict_row

from phg.models import ClipCandidate, MediaAsset, Play, Player, Segment, SyncAnchor

log = logging.getLogger(__name__)


class Database:
    def __init__(self, dsn: str) -> None:
        if not dsn:
            raise ValueError("DATABASE_URL is not set")
        self.dsn = dsn

    @contextmanager
    def connect(self) -> Iterator[psycopg.Connection]:
        with psycopg.connect(self.dsn, row_factory=dict_row) as conn:
            yield conn

    # -- job queue --------------------------------------------------------

    def claim_job(self, worker_name: str) -> dict[str, Any] | None:
        """Atomically take the next queued job. Safe to run on many workers."""
        sql = """
        WITH next AS (
          SELECT id FROM jobs
           WHERE status = 'queued' AND run_after <= now()
           ORDER BY created_at
           FOR UPDATE SKIP LOCKED
           LIMIT 1
        )
        UPDATE jobs j
           SET status = 'running', locked_by = %s, locked_at = now(),
               started_at = COALESCE(j.started_at, now()), attempts = j.attempts + 1
          FROM next
         WHERE j.id = next.id
        RETURNING j.*;
        """
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (worker_name,))
            return cur.fetchone()

    def finish_job(self, job_id: str, *, status: str, error: str | None = None) -> None:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                """UPDATE jobs
                      SET status = %s, error = %s, finished_at = now(),
                          progress = CASE WHEN %s = 'succeeded' THEN 100 ELSE progress END,
                          locked_by = NULL, locked_at = NULL
                    WHERE id = %s""",
                (status, error, status, job_id),
            )

    def retry_or_fail(self, job: dict[str, Any], error: str) -> None:
        """Requeue with backoff while attempts remain, otherwise fail."""
        if job["attempts"] < job["max_attempts"]:
            delay = 30 * (2 ** (job["attempts"] - 1))
            with self.connect() as conn, conn.cursor() as cur:
                cur.execute(
                    """UPDATE jobs
                          SET status = 'queued', error = %s, locked_by = NULL, locked_at = NULL,
                              run_after = now() + make_interval(secs => %s)
                        WHERE id = %s""",
                    (error, delay, job["id"]),
                )
            log.warning("job %s requeued in %ss: %s", job["id"], delay, error)
        else:
            self.finish_job(job["id"], status="failed", error=error)

    def enqueue(self, job_type: str, target_type: str, target_id: str, payload: dict | None = None) -> str:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                """INSERT INTO jobs (job_type, target_type, target_id, payload)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                (job_type, target_type, target_id, json.dumps(payload or {})),
            )
            return str(cur.fetchone()["id"])

    def set_progress(self, job_id: str, progress: float, note: str | None = None) -> None:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                """UPDATE jobs
                      SET progress = %s,
                          log = log || %s::jsonb
                    WHERE id = %s""",
                (progress, json.dumps([{"at": datetime.utcnow().isoformat(), "note": note}] if note else []), job_id),
            )

    # -- reads ------------------------------------------------------------

    def load_players(self, game_id: str) -> list[Player]:
        """Roster for a game, with that game's batting order and substitutions."""
        sql = """
        SELECT p.id, p.first_name, p.last_name, p.preferred_name, p.jersey_number,
               COALESCE(array_agg(DISTINCT pp.position) FILTER (WHERE pp.position IS NOT NULL), '{}') AS positions,
               le.batting_order,
               COALESCE(le.entered_inning, 1) AS entered_inning,
               le.exited_inning
          FROM games g
          JOIN seasons s        ON s.id = g.season_id
          JOIN players p        ON p.team_id = s.team_id AND p.is_active
     LEFT JOIN player_positions pp ON pp.player_id = p.id
     LEFT JOIN lineup_entries le   ON le.player_id = p.id AND le.game_id = g.id
         WHERE g.id = %s
      GROUP BY p.id, le.batting_order, le.entered_inning, le.exited_inning
        """
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(sql, (game_id,))
            return [
                Player(
                    id=str(r["id"]),
                    first_name=r["first_name"],
                    last_name=r["last_name"],
                    preferred_name=r["preferred_name"],
                    jersey_number=r["jersey_number"],
                    positions=tuple(r["positions"] or ()),
                    batting_order=r["batting_order"],
                    entered_inning=r["entered_inning"] or 1,
                    exited_inning=r["exited_inning"],
                )
                for r in cur.fetchall()
            ]

    def load_plays(self, game_id: str) -> list[Play]:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                """SELECT * FROM plays WHERE game_id = %s ORDER BY sequence_no""",
                (game_id,),
            )
            return [
                Play(
                    id=str(r["id"]),
                    game_id=str(r["game_id"]),
                    sequence_no=r["sequence_no"],
                    inning=r["inning"],
                    half=r["half"],
                    play_type=r["play_type"],
                    description=r["description"],
                    is_our_offense=r["is_our_offense"],
                    occurred_at=r["occurred_at"],
                    batter_name_raw=r["batter_name_raw"],
                    pitcher_name_raw=r["pitcher_name_raw"],
                    result=r["result"],
                    rbi=r["rbi"],
                    runs_scored=r["runs_scored"],
                    outs_before=r["outs_before"],
                    score_us=r["score_us"],
                    score_them=r["score_them"],
                    leverage_tag=r["leverage_tag"],
                    raw_row=r["raw_row"] or {},
                )
                for r in cur.fetchall()
            ]

    def load_media(self, game_id: str, media_root: str) -> list[MediaAsset]:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                """SELECT m.*,
                          COALESCE(json_agg(json_build_object(
                            'video_seconds', a.video_seconds,
                            'wall_clock_at', COALESCE(a.wall_clock_at, p.occurred_at)
                          ) ORDER BY a.video_seconds)
                          FILTER (WHERE a.id IS NOT NULL AND COALESCE(a.wall_clock_at, p.occurred_at) IS NOT NULL),
                          '[]') AS anchors
                     FROM media_assets m
                LEFT JOIN media_sync_anchors a ON a.media_asset_id = m.id
                LEFT JOIN plays p              ON p.id = a.play_id
                    WHERE m.game_id = %s AND m.status = 'ready'
                 GROUP BY m.id""",
                (game_id,),
            )
            assets = []
            for r in cur.fetchall():
                anchors = tuple(
                    SyncAnchor(
                        video_seconds=float(a["video_seconds"]),
                        wall_clock_at=datetime.fromisoformat(a["wall_clock_at"]),
                    )
                    for a in (r["anchors"] or [])
                )
                assets.append(
                    MediaAsset(
                        id=str(r["id"]),
                        game_id=str(r["game_id"]),
                        kind=r["kind"],
                        path=f"{media_root.rstrip('/')}/{r['storage_key']}",
                        duration_seconds=float(r["duration_seconds"] or 0),
                        fps=float(r["fps"] or 30),
                        width=r["width"] or 1920,
                        height=r["height"] or 1080,
                        has_audio=bool(r["has_audio"]),
                        recording_started_at=r["recording_started_at"],
                        anchors=anchors,
                    )
                )
            return assets

    def team_settings(self, game_id: str) -> dict[str, Any]:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                """SELECT t.id AS team_id, t.name AS team_name, t.primary_color,
                          t.secondary_color, t.logo_key, ts.*
                     FROM games g
                     JOIN seasons s ON s.id = g.season_id
                     JOIN teams t   ON t.id = s.team_id
                LEFT JOIN team_settings ts ON ts.team_id = t.id
                    WHERE g.id = %s""",
                (game_id,),
            )
            return cur.fetchone() or {}

    def players_with_consent(self, team_id: str) -> set[str]:
        """Only players whose guardians granted highlight generation get clips."""
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                """SELECT p.id
                     FROM players p
                     JOIN effective_consents ec ON ec.player_id = p.id
                    WHERE p.team_id = %s
                      AND ec.type = 'highlight_generation'
                      AND ec.is_active""",
                (team_id,),
            )
            return {str(r["id"]) for r in cur.fetchall()}

    # -- writes -----------------------------------------------------------

    def replace_clips_for_game(self, game_id: str, candidates: list[ClipCandidate],
                               auto_approve_threshold: float, review_floor: float) -> int:
        """Write a fresh set of clip candidates, preserving coach decisions.

        A clip a coach already approved or rejected is left alone. Re-running
        matching after fixing a roster typo must not silently undo review work.
        """
        inserted = 0
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                """DELETE FROM clips c
                    USING plays p
                    WHERE c.play_id = p.id
                      AND p.game_id = %s
                      AND c.review_status IN ('auto_approved','needs_review')""",
                (game_id,),
            )
            for c in candidates:
                if c.match_confidence < review_floor:
                    continue
                status = "auto_approved" if c.match_confidence >= auto_approve_threshold else "needs_review"
                cur.execute(
                    """INSERT INTO clips (
                         play_id, player_id, media_asset_id, category,
                         source_start_seconds, source_end_seconds,
                         pre_roll_seconds, post_roll_seconds,
                         match_method, match_confidence, confidence_factors,
                         review_status, rank_score, rank_factors, title)
                       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                       ON CONFLICT (play_id, player_id, category)
                         WHERE play_id IS NOT NULL
                       DO NOTHING""",
                    (
                        c.play_id, c.player_id, c.media_asset_id, c.category,
                        c.source_start_seconds, c.source_end_seconds,
                        c.pre_roll_seconds, c.post_roll_seconds,
                        c.match_method, c.match_confidence, json.dumps(c.confidence_factors),
                        status, c.rank_score, json.dumps(c.rank_factors), c.title,
                    ),
                )
                inserted += cur.rowcount
        return inserted

    def save_participant_resolutions(self, participants: list[Participant]) -> int:
        """Write resolved player ids back onto play_participants.

        The importer stores the raw name only, because resolving it needs the
        roster and the lineup, which matching has and importing does not. The
        derived statistics views join on player_id, so without this step every
        stat overlay and intro card comes out blank.
        """
        updated = 0
        with self.connect() as conn, conn.cursor() as cur:
            for p in participants:
                if p.player_id is None:
                    continue
                cur.execute(
                    """UPDATE play_participants
                          SET player_id = %s, resolve_confidence = %s, resolve_method = %s
                        WHERE play_id = %s AND role = %s::participant_role
                          AND (raw_name IS NOT DISTINCT FROM %s)
                          AND player_id IS DISTINCT FROM %s""",
                    (p.player_id, p.confidence, p.method, p.play_id, p.role,
                     p.raw_name, p.player_id),
                )
                updated += cur.rowcount
                if cur.rowcount == 0:
                    # The importer records a row per named participant, but a
                    # role inferred during matching (a runner pulled out of the
                    # narrative, say) may have no row yet.
                    cur.execute(
                        """INSERT INTO play_participants
                             (play_id, player_id, role, raw_name, resolve_confidence, resolve_method)
                           VALUES (%s, %s, %s::participant_role, %s, %s, %s)
                           ON CONFLICT (play_id, role, player_id) DO NOTHING""",
                        (p.play_id, p.player_id, p.role, p.raw_name, p.confidence, p.method),
                    )
                    updated += cur.rowcount
        return updated

    def save_segments(self, clip_id: str, segments: list[Segment]) -> None:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM clip_segments WHERE clip_id = %s", (clip_id,))
            for i, s in enumerate(segments):
                cur.execute(
                    """INSERT INTO clip_segments
                         (clip_id, position, start_seconds, end_seconds, keep, motion_score, reason)
                       VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (clip_id, i, s.start, s.end, s.keep, s.motion_score, s.reason),
                )

    def save_jersey_observations(self, media_asset_id: str, clip_id: str, observations) -> None:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM jersey_observations WHERE clip_id = %s", (clip_id,))
            for o in observations:
                cur.execute(
                    """INSERT INTO jersey_observations
                         (media_asset_id, clip_id, video_seconds, digits, ocr_confidence, bbox)
                       VALUES (%s,%s,%s,%s,%s,%s)""",
                    (media_asset_id, clip_id, o.video_seconds, o.digits, o.ocr_confidence,
                     json.dumps(list(o.bbox) if o.bbox else None)),
                )

    def update_clip_confidence(self, clip_id: str, score: float, factors: dict, method: str) -> None:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                """UPDATE clips
                      SET match_confidence = %s, confidence_factors = %s,
                          match_method = %s, updated_at = now()
                    WHERE id = %s""",
                (score, json.dumps(factors), method, clip_id),
            )

    def mark_media_ready(self, asset_id: str, probe) -> None:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                """UPDATE media_assets
                      SET duration_seconds = %s, width = %s, height = %s, fps = %s,
                          has_audio = %s, byte_size = COALESCE(byte_size, %s),
                          recording_started_at = COALESCE(recording_started_at, %s),
                          status = 'ready', error_message = NULL
                    WHERE id = %s""",
                (probe.duration_seconds, probe.width, probe.height, probe.fps,
                 probe.has_audio, probe.byte_size, probe.recording_started_at, asset_id),
            )

    def mark_media_failed(self, asset_id: str, message: str) -> None:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE media_assets SET status = 'failed', error_message = %s WHERE id = %s",
                (message[:2000], asset_id),
            )

    def record_reel_output(self, reel_id: str, output_key: str, duration: float, byte_size: int) -> None:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                """UPDATE reels
                      SET output_key = %s, duration_seconds = %s, byte_size = %s, rendered_at = now()
                    WHERE id = %s""",
                (output_key, duration, byte_size, reel_id),
            )

    def audit(self, action: str, entity_type: str, entity_id: str | None, metadata: dict | None = None) -> None:
        with self.connect() as conn, conn.cursor() as cur:
            cur.execute(
                """INSERT INTO audit_log (action, entity_type, entity_id, metadata)
                   VALUES (%s,%s,%s,%s)""",
                (action, entity_type, entity_id, json.dumps(metadata or {})),
            )
