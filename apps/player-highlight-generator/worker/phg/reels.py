"""Assemble a player's reel from approved clips.

Scope drives the clip query (one game, one tournament, a whole season) and the
intro card's stat line. Everything else - branding, music, aspect - comes from
team settings with per-reel overrides.

A rejected clip is never included. A clip still sitting in the review queue is
never included either: an unreviewed uncertain match is exactly the clip that
would put another child in a player's reel.
"""

from __future__ import annotations

import logging
import os
import tempfile
from pathlib import Path

from phg import config
from phg.db import Database
from phg.video.overlays import BrandTheme, PlayerCardData, render_intro_card
from phg.video.render import MusicBed, ReelSpec, render_reel

log = logging.getLogger(__name__)

_SCOPE_FILTER = {
    "game": "p.game_id = %(game_id)s",
    "tournament": "g.tournament_id = %(tournament_id)s",
    "season": "g.season_id = %(season_id)s",
}


def _load_reel(db: Database, reel_id: str) -> dict:
    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            """SELECT r.*, pl.first_name, pl.last_name, pl.preferred_name, pl.jersey_number,
                      t.id AS team_id, t.name AS team_name, t.primary_color, t.secondary_color,
                      t.logo_key, s.name AS season_name,
                      ts.show_intro_card, ts.show_score_overlay, ts.show_stat_overlay,
                      ts.music_volume_db, ts.duck_music_on_action, ts.default_music_track_id,
                      mt.storage_key AS music_key
                 FROM reels r
                 JOIN players pl ON pl.id = r.player_id
                 JOIN teams t    ON t.id = pl.team_id
            LEFT JOIN seasons s  ON s.id = r.season_id
            LEFT JOIN team_settings ts ON ts.team_id = t.id
            LEFT JOIN music_tracks mt  ON mt.id = COALESCE(r.music_track_id, ts.default_music_track_id)
                WHERE r.id = %s""",
            (reel_id,),
        )
        row = cur.fetchone()
    if row is None:
        raise ValueError(f"reel {reel_id} not found")
    return row


def _load_clips(db: Database, reel: dict) -> list[dict]:
    """Clips already pinned to the reel, or the auto-selection if none are."""
    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            """SELECT c.*, rc.position, rc.include_slowmo
                 FROM reel_clips rc JOIN clips c ON c.id = rc.clip_id
                WHERE rc.reel_id = %s ORDER BY rc.position""",
            (str(reel["id"]),),
        )
        pinned = cur.fetchall()
        if pinned:
            return pinned

        scope = reel["scope"]
        where = _SCOPE_FILTER[scope]
        cur.execute(
            f"""SELECT c.*, NULL::int AS position, FALSE AS include_slowmo
                  FROM clips c
                  JOIN plays p ON p.id = c.play_id
                  JOIN games g ON g.id = p.game_id
                 WHERE c.player_id = %(player_id)s
                   AND c.review_status IN ('auto_approved','approved')
                   AND c.preview_key IS NOT NULL
                   AND {where}
              ORDER BY c.rank_score DESC
                 LIMIT 12""",
            {
                "player_id": str(reel["player_id"]),
                "game_id": reel["game_id"],
                "tournament_id": reel["tournament_id"],
                "season_id": reel["season_id"],
            },
        )
        return cur.fetchall()


def _stat_lines(db: Database, reel: dict) -> list[tuple[str, str]]:
    player_id = str(reel["player_id"])
    with db.connect() as conn, conn.cursor() as cur:
        if reel["scope"] == "game":
            cur.execute(
                """SELECT b.hits, b.at_bats, b.rbi, b.runs, b.home_runs,
                          COALESCE(pi.strikeouts, 0) AS k
                     FROM player_game_batting b
                LEFT JOIN player_game_pitching pi
                       ON pi.player_id = b.player_id AND pi.game_id = b.game_id
                    WHERE b.player_id = %s AND b.game_id = %s""",
                (player_id, reel["game_id"]),
            )
            row = cur.fetchone()
            if not row:
                return []
            lines = [("H/AB", f"{row['hits']}/{row['at_bats']}"), ("RBI", str(row["rbi"]))]
            if row["home_runs"]:
                lines.append(("HR", str(row["home_runs"])))
            if row["k"]:
                lines.append(("K", str(row["k"])))
            return lines

        cur.execute(
            """SELECT batting_average, hits, rbi, home_runs, runs
                 FROM player_season_batting
                WHERE player_id = %s AND season_id = %s""",
            (player_id, reel["season_id"] or reel["game_id"]),
        )
        row = cur.fetchone()
        if not row:
            return []
        avg = f"{row['batting_average']:.3f}".lstrip("0") if row["batting_average"] else "-"
        return [("AVG", avg), ("H", str(row["hits"])), ("RBI", str(row["rbi"])), ("HR", str(row["home_runs"]))]


def build_reel(db: Database, cfg: config.Config, reel_id: str) -> dict:
    reel = _load_reel(db, reel_id)
    clips = _load_clips(db, reel)
    if not clips:
        raise ValueError(
            "reel has no eligible clips; every candidate is either rejected or still awaiting review"
        )

    aspect = reel["aspect"]
    work = Path(tempfile.mkdtemp(prefix=f"phg-reel-{reel_id[:8]}-", dir=str(cfg.work_root)))

    theme = BrandTheme(
        team_name=reel["team_name"],
        primary_color=reel["primary_color"],
        secondary_color=reel["secondary_color"],
        logo_path=str(cfg.media_root / reel["logo_key"]) if reel["logo_key"] else None,
    )

    intro_png = None
    if reel.get("show_intro_card", True):
        display = f"{reel['preferred_name'] or reel['first_name']} {reel['last_name']}"
        subtitle = " - ".join(x for x in (reel.get("season_name"), reel["team_name"]) if x)
        intro_png = render_intro_card(
            PlayerCardData(
                display_name=display,
                jersey_number=reel["jersey_number"],
                subtitle=subtitle,
                stat_lines=_stat_lines(db, reel),
            ),
            theme,
            work / "intro.png",
            aspect,
        )

    music = None
    if reel.get("music_key"):
        music = MusicBed(
            path=str(cfg.media_root / reel["music_key"]),
            volume_db=float(reel.get("music_volume_db") or cfg.video.music_volume_db),
            duck=bool(reel.get("duck_music_on_action", True)),
        )

    clip_paths = []
    for c in clips:
        path = str(cfg.media_root / c["preview_key"])
        if os.path.exists(path):
            clip_paths.append(path)
        else:
            log.warning("clip %s has no rendered file at %s; skipped", c["id"], path)
    if not clip_paths:
        raise ValueError("none of this reel's clips have been cut yet")

    out_key = f"reels/{reel_id}_{aspect.replace(':', 'x')}.mp4"
    out_path = str(cfg.media_root / out_key)

    render_reel(ReelSpec(
        clip_paths=clip_paths,
        output_path=out_path,
        aspect=aspect,
        intro_card_png=intro_png,
        music=music,
        crf=cfg.video.render_crf,
        preset=cfg.video.render_preset,
        ffmpeg=cfg.video.ffmpeg,
        work_dir=str(work),
    ))

    from phg.video.probe import probe as probe_file

    info = probe_file(out_path, cfg.video.ffprobe)
    return {
        "output_key": out_key,
        "duration": info.duration_seconds,
        "byte_size": os.path.getsize(out_path),
        "clip_count": len(clip_paths),
        "aspect": aspect,
    }
