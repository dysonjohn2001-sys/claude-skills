from phg.models import ClipCandidate, Play
from phg.ranking import RankInputs, score_clip, select_for_reel


def play(**kw):
    args = dict(
        id="p1", game_id="g1", sequence_no=1, inning=3, half="top",
        play_type="single", description="", is_our_offense=True,
    )
    args.update(kw)
    return Play(**args)


def clip(pid="p1", player="pl1", category="offense", start=0.0, end=13.0, conf=0.9):
    return ClipCandidate(
        play_id=pid, player_id=player, media_asset_id="m1", category=category,
        source_start_seconds=start, source_end_seconds=end,
        pre_roll_seconds=5.0, post_roll_seconds=8.0,
        match_method="schedule", match_confidence=conf,
    )


def rank(play_obj, role="batter", category="offense", **kw):
    c = clip(category=category)
    score_clip(c, RankInputs(play=play_obj, role=role, category=category, **kw))
    return c.rank_score


def test_bigger_hits_rank_higher():
    hr = rank(play(play_type="home_run", rbi=3))
    double = rank(play(play_type="double", rbi=1))
    single = rank(play(play_type="single"))
    assert hr > double > single


def test_strikeout_is_a_highlight_for_the_pitcher_and_not_the_batter():
    for_pitcher = rank(play(play_type="strikeout", is_our_offense=False),
                       role="pitcher", category="pitching")
    for_batter = rank(play(play_type="strikeout"))
    assert for_pitcher > for_batter * 3


def test_late_and_close_outranks_early_and_lopsided():
    late = rank(play(play_type="single", inning=7, score_us=4, score_them=4,
                     leverage_tag="tying_run"), total_innings=7)
    early = rank(play(play_type="single", inning=1, score_us=9, score_them=0), total_innings=7)
    assert late > early


def test_errors_are_suppressed_but_not_zeroed():
    score = rank(play(play_type="groundout", is_our_offense=False),
                 role="fielder_error", category="defense")
    assert 0 < score < 15


def test_rank_factors_are_recorded_for_the_review_screen():
    c = clip()
    score_clip(c, RankInputs(play=play(play_type="double"), role="batter", category="offense"))
    assert set(c.rank_factors) == {
        "play_merit", "leverage", "production", "action_density", "confidence"
    }


def test_selection_respects_the_duration_cap():
    clips = [clip(pid=f"p{i}", start=i * 20.0, end=i * 20.0 + 13.0) for i in range(20)]
    for c in clips:
        c.rank_score = 50.0
    chosen = select_for_reel(clips, max_clips=20, max_duration_seconds=60.0)
    assert sum(c.duration for c in chosen) <= 60.0


def test_selection_covers_every_category_a_player_appeared_in():
    clips = []
    for i, category in enumerate(["offense", "offense", "offense", "pitching", "defense"]):
        c = clip(pid=f"p{i}", category=category, start=i * 20.0, end=i * 20.0 + 13.0)
        c.rank_score = 90.0 if category == "offense" else 10.0
        clips.append(c)
    chosen = select_for_reel(clips, max_clips=4, max_duration_seconds=300.0)
    assert {c.category for c in chosen} >= {"offense", "pitching", "defense"}


def test_low_confidence_clips_are_excluded_from_reels():
    good, bad = clip(pid="a", conf=0.9), clip(pid="b", conf=0.2)
    good.rank_score = bad.rank_score = 80.0
    chosen = select_for_reel([good, bad], min_confidence=0.45)
    assert [c.play_id for c in chosen] == ["a"]


def test_selection_returns_chronological_order():
    clips = [clip(pid=f"p{i}", start=(5 - i) * 100.0, end=(5 - i) * 100.0 + 13.0) for i in range(5)]
    for i, c in enumerate(clips):
        c.rank_score = float(i * 10)
    chosen = select_for_reel(clips, max_clips=5, max_duration_seconds=300.0)
    starts = [c.source_start_seconds for c in chosen]
    assert starts == sorted(starts)
