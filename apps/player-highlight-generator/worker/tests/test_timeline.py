from datetime import datetime, timedelta, timezone

import pytest

from phg.matching.timeline import Timeline, TimelineError
from phg.models import MediaAsset, SyncAnchor

T0 = datetime(2026, 4, 18, 10, 0, 0, tzinfo=timezone.utc)


def asset(**kwargs) -> MediaAsset:
    base = dict(
        id="m1", game_id="g1", kind="full_game", path="/tmp/x.mp4",
        duration_seconds=7200.0,
    )
    base.update(kwargs)
    return MediaAsset(**base)


def test_requires_some_time_reference():
    with pytest.raises(TimelineError):
        Timeline(asset())


def test_container_timestamp_only_is_wide():
    tl = Timeline(asset(recording_started_at=T0))
    p = tl.project(T0 + timedelta(minutes=30))
    assert p.video_seconds == pytest.approx(1800.0)
    # No anchor means the error bar must be wide enough to be honest about it.
    assert p.uncertainty_seconds > 60


def test_single_anchor_offsets_the_clock():
    # Recording began 90s before the anchored play.
    tl = Timeline(asset(anchors=(SyncAnchor(video_seconds=90.0, wall_clock_at=T0),)))
    p = tl.project(T0 + timedelta(seconds=600))
    assert p.video_seconds == pytest.approx(690.0)
    assert p.anchor_count == 1


def test_two_anchors_correct_clock_drift():
    # Camera clock runs 1% slow: 3600 wall seconds cover 3564 video seconds.
    anchors = (
        SyncAnchor(video_seconds=0.0, wall_clock_at=T0),
        SyncAnchor(video_seconds=3564.0, wall_clock_at=T0 + timedelta(seconds=3600)),
    )
    tl = Timeline(asset(anchors=anchors))
    p = tl.project(T0 + timedelta(seconds=1800))
    assert p.video_seconds == pytest.approx(1782.0, abs=0.5)
    assert p.drift_ppm < 0


def test_implausible_drift_is_rejected_not_applied():
    # A 20% disagreement is a data-entry error, not drift.
    anchors = (
        SyncAnchor(video_seconds=0.0, wall_clock_at=T0),
        SyncAnchor(video_seconds=2880.0, wall_clock_at=T0 + timedelta(seconds=3600)),
    )
    tl = Timeline(asset(anchors=anchors))
    p = tl.project(T0 + timedelta(seconds=3600))
    # Slope pinned to 1.0, so the projection is the plain offset.
    assert p.drift_ppm == pytest.approx(0.0)


def test_interpolated_window_is_tighter_than_extrapolated():
    anchors = (
        SyncAnchor(video_seconds=60.0, wall_clock_at=T0),
        SyncAnchor(video_seconds=3660.0, wall_clock_at=T0 + timedelta(seconds=3600)),
    )
    tl = Timeline(asset(anchors=anchors))
    inside = tl.project(T0 + timedelta(seconds=1800))
    outside = tl.project(T0 + timedelta(seconds=5400))
    assert inside.uncertainty_seconds < outside.uncertainty_seconds


def test_clamp_keeps_windows_inside_the_file():
    tl = Timeline(asset(duration_seconds=100.0, recording_started_at=T0))
    assert tl.clamp(-20.0, 10.0) == (0.0, 10.0)
    assert tl.clamp(95.0, 130.0) == (95.0, 100.0)
