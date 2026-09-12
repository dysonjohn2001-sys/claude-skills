"""End-to-end matching against a real PostgreSQL database.

Skipped unless PHG_TEST_DSN points at a database with the migrations applied.
Run it against a throwaway database - it writes and deletes rows.

    createdb phg_test
    psql phg_test -f db/migrations/0001_init.sql
    psql phg_test -f db/migrations/0002_stat_views.sql
    PHG_TEST_DSN=postgresql:///phg_test python -m pytest tests/test_db_integration.py
"""

from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

import pytest

psycopg = pytest.importorskip("psycopg")

from phg.db import Database  # noqa: E402
from phg.matching.play_matcher import PlayMatcher  # noqa: E402
from phg.ranking import RankInputs, score_clip  # noqa: E402

DSN = os.environ.get("PHG_TEST_DSN")
pytestmark = pytest.mark.skipif(not DSN, reason="PHG_TEST_DSN is not set")

FIRST_PITCH = datetime(2026, 4, 18, 14, 4, 0, tzinfo=timezone.utc)


@pytest.fixture()
def fixture_game():
    """Create a team, season, game, roster, plays and a video; tear it all down."""
    db = Database(DSN)
    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            "INSERT INTO teams (name) VALUES ('Integration Rays') RETURNING id"
        )
        team_id = cur.fetchone()["id"]
        cur.execute(
            """INSERT INTO seasons (team_id, name, starts_on)
               VALUES (%s, 'Test Season', '2026-03-01') RETURNING id""",
            (team_id,),
        )
        season_id = cur.fetchone()["id"]
        cur.execute(
            """INSERT INTO games (season_id, played_on, first_pitch_at, opponent_name)
               VALUES (%s, '2026-04-18', %s, 'Test Owls') RETURNING id""",
            (season_id, FIRST_PITCH),
        )
        game_id = cur.fetchone()["id"]

        players = {}
        roster = [
            ("Jake", "Smith", "7", "SS", 1),
            ("Marcus", "Hernandez", "12", "2B", 2),
            ("Liam", "Nguyen", "15", "P", 3),
        ]
        for first, last, jersey, position, order in roster:
            cur.execute(
                """INSERT INTO players (team_id, first_name, last_name, jersey_number)
                   VALUES (%s,%s,%s,%s) RETURNING id""",
                (team_id, first, last, jersey),
            )
            player_id = cur.fetchone()["id"]
            players[last] = player_id
            cur.execute(
                "INSERT INTO player_positions (player_id, position, is_primary) VALUES (%s,%s,TRUE)",
                (player_id, position),
            )
            cur.execute(
                """INSERT INTO lineup_entries (game_id, player_id, batting_order, starting_position)
                   VALUES (%s,%s,%s,%s)""",
                (game_id, player_id, order, position),
            )
            # Every player gets highlight consent, or the matcher skips them.
            cur.execute(
                """INSERT INTO guardians (full_name, email) VALUES (%s, %s) RETURNING id""",
                (f"{first} guardian", f"{last.lower()}@example.test"),
            )
            guardian_id = cur.fetchone()["id"]
            cur.execute(
                "INSERT INTO player_guardians (player_id, guardian_id) VALUES (%s,%s)",
                (player_id, guardian_id),
            )
            for consent_type in ("media_capture", "highlight_generation"):
                cur.execute(
                    """INSERT INTO consents (player_id, guardian_id, type, granted)
                       VALUES (%s,%s,%s,TRUE)""",
                    (player_id, guardian_id, consent_type),
                )

        cur.execute(
            """INSERT INTO media_assets
                 (game_id, kind, storage_key, original_filename, duration_seconds,
                  width, height, fps, has_audio, status)
               VALUES (%s,'full_game','games/test.mp4','test.mp4',7200,1920,1080,30,TRUE,'ready')
               RETURNING id""",
            (game_id,),
        )
        asset_id = cur.fetchone()["id"]

        plays = [
            (1, 1, "top", 0, "double", "Jake Smith doubles to left", True, "Jake Smith", None, 1),
            (2, 1, "top", 120, "single", "Marcus Hernandez singles", True, "Marcus Hernandez", None, 2),
            (3, 1, "bottom", 600, "strikeout", "B. Carter strikes out", False, None, "Liam Nguyen", None),
        ]
        play_ids = []
        for seq, inning, half, offset, play_type, description, ours, batter, pitcher, order in plays:
            cur.execute(
                """INSERT INTO plays
                     (game_id, sequence_no, inning, half, occurred_at, play_type, description,
                      is_our_offense, batter_name_raw, pitcher_name_raw, raw_row)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
                (
                    game_id, seq, inning, half, FIRST_PITCH + timedelta(seconds=offset),
                    play_type, description, ours, batter, pitcher,
                    '{"batting_order": %s}' % (order if order else "null"),
                ),
            )
            play_ids.append(cur.fetchone()["id"])

        # One sync anchor: the first play happens 300 seconds into the recording.
        cur.execute(
            """INSERT INTO media_sync_anchors (media_asset_id, video_seconds, play_id)
               VALUES (%s, 300, %s)""",
            (asset_id, play_ids[0]),
        )

    yield {"db": db, "team_id": team_id, "game_id": game_id, "players": players}

    with db.connect() as conn, conn.cursor() as cur:
        cur.execute("DELETE FROM teams WHERE id = %s", (team_id,))


def test_loads_roster_with_lineup_and_positions(fixture_game):
    players = fixture_game["db"].load_players(fixture_game["game_id"])
    assert len(players) == 3
    smith = next(p for p in players if p.last_name == "Smith")
    assert smith.batting_order == 1
    assert smith.positions == ("SS",)
    assert smith.jersey_number == "7"


def test_loads_media_with_its_sync_anchor(fixture_game):
    assets = fixture_game["db"].load_media(fixture_game["game_id"], "/media")
    assert len(assets) == 1
    assert assets[0].anchors[0].video_seconds == 300.0
    assert assets[0].duration_seconds == 7200.0


def test_consent_gate_lists_only_consented_players(fixture_game):
    consented = fixture_game["db"].players_with_consent(fixture_game["team_id"])
    assert consented == set(map(str, fixture_game["players"].values()))


def test_full_match_writes_clips_with_the_right_categories(fixture_game):
    db, game_id = fixture_game["db"], fixture_game["game_id"]
    players = db.load_players(game_id)
    plays = db.load_plays(game_id)
    assets = db.load_media(game_id, "/media")

    report = PlayMatcher(players=players).match_game(plays, assets)
    by_play = {p.id: p for p in plays}
    for candidate in report.candidates:
        play = by_play[candidate.play_id]
        role = {"offense": "batter", "baserunning": "runner",
                "pitching": "pitcher", "defense": "fielder_putout"}[candidate.category]
        score_clip(candidate, RankInputs(play=play, role=role, category=candidate.category))

    written = db.replace_clips_for_game(
        game_id, report.candidates, auto_approve_threshold=0.80, review_floor=0.45
    )
    assert written >= 3

    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            """SELECT pl.last_name, c.category, c.match_confidence, c.review_status,
                      c.source_start_seconds, c.source_end_seconds
                 FROM clips c
                 JOIN players pl ON pl.id = c.player_id
                 JOIN plays p    ON p.id = c.play_id
                WHERE p.game_id = %s ORDER BY c.source_start_seconds""",
            (game_id,),
        )
        rows = cur.fetchall()

    categories = {(r["last_name"], r["category"]) for r in rows}
    assert ("Smith", "offense") in categories
    assert ("Hernandez", "offense") in categories
    assert ("Nguyen", "pitching") in categories

    # The anchor puts play 1 at video second 300; with 5s lead-in the window
    # opens at 295 and, with 8s follow-through, closes at 308.
    first = rows[0]
    assert float(first["source_start_seconds"]) == pytest.approx(295.0)
    assert float(first["source_end_seconds"]) == pytest.approx(308.0)

    # Clean, timestamped, lineup-confirmed data should clear review outright.
    assert all(float(r["match_confidence"]) >= 0.80 for r in rows)
    assert all(r["review_status"] == "auto_approved" for r in rows)


def test_rerunning_matching_preserves_a_coach_decision(fixture_game):
    db, game_id = fixture_game["db"], fixture_game["game_id"]
    players = db.load_players(game_id)
    plays = db.load_plays(game_id)
    assets = db.load_media(game_id, "/media")
    report = PlayMatcher(players=players).match_game(plays, assets)
    db.replace_clips_for_game(game_id, report.candidates, 0.80, 0.45)

    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            """UPDATE clips c SET review_status = 'rejected'
                 FROM plays p WHERE p.id = c.play_id AND p.game_id = %s
                 AND c.id = (SELECT c2.id FROM clips c2 JOIN plays p2 ON p2.id = c2.play_id
                              WHERE p2.game_id = %s LIMIT 1)
               RETURNING c.id""",
            (game_id, game_id),
        )
        rejected_id = cur.fetchone()["id"]

    db.replace_clips_for_game(game_id, report.candidates, 0.80, 0.45)

    with db.connect() as conn, conn.cursor() as cur:
        cur.execute("SELECT review_status FROM clips WHERE id = %s", (rejected_id,))
        row = cur.fetchone()
    assert row is not None, "a rejected clip must survive a re-match"
    assert row["review_status"] == "rejected"


def test_job_queue_claims_exactly_once(fixture_game):
    db = fixture_game["db"]
    job_id = db.enqueue("match_plays", "game", fixture_game["game_id"], {"source": "test"})

    first = db.claim_job("worker-a")
    while first and str(first["id"]) != job_id:
        db.finish_job(str(first["id"]), status="succeeded")
        first = db.claim_job("worker-a")
    assert first is not None and str(first["id"]) == job_id

    # A second worker polling at the same moment must not get the same job.
    second = db.claim_job("worker-b")
    assert second is None or str(second["id"]) != job_id

    db.finish_job(job_id, status="succeeded")
    with db.connect() as conn, conn.cursor() as cur:
        cur.execute("SELECT status, progress FROM jobs WHERE id = %s", (job_id,))
        row = cur.fetchone()
    assert row["status"] == "succeeded"
    assert float(row["progress"]) == 100.0


def test_resolved_participants_feed_the_statistics_views(fixture_game):
    """Without this write-back every stat overlay and intro card comes out blank."""
    db, game_id = fixture_game["db"], fixture_game["game_id"]
    players = db.load_players(game_id)
    plays = db.load_plays(game_id)
    assets = db.load_media(game_id, "/media")

    report = PlayMatcher(players=players).match_game(plays, assets)
    assert report.participants, "matching produced no resolved participants"

    written = db.save_participant_resolutions(report.participants)
    assert written > 0

    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            """SELECT count(*) AS n FROM play_participants pp
                 JOIN plays p ON p.id = pp.play_id
                WHERE p.game_id = %s AND pp.player_id IS NULL""",
            (game_id,),
        )
        assert cur.fetchone()["n"] == 0, "some credited names never resolved"

        # Smith doubled and Hernandez singled, so the batting view should show
        # one hit apiece.
        cur.execute(
            """SELECT pl.last_name, b.hits, b.at_bats
                 FROM player_game_batting b
                 JOIN players pl ON pl.id = b.player_id
                WHERE b.game_id = %s ORDER BY pl.last_name""",
            (game_id,),
        )
        batting = {r["last_name"]: (r["hits"], r["at_bats"]) for r in cur.fetchall()}
    assert batting.get("Smith") == (1, 1)
    assert batting.get("Hernandez") == (1, 1)


def test_rerunning_resolution_is_idempotent(fixture_game):
    db, game_id = fixture_game["db"], fixture_game["game_id"]
    report = PlayMatcher(players=db.load_players(game_id)).match_game(
        db.load_plays(game_id), db.load_media(game_id, "/media")
    )
    db.save_participant_resolutions(report.participants)

    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            """SELECT count(*) AS n FROM play_participants pp
                 JOIN plays p ON p.id = pp.play_id WHERE p.game_id = %s""",
            (game_id,),
        )
        before = cur.fetchone()["n"]

    # A second pass must update in place, never duplicate.
    assert db.save_participant_resolutions(report.participants) == 0

    with db.connect() as conn, conn.cursor() as cur:
        cur.execute(
            """SELECT count(*) AS n FROM play_participants pp
                 JOIN plays p ON p.id = pp.play_id WHERE p.game_id = %s""",
            (game_id,),
        )
        assert cur.fetchone()["n"] == before
