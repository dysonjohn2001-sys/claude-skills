"""Dead-time detection with OpenCV.

Youth baseball is mostly standing around. A 13-second window cut around a
scored play still contains the batter adjusting a glove and the umpire dusting
the plate. This module finds the part where something moves and reports the
rest as trimmable.

It is intentionally conservative. It returns segments with a `keep` flag rather
than cutting anything, it never trims a clip below a floor, and it always
preserves a lead-in before the first motion so the viewer sees the pitch, not
just the swing.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import cv2
import numpy as np

from phg.models import Segment

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeadTimeSettings:
    sample_fps: float = 6.0
    motion_threshold: float = 0.015     # fraction of pixels changed
    pixel_delta: int = 22               # per-pixel intensity delta that counts as change
    smooth_window: int = 5              # samples in the moving average
    min_kept_seconds: float = 4.0
    lead_in_seconds: float = 1.5        # always keep this much before first motion
    tail_out_seconds: float = 1.0
    analysis_width: int = 320           # downscale before differencing


@dataclass
class MotionProfile:
    times: list[float]                  # seconds, relative to window start
    values: list[float]                 # smoothed 0..1 motion fraction
    settings: DeadTimeSettings

    @property
    def density(self) -> float:
        """Mean motion, normalised against the threshold. Feeds clip ranking."""
        if not self.values:
            return 0.5
        mean = float(np.mean(self.values))
        return float(min(1.0, mean / max(1e-6, self.settings.motion_threshold * 2.0)))

    @property
    def peak_time(self) -> float:
        if not self.values:
            return 0.0
        return self.times[int(np.argmax(self.values))]


def profile_window(
    video_path: str,
    start_seconds: float,
    end_seconds: float,
    settings: DeadTimeSettings | None = None,
) -> MotionProfile:
    """Sample the window and return a smoothed motion-over-time series."""
    s = settings or DeadTimeSettings()
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        log.error("could not open %s for motion analysis", video_path)
        return MotionProfile([], [], s)

    try:
        times, raw = _sample(cap, start_seconds, end_seconds, s)
    finally:
        cap.release()

    return MotionProfile(times, _smooth(raw, s.smooth_window), s)


def _sample(cap, start: float, end: float, s: DeadTimeSettings) -> tuple[list[float], list[float]]:
    step = 1.0 / max(0.5, s.sample_fps)
    times: list[float] = []
    values: list[float] = []
    previous: np.ndarray | None = None

    t = start
    while t < end:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000.0)
        ok, frame = cap.read()
        if not ok or frame is None:
            break
        gray = _prepare(frame, s.analysis_width)
        if previous is not None:
            delta = cv2.absdiff(previous, gray)
            changed = np.count_nonzero(delta > s.pixel_delta)
            values.append(changed / float(delta.size))
            times.append(round(t - start, 3))
        previous = gray
        t += step

    return times, values


def _prepare(frame: np.ndarray, width: int) -> np.ndarray:
    scale = width / max(1, frame.shape[1])
    if scale < 1.0:
        frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Blur first, or camera shake and grass texture read as action.
    return cv2.GaussianBlur(gray, (5, 5), 0)


def _smooth(values: list[float], window: int) -> list[float]:
    if not values or window <= 1:
        return values
    kernel = np.ones(window) / window
    padded = np.pad(np.asarray(values, dtype=float), (window // 2, window // 2), mode="edge")
    return list(np.convolve(padded, kernel, mode="valid")[: len(values)])


def segments_for(profile: MotionProfile, clip_duration: float) -> list[Segment]:
    """Split a clip into keep/drop segments based on its motion profile."""
    s = profile.settings
    if not profile.values:
        return [Segment(0.0, clip_duration, keep=True, reason="no motion data; kept whole")]

    above = [v >= s.motion_threshold for v in profile.values]
    if not any(above):
        # Nothing crossed the bar. Keep the middle rather than dropping the clip:
        # a quiet frame is more often a distant camera than a dead play.
        mid = clip_duration / 2.0
        half = max(s.min_kept_seconds, clip_duration * 0.6) / 2.0
        return _bracket(max(0.0, mid - half), min(clip_duration, mid + half), clip_duration,
                        "motion below threshold; kept centre window")

    first = profile.times[above.index(True)]
    last = profile.times[len(above) - 1 - above[::-1].index(True)]

    keep_start = max(0.0, first - s.lead_in_seconds)
    keep_end = min(clip_duration, last + s.tail_out_seconds)

    # Enforce the floor by growing symmetrically around the action.
    if keep_end - keep_start < s.min_kept_seconds:
        grow = (s.min_kept_seconds - (keep_end - keep_start)) / 2.0
        keep_start = max(0.0, keep_start - grow)
        keep_end = min(clip_duration, keep_end + grow)

    return _bracket(keep_start, keep_end, clip_duration, "action window")


def _bracket(keep_start: float, keep_end: float, duration: float, reason: str) -> list[Segment]:
    out: list[Segment] = []
    if keep_start > 0.05:
        out.append(Segment(0.0, round(keep_start, 3), keep=False, reason="pre-action dead time"))
    out.append(Segment(round(keep_start, 3), round(keep_end, 3), keep=True, reason=reason))
    if duration - keep_end > 0.05:
        out.append(Segment(round(keep_end, 3), round(duration, 3), keep=False, reason="post-action dead time"))
    return out


def kept_spans(segments: list[Segment]) -> list[tuple[float, float]]:
    return [(s.start, s.end) for s in segments if s.keep]
