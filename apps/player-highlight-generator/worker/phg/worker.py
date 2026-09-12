"""The job loop and its handlers.

Jobs live in PostgreSQL rather than Redis or SQS. For a single-team private
deployment that is the right trade: one fewer service to run, transactional
consistency with the data the jobs operate on, and `FOR UPDATE SKIP LOCKED`
gives multi-worker safety for free.

Pipeline order for a game:

    probe_media (per upload)
        -> match_plays (per game)          produces clip rows
            -> analyze_clip (per clip)     dead time, then jersey OCR if uncertain
                -> cut_clip (per clip)     writes the clip MP4
                    -> render_reel         per player, per scope, per aspect
"""

from __future__ import annotations

import json
import logging
import signal
import time
from pathlib import Path
from typing import Any, Callable

from phg import config
from phg.db import Database
from phg.matching.confidence import ConfidenceResult, apply_jersey
from phg.matching.jersey_ocr import JerseyReader, OcrSettings, summarize
from phg.matching.play_matcher import PlayMatcher
from phg.models import Play
from phg.ranking import RankInputs, score_clip
from phg.video import deadtime, probe
from phg.video.clipper import ClipSpec, cut
from phg.video.deadtime import DeadTimeSettings

log = logging.getLogger(__name__)

Handler = Callable[[Database, config.Config, dict[str, Any]], dict[str, Any]]
_HANDLERS: dict[str, Handler] = {}


def handler(name: str):
    def register(fn: Handler) -> Handler:
        _HANDLERS[name] = fn
        return fn
    return register


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


@handler("probe_media")
def probe_media(db: Database, cfg: config.Config, job: dict[str, Any]) -> dict[str, Any]:
    asset_id = str(job["target_id"])
    storage_key = job["payload"].get("storage_key")
    if not storage_key:
        raise ValueError("probe_media requires storage_key in the payload")

    path = str(cfg.media_root / storage_key)
    try:
        result = probe.probe(path, cfg.video.ffprobe)
    except probe.ProbeError as exc:
        db.mark_media_failed(asset_id, str(exc))
        raise

    db.mark_media_ready(asset_id, result)
    db.audit("media.probed", "media_asset", asset_id, {
        "duration": result.duration_seconds,
        "resolution": f"{result.width}x{result.height}",
        "recording_started_at": result.recording_started_at.isoformat() if result.recording_started_at else None,
    })

    game_id = job["payload"].get("game_id")
    if game_id and job["payload"].get("auto_match", True):
        db.enqueue("match_plays", "game", game_id, {})
    return {"duration_seconds": result.duration_seconds}


@handler("match_plays")
def match_plays(db: Database, cfg: config.Config, job: dict[str, Any]) -> dict[str, Any]:
    game_id = str(job["target_id"])
    settings = db.team_settings(game_id)

    players = db.load_players(game_id)
    plays = db.load_plays(game_id)
    assets = db.load_media(game_id, str(cfg.media_root))

    if not plays:
        return {"skipped": "no play-by-play imported for this game"}
    if not assets:
        return {"skipped": "no ready video for this game"}

    consented = db.players_with_consent(str(settings["team_id"]))
    matcher = PlayMatcher(
        players=players,
        pre_roll=float(settings.get("pre_roll_seconds") or cfg.video.pre_roll_seconds),
        post_roll=float(settings.get("post_roll_seconds") or cfg.video.post_roll_seconds),
        base_window_seconds=cfg.matching.base_search_window_seconds,
        drift_seconds_per_minute=cfg.matching.drift_seconds_per_minute,
    )
    report = matcher.match_game(plays, assets)

    # Persist identities before clips: the stat overlays read from the derived
    # views, which join play_participants on player_id.
    resolved_count = db.save_participant_resolutions(report.participants)

    by_id: dict[str, Play] = {p.id: p for p in plays}
    total_innings = max((p.inning for p in plays), default=7)

    kept = []
    for candidate in report.candidates:
        # Consent gate: no reel is built for a player without an active
        # highlight_generation consent on file.
        if consented and candidate.player_id not in consented:
            continue
        play = by_id.get(candidate.play_id or "")
        if play is None:
            continue
        role = {"offense": "batter", "baserunning": "runner",
                "pitching": "pitcher", "defense": "fielder_putout"}[candidate.category]
        score_clip(candidate, RankInputs(
            play=play, role=role, category=candidate.category, total_innings=total_innings,
        ))
        kept.append(candidate)

    written = db.replace_clips_for_game(
        game_id, kept,
        auto_approve_threshold=float(settings.get("auto_approve_threshold") or cfg.matching.auto_approve_threshold),
        review_floor=float(settings.get("review_floor_threshold") or cfg.matching.review_floor_threshold),
    )

    db.audit("game.matched", "game", game_id, {
        "participants_resolved": resolved_count,
        "candidates": len(report.candidates),
        "written": written,
        "skipped_plays": len(report.skipped),
        "inferred_timestamps": report.plays_with_inferred_time,
        "sync_anchors": report.anchor_count,
    })

    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            """SELECT c.id FROM clips c JOIN plays p ON p.id = c.play_id
                WHERE p.game_id = %s AND c.review_status IN ('auto_approved','needs_review')""",
            (game_id,),
        )
        for row in cur.fetchall():
            db.enqueue("analyze_clip", "clip", str(row["id"]), {"game_id": game_id})

    return {
        "participants_resolved": resolved_count,
        "candidates": len(report.candidates),
        "clips_written": written,
        "plays_skipped": len(report.skipped),
        "sync_anchors": report.anchor_count,
    }


