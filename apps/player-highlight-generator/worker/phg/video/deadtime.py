"""Dead-time detection with OpenCV.

Youth baseball is mostly standing around. A 13-second window cut around a
scored play still contains the batter adjusting a glove and the umpire dusting
the plate. This module finds the part where something moves and reports the
rest as trimmable.

Three things about real footage shaped this design, each of which broke an
earlier absolute-threshold version when it met an actual exported clip:

  Fixed wide shots barely move. A 10U field shot from behind the backstop puts
  the players thirty metres away and a few dozen pixels tall. On a real home-run
  clip the motion never exceeded 0.013 and the median was 0.0023, so a fixed
  0.015 threshold matched nothing at all. The threshold is therefore derived
  from each clip's own distribution, with an absolute floor only as a backstop.

  Scene cuts look like enormous motion. The same clip opened with a title card
  and cut to footage at 4.0s, changing 93% of the pixels in one frame - 405x the
  median. An earlier version read that cut as the action peak and kept the title
  card. Cuts are now detected and excluded rather than counted.

  Exported clips carry leaders. A run of near-zero motion before the first cut
  is a static graphic, not a quiet moment on the field, and it is dropped.

The module stays conservative: it returns keep/drop segments rather than cutting
anything, never trims below a floor, and keeps a lead-in before the first motion
so the viewer sees the pitch and not just the swing.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

import cv2
import numpy as np

from phg.models import Segment

log = logging.getLogger(__name__)


@dataclass(frozen=True)
class DeadTimeSettings:
    sample_fps: float = 6.0
    pixel_delta: int = 22               # per-pixel intensity delta that counts as change
    smooth_window: int = 5              # samples in the moving average
    min_kept_seconds: float = 4.0
    lead_in_seconds: float = 1.5        # always keep this much before first motion
    tail_out_seconds: float = 1.0
    analysis_width: int = 320           # downscale before differencing

    # The trim asks "is this edge quiet compared to the rest of this clip?",
    # not "what counts as action?". Anything at or below the 25th percentile of
    # the clip's own motion is among its quietest quarter and is a candidate for
    # trimming, but only at the head and tail. This is scale-free: it behaves
    # the same on a locked-off wide shot where nothing exceeds 0.013 and on
    # handheld footage that routinely exceeds 0.1.
    adaptive_threshold: bool = True
    quiet_percentile: float = 25.0
    min_absolute_threshold: float = 0.0012
    # Fallback when adaptive is off. Suits close or panned footage; it is far
    # too high for a fixed wide shot, where real play never reaches it.
    motion_threshold: float = 0.015
    # Do not bother re-encoding to save less than this at an edge.
    min_trim_seconds: float = 0.75

    # A sample this many times the median, or this fraction of the frame
    # outright, is a scene cut rather than action.
    scene_cut_ratio: float = 20.0
    scene_cut_absolute: float = 0.25
    # A leader is a run of frames this still. Real footage never is.
    leader_max_motion: float = 0.0006


@dataclass
class MotionProfile:
    times: list[float]                  # seconds, relative to window start
    values: list[float]                 # smoothed 0..1 motion fraction
    settings: DeadTimeSettings
    raw: list[float] = field(default_factory=list)      # unsmoothed
    cuts: list[float] = field(default_factory=list)     # times of scene cuts
    leader_ends: float = 0.0            # end of a static title card, if any

    @property
    def threshold(self) -> float:
        """Motion at or below this is quiet for this particular clip."""
        s = self.settings
        body = self._body()
        if not s.adaptive_threshold or len(body) < 8:
            return s.motion_threshold
        return max(s.min_absolute_threshold, float(np.percentile(body, s.quiet_percentile)))

    def _body(self) -> list[float]:
        """Samples that are neither leader nor scene cut."""
        cut_times = set(self.cuts)
        return [
            v
            for t, v in zip(self.times, self.raw or self.values)
            if t >= self.leader_ends and t not in cut_times
        ]

    @property
    def density(self) -> float:
        """Mean motion, normalised against the threshold. Feeds clip ranking."""
        body = self._body()
        if not body:
            return 0.5
        # The threshold marks the clip's quiet floor, so scale against a
        # multiple of it to keep density comparable across clips.
        return float(min(1.0, float(np.mean(body)) / max(1e-6, self.threshold * 4.0)))

    @property
    def peak_time(self) -> float:
        """Busiest moment, ignoring leaders and cuts. Feeds slow-motion picking."""
        candidates = [
            (v, t)
            for t, v in zip(self.times, self.values)
            if t >= self.leader_ends and t not in set(self.cuts)
        ]
        if not candidates:
            return 0.0
        return max(candidates)[1]


def profile_window(
    video_path: str,
    start_seconds: float,
    end_seconds: float,
    settings: DeadTimeSettings | None = None,
) -> MotionProfile:
    """Sample the window and return a motion series with cuts and leader marked."""
    s = settings or DeadTimeSettings()
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        log.error("could not open %s for motion analysis", video_path)
        return MotionProfile([], [], s)

    try:
        times, raw = _sample(cap, start_seconds, end_seconds, s)
    finally:
        cap.release()

    if not raw:
        return MotionProfile([], [], s)

    cuts = _detect_cuts(times, raw, s)
    leader_ends = _detect_leader(times, raw, cuts, s)

    # Smooth with cut spikes removed, or the moving average smears a 0.93 frame
    # difference across a second either side of the cut.
    damped = _damp_cuts(times, raw, cuts)
    return MotionProfile(
        times=times,
        values=_smooth(damped, s.smooth_window),
        settings=s,
        raw=raw,
        cuts=cuts,
        leader_ends=leader_ends,
    )


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


def _detect_cuts(times: list[float], raw: list[float], s: DeadTimeSettings) -> list[float]:
    """Find hard scene changes, which are discontinuities rather than motion."""
    if len(raw) < 4:
        return []
    positive = [v for v in raw if v > 0]
    median = float(np.median(positive)) if positive else 0.0
    ratio_level = median * s.scene_cut_ratio if median > 0 else s.scene_cut_absolute
    level = min(s.scene_cut_absolute, max(ratio_level, s.min_absolute_threshold * 10))
    return [t for t, v in zip(times, raw) if v >= level]


def _detect_leader(
    times: list[float], raw: list[float], cuts: list[float], s: DeadTimeSettings
) -> float:
    """Return the end of an opening static graphic, or 0.0 if there is none.

    An exported highlight often opens with a title card: perfectly still frames,
    then a hard cut into the footage. Real footage is never perfectly still, so
    near-zero motion right up to a cut identifies the card unambiguously.
    """
    if not cuts:
        return 0.0
    first_cut = cuts[0]
    before = [v for t, v in zip(times, raw) if t < first_cut]
    if len(before) < 3:
        return 0.0
    if max(before) > s.leader_max_motion:
        return 0.0
    # Do not swallow most of a clip on the strength of a mid-clip cut.
    if first_cut > times[-1] * 0.5:
        return 0.0
    return first_cut


def _damp_cuts(times: list[float], raw: list[float], cuts: list[float]) -> list[float]:
    if not cuts:
        return raw
    cut_set = set(cuts)
    out = list(raw)
    for i, t in enumerate(times):
        if t not in cut_set:
            continue
        neighbours = [
            raw[j] for j in (i - 2, i - 1, i + 1, i + 2)
            if 0 <= j < len(raw) and times[j] not in cut_set
        ]
        out[i] = float(np.median(neighbours)) if neighbours else 0.0
    return out


def _smooth(values: list[float], window: int) -> list[float]:
    if not values or window <= 1:
        return values
    kernel = np.ones(window) / window
    padded = np.pad(np.asarray(values, dtype=float), (window // 2, window // 2), mode="edge")
    return list(np.convolve(padded, kernel, mode="valid")[: len(values)])


def segments_for(profile: MotionProfile, clip_duration: float) -> list[Segment]:
    """Split a clip into keep/drop segments based on its motion profile.

    Trims quiet runs from the head and tail only. It does not try to excerpt
    action from the middle: a clip cut around one play is a continuous event,
    and cutting holes in it produces something that reads as broken rather than
    tight.
    """
    s = profile.settings
    if not profile.values:
        return [Segment(0.0, clip_duration, keep=True, reason="no motion data; kept whole")]

    leader = profile.leader_ends
    threshold = profile.threshold
    body = [(t, v) for t, v in zip(profile.times, profile.values) if t >= leader]

    if not body:
        return _assemble(leader, clip_duration, clip_duration, "kept whole", leader)

    active = [t for t, v in body if v >= threshold]
    if not active:
        # Everything is equally quiet. Keep it all rather than guessing: a still
        # frame is more often a distant camera than a dead play.
        return _assemble(leader, clip_duration, clip_duration,
                         "no quiet edges to trim", leader)

    keep_start = max(leader, active[0] - s.lead_in_seconds)
    keep_end = min(clip_duration, active[-1] + s.tail_out_seconds)

    # Not worth a re-encode to shave a fraction of a second off an edge.
    if keep_start - leader < s.min_trim_seconds:
        keep_start = leader
    if clip_duration - keep_end < s.min_trim_seconds:
        keep_end = clip_duration

    # Enforce the minimum length by growing around the action, never back into
    # the leader.
    if keep_end - keep_start < s.min_kept_seconds:
        grow = (s.min_kept_seconds - (keep_end - keep_start)) / 2.0
        keep_start = max(leader, keep_start - grow)
        keep_end = min(clip_duration, keep_end + grow)
        if keep_end - keep_start < s.min_kept_seconds:
            keep_end = min(clip_duration, keep_start + s.min_kept_seconds)

    return _assemble(keep_start, keep_end, clip_duration, "action window", leader)


def _assemble(
    keep_start: float, keep_end: float, duration: float, reason: str, leader: float
) -> list[Segment]:
    """Build the segment list, keeping the leader distinct from quiet footage.

    A title card and a quiet stretch of real play are both dropped, but a coach
    reading the review screen should be able to tell which was which.
    """
    out: list[Segment] = []
    if leader > 0.05:
        out.append(Segment(0.0, round(leader, 3), keep=False, reason="title card or leader"))
    if keep_start - leader > 0.05:
        out.append(
            Segment(round(leader, 3), round(keep_start, 3), keep=False, reason="pre-action dead time")
        )
    out.append(Segment(round(keep_start, 3), round(keep_end, 3), keep=True, reason=reason))
    if duration - keep_end > 0.05:
        out.append(
            Segment(round(keep_end, 3), round(duration, 3), keep=False, reason="post-action dead time")
        )
    return out


def kept_spans(segments: list[Segment]) -> list[tuple[float, float]]:
    return [(s.start, s.end) for s in segments if s.keep]
