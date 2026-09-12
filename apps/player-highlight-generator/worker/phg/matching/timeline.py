"""Map game wall-clock time onto video file time.

This is the primary matching mechanism. Everything else - roster, batting
order, jersey digits - only decides *which player* a play belongs to. This
module decides *where in the footage* the play is.

Three levels of information, in descending order of accuracy:

  2+ sync anchors  a least-squares fit that also corrects clock drift between
                   the scorekeeper's phone and the camera
  1 sync anchor    a fixed offset; drift accumulates with distance
  0 anchors        the container's recording start timestamp only

A coach sets an anchor by scrubbing to a play in the review screen and
pressing "this is it". One anchor near the first inning and one near the last
is enough to hold a three-hour recording within a couple of seconds.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from phg.models import MediaAsset, SyncAnchor


class TimelineError(ValueError):
    """Raised when a media asset carries no usable time reference at all."""


@dataclass(frozen=True)
class Projection:
    """Where a wall-clock instant lands in the video, and how sure we are."""

    video_seconds: float
    uncertainty_seconds: float
    anchor_count: int
    drift_ppm: float = 0.0          # parts per million of clock skew corrected

    @property
    def window(self) -> tuple[float, float]:
        return (
            self.video_seconds - self.uncertainty_seconds,
            self.video_seconds + self.uncertainty_seconds,
        )


class Timeline:
    """A fitted wall-clock-to-video-time mapping for one media asset."""

    def __init__(
        self,
        asset: MediaAsset,
        *,
        base_window_seconds: float = 25.0,
        drift_seconds_per_minute: float = 0.35,
    ) -> None:
        self.asset = asset
        self.base_window = base_window_seconds
        self.drift_per_minute = drift_seconds_per_minute
        self._anchors: list[SyncAnchor] = sorted(asset.anchors, key=lambda a: a.video_seconds)

        if not self._anchors and asset.recording_started_at is None:
            raise TimelineError(
                f"media asset {asset.id} has neither a sync anchor nor a recording start time; "
                "ask the coach to set one anchor in the review screen"
            )

        self._slope, self._intercept, self._epoch = self._fit()

    # -- fitting ----------------------------------------------------------

    def _fit(self) -> tuple[float, float, datetime]:
        """Return (slope, intercept, epoch) for video_t = slope*dt + intercept."""
        if len(self._anchors) >= 2:
            epoch = self._anchors[0].wall_clock_at
            xs = [(a.wall_clock_at - epoch).total_seconds() for a in self._anchors]
            ys = [a.video_seconds for a in self._anchors]
            n = len(xs)
            mean_x = sum(xs) / n
            mean_y = sum(ys) / n
            denom = sum((x - mean_x) ** 2 for x in xs)
            if denom == 0:
                # All anchors share a wall-clock instant; fall back to offset only.
                return 1.0, mean_y, epoch
            slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / denom
            # A camera clock that disagrees by more than 2% is a data-entry
            # error, not drift. Refuse the fit rather than warp the whole game.
            if not 0.98 <= slope <= 1.02:
                slope = 1.0
            intercept = mean_y - slope * mean_x
            return slope, intercept, epoch

        if len(self._anchors) == 1:
            a = self._anchors[0]
            return 1.0, a.video_seconds, a.wall_clock_at

        started = self.asset.recording_started_at
        assert started is not None  # guarded in __init__
        return 1.0, 0.0, started

    # -- projection -------------------------------------------------------

    def project(self, wall_clock: datetime) -> Projection:
        """Project a wall-clock instant into video time with an error bar."""
        dt = (wall_clock - self._epoch).total_seconds()
        video_seconds = self._slope * dt + self._intercept
        return Projection(
            video_seconds=video_seconds,
            uncertainty_seconds=self._uncertainty(video_seconds),
            anchor_count=len(self._anchors),
            drift_ppm=(self._slope - 1.0) * 1_000_000,
        )

    def _uncertainty(self, video_seconds: float) -> float:
        """Error bar grows with distance from the nearest anchor."""
        if not self._anchors:
            # No anchor at all: trust only the container timestamp, which on
            # phone recordings is routinely a minute off.
            return self.base_window + 60.0

        nearest = min(abs(video_seconds - a.video_seconds) for a in self._anchors)
        # Two anchors that bracket this moment means we interpolated rather
        # than extrapolated, which is materially tighter.
        bracketed = (
            len(self._anchors) >= 2
            and self._anchors[0].video_seconds <= video_seconds <= self._anchors[-1].video_seconds
        )
        drift = (nearest / 60.0) * self.drift_per_minute
        if bracketed:
            drift *= 0.4
        return self.base_window + drift

    def clamp(self, start: float, end: float) -> tuple[float, float]:
        """Clamp a window to the bounds of the actual file."""
        duration = self.asset.duration_seconds
        start = max(0.0, min(start, duration))
        end = max(0.0, min(end, duration))
        if end <= start:
            end = min(duration, start + 1.0)
        return start, end

    @property
    def anchor_count(self) -> int:
        return len(self._anchors)