@handler("analyze_clip")
def analyze_clip(db: Database, cfg: config.Config, job: dict[str, Any]) -> dict[str, Any]:
    """Dead-time detection, then jersey OCR only if confidence is uncertain."""
    clip_id = str(job["target_id"])
    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            """SELECT c.*, m.storage_key, pl.jersey_number, t.id AS team_id,
                      ts.dead_time_removal, ts.motion_threshold, ts.jersey_ocr_enabled
                 FROM clips c
                 JOIN media_assets m ON m.id = c.media_asset_id
                 JOIN players pl     ON pl.id = c.player_id
                 JOIN teams t        ON t.id = pl.team_id
            LEFT JOIN team_settings ts ON ts.team_id = t.id
                WHERE c.id = %s""",
            (clip_id,),
        )
        clip = cur.fetchone()
    if clip is None:
        return {"skipped": "clip no longer exists"}

    path = str(cfg.media_root / clip["storage_key"])
    start = float(clip["source_start_seconds"])
    end = float(clip["source_end_seconds"])
    duration = end - start

    density = 0.5
    if clip.get("dead_time_removal", cfg.video.dead_time_removal):
        settings = DeadTimeSettings(
            sample_fps=cfg.video.motion_sample_fps,
            motion_threshold=float(clip.get("motion_threshold") or cfg.video.motion_threshold),
            min_kept_seconds=cfg.video.min_kept_seconds,
        )
        profile = deadtime.profile_window(path, start, end, settings)
        segments = deadtime.segments_for(profile, duration)
        db.save_segments(clip_id, segments)
        density = profile.density

    # Jersey recognition: secondary, banded, capped - and best-effort.
    #
    # It runs inside its own try/except because it is an optional signal built
    # on optional dependencies (Tesseract, and an OpenCV 4.x person detector).
    # Letting it fail this job would also discard the dead-time result above and
    # skip queueing the cut, so a missing optional dependency would cost the
    # coach the clip entirely. It must never do that.
    confidence = float(clip["match_confidence"])
    jersey_used = False
    in_band = cfg.matching.jersey_band_low <= confidence < cfg.matching.jersey_band_high
    enabled = cfg.matching.jersey_enabled and clip.get("jersey_ocr_enabled", True)

    if enabled and in_band and clip["jersey_number"]:
        try:
            reader = JerseyReader(OcrSettings())
            if not reader.available:
                log.info("clip %s: %s", clip_id, reader.unavailable_reason)
            else:
                observations = reader.read_window(path, start, end)
                db.save_jersey_observations(str(clip["media_asset_id"]), clip_id, observations)
                if observations:
                    result = ConfidenceResult(
                        score=confidence,
                        factors=dict(clip["confidence_factors"] or {}),
                        method=clip["match_method"],
                    )
                    apply_jersey(
                        result,
                        expected_jersey=clip["jersey_number"],
                        observations=summarize(observations),
                        max_adjustment=cfg.matching.jersey_max_adjustment,
                    )
                    db.update_clip_confidence(clip_id, result.score, result.factors, result.method)
                    confidence = result.score
                    jersey_used = True
        except Exception as exc:  # noqa: BLE001 - a secondary signal never fails the job
            log.warning("clip %s: jersey recognition skipped (%s)", clip_id, exc)

    # Re-decide review status now that both signals are in.
    auto = cfg.matching.auto_approve_threshold
    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            """UPDATE clips
                  SET review_status = CASE
                        WHEN review_status IN ('approved','rejected') THEN review_status
                        WHEN %s >= %s THEN 'auto_approved'::review_status
                        ELSE 'needs_review'::review_status END,
                      rank_factors = rank_factors || %s::jsonb
                WHERE id = %s""",
            (confidence, auto, json.dumps({"action_density": round(density * 100, 2)}), clip_id),
        )

    db.enqueue("cut_clip", "clip", clip_id, {})
    return {"confidence": confidence, "jersey_used": jersey_used, "action_density": density}


