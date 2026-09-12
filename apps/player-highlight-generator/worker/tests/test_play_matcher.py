from datetime import datetime, timedelta, timezone

import pytest

from phg.matching.play_matcher import PlayMatcher
from phg.models import MediaAsset, Play, Player, SyncAnchor

T0 = datetime(2026, 4, 18, 10, 0, 0, tzinfo=timezone.utc)

ROSTER = [
    Player(id="pl1", first_name="Jake", last_name="Smith", jersey_number="7",
           positions=("SS", "P"), batting_order=1),
    Player(id="pl2", first_name="Marcus", last_name="Hernandez", jersey_number="12",
           positions=("2B",), batting_order=2),
    Player(id="pl3", first_name="Owen", last_name="Brooks", jersey_number="21",
           positions=("CF",), batting_order=3),
]

ASSET = MediaAsset(
    id="m1", game_id="g1", kind="full_game", path="/tmp/game.mp4",
    duration_seconds=7200.0,
    anchors=(SyncAnchor(video_seconds=300.0, wall_clock_at=T0),),
)


def play(seq, offset_seconds, **kw):
    args = dict(
        id=f"p{seq}", game_id="g1", sequence_no=seq, inning=1, half="top",
        play_type="single", description="a hit", is_our_offense=True,
        occurred_at=T0 + timedelta(seconds=offset_seconds),
        batter_name_raw="Jake Smith",
    )
    args.update(kw)
    return Play(**args)


def matcher(**kw):
    return PlayMatcher(players=ROSTER, **kw)


def test_a_clean_play_produces_one_offensive_clip_in_the_right_window():
    report = matcher().match_game([play(1, 60, raw_row={"batting_order": 1})], [ASSET])
    assert len(report.candidates) == 1
    c = report.candidates[0]
    assert c.player_id == "pl1"
    assert c.category == "offense"
    # Anchor puts wall-clock T0 at video 300s, so T0+60s is video 360s.
    assert c.source_start_seconds == pytest.approx(355.0)
    assert c.source_end_seconds == pytest.approx(368.0)
    assert c.match_confidence >= 0.80


def test_roll_settings_change_the_window():
    report = matcher(pre_roll=2.0, post_roll=3.0).match_game([play(1, 60)], [ASSET])
    c = report.candidates[0]
    assert c.source_end_seconds - c.source_start_seconds == pytest.approx(5.0)


def test_defensive_play_credits_the_fielder_not_the_batter():
    p = play(
        1, 120, is_our_offense=False, batter_name_raw=None,
        pitcher_name_raw="Owen Brooks", play_type="groundout",
        raw_row={"putout_by": ["Jake Smith"]},
    )
    report = matcher().match_game([p], [ASSET])
    by_player = {c.player_id: c.category for c in report.candidates}
    assert by_player["pl1"] == "defense"
    assert by_player["pl3"] == "pitching"


def test_baserunning_play_is_categorised_separately():
    p = play(1, 200, play_type="stolen_base", batter_name_raw="Marcus Hernandez")
    report = matcher().match_game([p], [ASSET])
    assert report.candidates[0].category == "baserunning"


def test_unmatched_name_is_dropped_rather_than_guessed():
    p = play(1, 60, batter_name_raw="Somebody Else Entirely", raw_row={})
    report = matcher().match_game([p], [ASSET])
    assert report.candidates == []


def test_batting_order_disagreement_lowers_confidence_without_discarding():
    agrees = matcher().match_game([play(1, 60, raw_row={"batting_order": 1})], [ASSET])
    differs = matcher().match_game([play(1, 60, raw_row={"batting_order": 3})], [ASSET])
    assert differs.candidates[0].match_confidence < agrees.candidates[0].match_confidence
    assert differs.candidates[0].match_confidence > 0


def test_missing_timestamps_are_interpolated_between_known_ones():
    plays = [
        play(1, 0),
        play(2, 0, occurred_at=None),
        play(3, 600),
    ]
    report = matcher().match_game(plays, [ASSET])
    assert report.plays_with_inferred_time == 1
    middle = next(c for c in report.candidates if c.play_id == "p2")
    # Halfway between video 300s and video 900s.
    assert middle.source_start_seconds == pytest.approx(595.0, abs=1.0)


def test_no_timestamps_at_all_paces_from_first_pitch():
    plays = [play(i, 0, inning=i, occurred_at=None) for i in (1, 2, 3)]
    report = matcher().match_game(plays, [ASSET], first_pitch_at=T0)
    assert report.plays_with_inferred_time == 3
    starts = sorted(c.source_start_seconds for c in report.candidates)
    assert starts == sorted(set(starts))          # innings spread out, not stacked


def test_a_play_outside_every_video_is_reported_not_clipped():
    far = play(1, 100_000)
    report = matcher().match_game([far], [ASSET])
    assert report.candidates == []
    assert any("outside every uploaded video" in reason for _, reason in report.skipped)


def test_asset_without_any_time_reference_is_reported():
    orphan = MediaAsset(
        id="m2", game_id="g1", kind="full_game", path="/tmp/o.mp4", duration_seconds=100.0,
    )
    report = matcher().match_game([play(1, 60)], [orphan])
    assert any("sync anchor" in reason for _, reason in report.skipped)


def test_windows_never_run_past_the_end_of_the_file():
    short = MediaAsset(
        id="m3", game_id="g1", kind="full_game", path="/tmp/s.mp4", duration_seconds=310.0,
        anchors=(SyncAnchor(video_seconds=300.0, wall_clock_at=T0),),
    )
    report = matcher().match_game([play(1, 8)], [short])
    c = report.candidates[0]
    assert c.source_end_seconds <= 310.0
