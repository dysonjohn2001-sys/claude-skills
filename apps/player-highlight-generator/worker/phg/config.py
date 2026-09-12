"""Runtime configuration, read once from the environment."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


def _f(name: str, default: float) -> float:
    return float(os.environ.get(name, default))


def _i(name: str, default: int) -> int:
    return int(os.environ.get(name, default))


def _b(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class MatchingConfig:
    """Tunables for play-to-video and play-to-player matching."""

    # How far either side of the projected play instant we are still willing to
    # believe the play happened. Widens automatically when the sync anchor is
    # old (see timeline.projected_window).
    base_search_window_seconds: float = field(default_factory=lambda: _f("PHG_SEARCH_WINDOW", 25.0))
    # Extra slack added per minute of distance from the nearest sync anchor.
    drift_seconds_per_minute: float = field(default_factory=lambda: _f("PHG_DRIFT_PER_MIN", 0.35))

    auto_approve_threshold: float = field(default_factory=lambda: _f("PHG_AUTO_APPROVE", 0.80))
    review_floor_threshold: float = field(default_factory=lambda: _f("PHG_REVIEW_FLOOR", 0.45))

    # Jersey OCR is a tiebreaker, never a primary signal. It only runs when the
    # schedule-based confidence lands inside this band.
    jersey_band_low: float = field(default_factory=lambda: _f("PHG_JERSEY_BAND_LOW", 0.45))
    jersey_band_high: float = field(default_factory=lambda: _f("PHG_JERSEY_BAND_HIGH", 0.85))
    jersey_enabled: bool = field(default_factory=lambda: _b("PHG_JERSEY_ENABLED", True))
    # Ceiling on how much a jersey read can move confidence in either direction.
    jersey_max_adjustment: float = field(default_factory=lambda: _f("PHG_JERSEY_MAX_ADJ", 0.18))


@dataclass(frozen=True)
class VideoConfig:
    pre_roll_seconds: float = field(default_factory=lambda: _f("PHG_PRE_ROLL", 5.0))
    post_roll_seconds: float = field(default_factory=lambda: _f("PHG_POST_ROLL", 8.0))

    dead_time_removal: bool = field(default_factory=lambda: _b("PHG_DEAD_TIME", True))
    motion_threshold: float = field(default_factory=lambda: _f("PHG_MOTION_THRESHOLD", 0.015))
    motion_sample_fps: float = field(default_factory=lambda: _f("PHG_MOTION_SAMPLE_FPS", 6.0))
    # Never trim a clip below this, however quiet the frame looks.
    min_kept_seconds: float = field(default_factory=lambda: _f("PHG_MIN_KEPT", 4.0))

    render_crf: int = field(default_factory=lambda: _i("PHG_CRF", 20))
    render_preset: str = field(default_factory=lambda: os.environ.get("PHG_PRESET", "medium"))
    audio_bitrate: str = field(default_factory=lambda: os.environ.get("PHG_AUDIO_BITRATE", "192k"))
    music_volume_db: float = field(default_factory=lambda: _f("PHG_MUSIC_DB", -18.0))
    duck_music_db: float = field(default_factory=lambda: _f("PHG_DUCK_DB", -8.0))

    ffmpeg: str = field(default_factory=lambda: os.environ.get("PHG_FFMPEG", "ffmpeg"))
    ffprobe: str = field(default_factory=lambda: os.environ.get("PHG_FFPROBE", "ffprobe"))


@dataclass(frozen=True)
class Config:
    database_url: str = field(default_factory=lambda: os.environ.get("DATABASE_URL", ""))
    media_root: Path = field(default_factory=lambda: Path(os.environ.get("PHG_MEDIA_ROOT", "/var/lib/phg/media")))
    work_root: Path = field(default_factory=lambda: Path(os.environ.get("PHG_WORK_ROOT", "/tmp/phg-work")))
    worker_name: str = field(default_factory=lambda: os.environ.get("PHG_WORKER_NAME", "worker-1"))
    poll_interval_seconds: float = field(default_factory=lambda: _f("PHG_POLL_INTERVAL", 3.0))
    matching: MatchingConfig = field(default_factory=MatchingConfig)
    video: VideoConfig = field(default_factory=VideoConfig)


def load() -> Config:
    return Config()