@handler("cut_clip")
def cut_clip(db: Database, cfg: config.Config, job: dict[str, Any]) -> dict[str, Any]:
    clip_id = str(job["target_id"])
    aspect = job["payload"].get("aspect", "16:9")

    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            """SELECT c.*, m.storage_key,
                      COALESCE(json_agg(json_build_object('s', cs.start_seconds, 'e', cs.end_seconds)
                               ORDER BY cs.position) FILTER (WHERE cs.keep), '[]') AS spans
                 FROM clips c
                 JOIN media_assets m ON m.id = c.media_asset_id
            LEFT JOIN clip_segments cs ON cs.clip_id = c.id
                WHERE c.id = %s
             GROUP BY c.id, m.storage_key""",
            (clip_id,),
        )
        clip = cur.fetchone()
    if clip is None:
        return {"skipped": "clip no longer exists"}

    source = str(cfg.media_root / clip["storage_key"])
    start = float(clip["source_start_seconds"])
    kept = clip["spans"] or []
    spans = (
        [(start + float(s["s"]), start + float(s["e"])) for s in kept]
        if kept else [(start, float(clip["source_end_seconds"]))]
    )

    out_key = f"clips/{clip_id}_{aspect.replace(':', 'x')}.mp4"
    out_path = str(cfg.media_root / out_key)

    cut(ClipSpec(
        source_path=source,
        output_path=out_path,
        spans=spans,
        aspect=aspect,
        crf=cfg.video.render_crf,
        preset=cfg.video.render_preset,
        ffmpeg=cfg.video.ffmpeg,
    ))

    with db.connect() as conn, conn.cursor() as cur:
        cur.execute("UPDATE clips SET preview_key = %s, updated_at = now() WHERE id = %s",
                    (out_key, clip_id))
    return {"output": out_key, "spans": len(spans)}


@handler("render_reel")
def render_reel_job(db: Database, cfg: config.Config, job: dict[str, Any]) -> dict[str, Any]:
    """Delegated to reels.build so the assembly logic stays testable."""
    from phg.reels import build_reel

    reel_id = str(job["target_id"])
    result = build_reel(db, cfg, reel_id)
    db.record_reel_output(reel_id, result["output_key"], result["duration"], result["byte_size"])
    db.audit("reel.rendered", "reel", reel_id, result)
    return result


# ---------------------------------------------------------------------------
# Loop
# ---------------------------------------------------------------------------


class Worker:
    def __init__(self, cfg: config.Config | None = None) -> None:
        self.cfg = cfg or config.load()
        self.db = Database(self.cfg.database_url)
        self._running = True
        Path(self.cfg.work_root).mkdir(parents=True, exist_ok=True)

    def stop(self, *_: Any) -> None:
        log.info("shutdown requested; finishing current job")
        self._running = False

    def run(self) -> None:
        signal.signal(signal.SIGTERM, self.stop)
        signal.signal(signal.SIGINT, self.stop)
        log.info("worker %s started", self.cfg.worker_name)

        while self._running:
            job = self.db.claim_job(self.cfg.worker_name)
            if job is None:
                time.sleep(self.cfg.poll_interval_seconds)
                continue
            self.run_job(job)

        log.info("worker %s stopped", self.cfg.worker_name)

    def run_job(self, job: dict[str, Any]) -> None:
        job_type = job["job_type"]
        fn = _HANDLERS.get(job_type)
        if fn is None:
            self.db.finish_job(str(job["id"]), status="failed", error=f"unknown job type {job_type}")
            return

        started = time.time()
        try:
            result = fn(self.db, self.cfg, job)
            self.db.finish_job(str(job["id"]), status="succeeded")
            log.info("%s %s ok in %.1fs: %s", job_type, job["target_id"], time.time() - started, result)
        except Exception as exc:  # noqa: BLE001 - the loop must survive any handler
            log.exception("%s %s failed", job_type, job["target_id"])
            self.db.retry_or_fail(job, f"{type(exc).__name__}: {exc}")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s %(message)s",
    )
    Worker().run()


if __name__ == "__main__":
    main()
