import pytest

from phg.video.clipper import ClipSpec, RenderError, SlowMotion, build_command
from phg.video.overlays import BrandTheme, ScoreboardState, escape_drawtext


def graph_of(args: list[str]) -> str:
    return args[args.index("-filter_complex") + 1]


def spec(**kw) -> ClipSpec:
    base = dict(
        source_path="/media/game.mp4",
        output_path="/media/clips/c1.mp4",
        spans=[(100.0, 113.0)],
    )
    base.update(kw)
    return ClipSpec(**base)


def test_empty_span_list_is_refused():
    with pytest.raises(RenderError):
        build_command(spec(spans=[]))


def test_single_span_trims_and_encodes_h264():
    args = build_command(spec())
    graph = graph_of(args)
    assert "trim=start=100.000:end=113.000" in graph
    assert "libx264" in args
    assert args[-1] == "/media/clips/c1.mp4"


def test_multiple_kept_spans_are_concatenated():
    args = build_command(spec(spans=[(100.0, 106.0), (109.0, 113.0)]))
    graph = graph_of(args)
    assert "concat=n=2:v=1:a=0" in graph
    assert "concat=n=2:v=0:a=1" in graph


def test_muted_source_gets_a_silent_track_rather_than_no_track():
    """Uniform stream layout is what lets the reel stage concatenate cleanly."""
    args = build_command(spec(mute_source=True))
    assert "-an" not in args
    assert "anullsrc=channel_layout=stereo:sample_rate=48000" in args
    assert "atrim" not in graph_of(args)


def test_output_is_scaled_and_padded_to_the_chosen_canvas():
    wide = graph_of(build_command(spec(aspect="16:9")))
    tall = graph_of(build_command(spec(aspect="9:16")))
    assert "scale=1920:1080" in wide and "pad=1920:1080" in wide
    assert "scale=1080:1920" in tall and "pad=1080:1920" in tall


def test_slow_motion_stretches_only_the_requested_section():
    args = build_command(spec(slowmo=SlowMotion(start=4.0, end=7.0, rate=0.5)))
    graph = graph_of(args)
    assert "setpts=2.0000*(PTS-STARTPTS)" in graph
    assert "concat=n=3:v=1:a=0" in graph
    assert "atempo=0.500" in graph


def test_slow_motion_overrunning_the_clip_is_clamped_not_dropped():
    """A window that runs a fraction past the end must still apply. Dropping it
    silently means the coach sets slow motion and nothing happens."""
    args = build_command(spec(spans=[(100.0, 113.0)], slowmo=SlowMotion(start=10.0, end=13.5, rate=0.5)))
    graph = graph_of(args)
    assert "concat=n=3:v=1:a=0" in graph
    assert "trim=start=10.000:end=13.000" in graph


def test_slow_motion_entirely_past_the_clip_is_refused():
    args = build_command(spec(spans=[(100.0, 113.0)], slowmo=SlowMotion(start=40.0, end=70.0, rate=0.5)))
    assert "concat=n=3:v=1:a=0" not in graph_of(args)


def test_slow_motion_too_short_to_see_is_refused():
    args = build_command(spec(slowmo=SlowMotion(start=4.0, end=4.2, rate=0.5)))
    assert "concat=n=3:v=1:a=0" not in graph_of(args)


def test_scorebug_and_lower_third_are_drawn_when_a_theme_is_present():
    theme = BrandTheme(team_name="Riverside Rays", primary_color="#0F2B5B",
                       secondary_color="#C8102E")
    board = ScoreboardState(
        us_label="RAY", them_label="OWL", score_us=4, score_them=3,
        inning=6, half="bottom", outs=2,
    )
    args = build_command(spec(theme=theme, scoreboard=board,
                              lower_third=("Jake Smith #7", "2-for-3, 2 RBI")))
    graph = graph_of(args)
    assert "drawtext" in graph and "drawbox" in graph
    assert "RAY 4" in graph
    assert "Jake Smith #7" in graph


def test_drawtext_escaping_handles_the_two_unescape_passes():
    """Only the backslash, the quote and the colon need handling. Escaping a
    comma or bracket would draw a visible backslash on the video."""
    assert escape_drawtext("2 RBI: Smith's double, big") == (
        r"2 RBI\: Smith'\\\''s double, big"
    )
    assert escape_drawtext(r"a\b") == r"a\\b"
    assert escape_drawtext("a, b; c [d] 100%") == "a, b; c [d] 100%"


def test_drawtext_disables_expansion_so_percent_signs_are_literal():
    theme = BrandTheme(team_name="Rays")
    args = build_command(spec(theme=theme, lower_third=("100% effort", "{not a token}")))
    assert graph_of(args).count("expansion=none") >= 2


def test_faststart_is_set_so_parents_can_stream_without_downloading():
    assert "+faststart" in build_command(spec())
