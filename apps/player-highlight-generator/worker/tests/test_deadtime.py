"""Dead-time detection against footage shaped like the real thing.

Every case here comes from a defect found by running an actual exported
GameChanger home-run clip through the pipeline. The synthetic sources reproduce
that clip's shape - a static title card, a hard cut, then a locked-off wide shot
where the players are a few dozen pixels tall - because the 17 MB original does
not belong in a repository.

Measured on the real clip, for reference:

    title card      0.00000 motion, 0.0s - 4.0s
    cut to footage  0.93432 in one frame, 405x the median
    play            median 0.00231, p90 0.00729, max 0.01304

The shipped absolute threshold of 0.015 matched none of the 113 footage samples.
"""

from __future__ import annotations

import shutil
import subprocess

import pytest

from phg.video.deadtime import (
    DeadTimeSettings,
    kept_spans,
    profile_window,
    segments_for,
)

pytestmark = pytest.mark.skipif(
    shutil.which("ffmpeg") is None, reason="ffmpeg is required"
)


def _build(path, parts: list[str], fps: int = 30) -> str:
    """Concatenate lavfi sources into one clip."""
    inputs: list[str] = []
    for part in parts:
        inputs += ["-f", "lavfi", "-i", part]
    n = len(parts)
    graph = "".join(f"[{i}:v]scale=960:540,fps={fps},setsar=1[v{i}];" for i in range(n))
    graph += "".join(f"[v{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=0[out]"
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs,
         "-filter_complex", graph, "-map", "[out]",
         "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", str(path)],
        capture_output=True, check=True,
    )
    return str(path)


# A locked-off wide shot: a still field with one small thing moving on it, which
# is what a distant baserunner looks like to a frame differencer.
WIDE_SHOT = (
    "color=c=0x3A7D2C:s=960x540:d={d},"
    "drawbox=x='100+mod(t*40\\,700)':y=260:w=14:h=26:color=white@1:t=fill"
)
TITLE_CARD = "color=c=black:s=960x540:d={d}"
BUSY = "testsrc2=size=960x540:rate=30:duration={d}"


@pytest.fixture(scope="module")
def exported_clip(tmp_path_factory) -> str:
    """A 4s title card, a hard cut, then 16s of low-motion wide shot."""
    return _build(
        tmp_path_factory.mktemp("dt") / "exported.mp4",
        [TITLE_CARD.format(d=4), WIDE_SHOT.format(d=16)],
    )


@pytest.fixture(scope="module")
def one_play(tmp_path_factory) -> str:
    """A quiet run, a burst, a quiet run: the shape of a window around one play."""
    return _build(
        tmp_path_factory.mktemp("dt") / "oneplay.mp4",
        [WIDE_SHOT.format(d=5), BUSY.format(d=4), WIDE_SHOT.format(d=6)],
    )


# --- title card and scene cuts -------------------------------------------


def test_title_card_is_detected_as_a_leader(exported_clip):
    profile = profile_window(exported_clip, 0.0, 20.0)
    assert profile.leader_ends == pytest.approx(4.0, abs=0.4)


def test_the_cut_into_footage_is_detected_as_a_cut(exported_clip):
    profile = profile_window(exported_clip, 0.0, 20.0)
    assert profile.cuts, "the cut from title card to footage was missed"
    assert profile.cuts[0] == pytest.approx(4.0, abs=0.4)


def test_the_title_card_is_dropped_and_the_play_is_kept(exported_clip):
    """The first version kept 1.75-5.75s: almost entirely the title card."""
    profile = profile_window(exported_clip, 0.0, 20.0)
    segments = segments_for(profile, 20.0)

    dropped_leader = [s for s in segments if not s.keep and s.reason == "title card or leader"]
    assert dropped_leader, "the title card was not dropped"
    assert dropped_leader[0].end == pytest.approx(4.0, abs=0.4)

    spans = kept_spans(segments)
    assert spans, "everything was dropped"
    assert spans[0][0] >= 3.6, "the kept window reaches back into the title card"
    # Most of the footage survives; a home run is action end to end.
    assert sum(e - s for s, e in spans) > 12.0


def test_a_scene_cut_is_not_mistaken_for_the_action_peak(exported_clip):
    """The cut changes 93% of pixels. Reading that as the peak put slow motion
    on the title card transition."""
    profile = profile_window(exported_clip, 0.0, 20.0)
    assert profile.peak_time > profile.leader_ends


# --- adaptive threshold ---------------------------------------------------


def test_threshold_adapts_to_a_low_motion_wide_shot(exported_clip):
    """A fixed 0.015 matched none of the real clip's 113 footage samples."""
    profile = profile_window(exported_clip, 0.0, 20.0)
    assert profile.threshold < 0.015
    assert profile.threshold >= DeadTimeSettings().min_absolute_threshold


def test_absolute_threshold_is_used_when_adaptive_is_switched_off(exported_clip):
    settings = DeadTimeSettings(adaptive_threshold=False, motion_threshold=0.02)
    profile = profile_window(exported_clip, 0.0, 20.0, settings)
    assert profile.threshold == 0.02


# --- edge trimming --------------------------------------------------------


def test_quiet_edges_are_trimmed_around_a_single_play(one_play):
    profile = profile_window(one_play, 0.0, 15.0)
    spans = kept_spans(segments_for(profile, 15.0))
    assert spans
    start, end = spans[0][0], spans[-1][1]
    # The burst runs 5-9s; the lead-in and tail-out widen that a little.
    assert start < 5.5
    assert end < 13.0, "the quiet tail was not trimmed"


def test_a_clip_is_never_trimmed_below_the_floor(one_play):
    settings = DeadTimeSettings(min_kept_seconds=8.0)
    profile = profile_window(one_play, 0.0, 15.0, settings)
    spans = kept_spans(segments_for(profile, 15.0))
    assert sum(e - s for s, e in spans) >= 7.9


def test_a_fraction_of_a_second_at_an_edge_is_not_worth_trimming(one_play):
    settings = DeadTimeSettings(min_trim_seconds=30.0)
    profile = profile_window(one_play, 0.0, 15.0, settings)
    spans = kept_spans(segments_for(profile, 15.0))
    assert spans[0][0] == pytest.approx(profile.leader_ends, abs=0.01)
    assert spans[-1][1] == pytest.approx(15.0, abs=0.01)


def test_segments_tile_the_clip_without_gaps(exported_clip):
    segments = segments_for(profile_window(exported_clip, 0.0, 20.0), 20.0)
    assert segments[0].start == 0.0
    assert segments[-1].end == pytest.approx(20.0, abs=0.01)
    for earlier, later in zip(segments, segments[1:]):
        assert earlier.end == pytest.approx(later.start, abs=0.001)


def test_leader_and_quiet_footage_are_labelled_differently(exported_clip):
    """A coach reading the review screen should be able to tell a dropped title
    card from a dropped quiet stretch of real play."""
    reasons = {s.reason for s in segments_for(profile_window(exported_clip, 0.0, 20.0), 20.0)}
    assert "title card or leader" in reasons


def test_unreadable_video_keeps_the_whole_clip():
    profile = profile_window("/nonexistent/file.mp4", 0.0, 10.0)
    segments = segments_for(profile, 10.0)
    assert len(segments) == 1
    assert segments[0].keep
    assert segments[0].start == 0.0 and segments[0].end == 10.0


def test_density_and_peak_ignore_the_leader_and_the_cut(exported_clip):
    profile = profile_window(exported_clip, 0.0, 20.0)
    assert 0.0 <= profile.density <= 1.0
    assert profile.peak_time >= profile.leader_ends
