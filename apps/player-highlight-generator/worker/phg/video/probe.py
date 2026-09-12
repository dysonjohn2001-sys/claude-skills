"""Read technical metadata and the recording start time from a media file."""

from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone

from dateutil import parser as date_parser

log = logging.getLogger(__name__)

# Tags different cameras and phones use for "when recording started".
_CREATION_TAGS = (
    "creation_time",
    "com.apple.quicktime.creationdate",
    "date",
    "DateTimeOriginal",
)


class ProbeError(RuntimeError):
    pass


@dataclass(frozen=True)
class ProbeResult:
    duration_seconds: float
    width: int
    height: int
    fps: float
    has_audio: bool
    video_codec: str
    audio_codec: str | None
    recording_started_at: datetime | None
    byte_size: int | None

    @property
    def is_vertical(self) -> bool:
        return self.height > self.width


def _parse_fps(rate: str | None) -> float:
    if not rate or rate in {"0/0", "N/A"}:
        return 0.0
    if "/" in rate:
        num, _, den = rate.partition("/")
        try:
            d = float(den)
            return float(num) / d if d else 0.0
        except ValueError:
            return 0.0
    try:
        return float(rate)
    except ValueError:
        return 0.0


def _creation_time(container_tags: dict, stream_tags: dict) -> datetime | None:
    for tags in (container_tags, stream_tags):
        for key in _CREATION_TAGS:
            raw = tags.get(key)
            if not raw:
                continue
            try:
                parsed = date_parser.parse(raw)
            except (ValueError, TypeError, OverflowError):
                continue
            # A naive timestamp from a camera is local time at the field. The
            # caller re-interprets it in the team's timezone; storing it as UTC
            # here at least keeps it unambiguous downstream.
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed
    return None


def probe(path: str, ffprobe: str = "ffprobe") -> ProbeResult:
    cmd = [
        ffprobe, "-v", "error",
        "-print_format", "json",
        "-show_format", "-show_streams",
        path,
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=True)
    except FileNotFoundError as exc:
        raise ProbeError(f"ffprobe not found on PATH ({ffprobe})") from exc
    except subprocess.CalledProcessError as exc:
        raise ProbeError(f"ffprobe failed on {path}: {exc.stderr.strip()[:400]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise ProbeError(f"ffprobe timed out on {path}") from exc

    data = json.loads(out.stdout or "{}")
    fmt = data.get("format", {})
    streams = data.get("streams", [])

    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    if video is None:
        raise ProbeError(f"{path} contains no video stream")

    duration = float(fmt.get("duration") or video.get("duration") or 0.0)
    if duration <= 0:
        raise ProbeError(f"{path} reports a zero duration; the upload is probably truncated")

    width = int(video.get("width") or 0)
    height = int(video.get("height") or 0)
    # A phone video carries rotation metadata; swap so downstream sizing is real.
    rotation = 0
    for sd in video.get("side_data_list", []) or []:
        if "rotation" in sd:
            rotation = abs(int(sd["rotation"]))
    if rotation in (90, 270):
        width, height = height, width

    fps = _parse_fps(video.get("avg_frame_rate")) or _parse_fps(video.get("r_frame_rate")) or 30.0

    return ProbeResult(
        duration_seconds=round(duration, 3),
        width=width,
        height=height,
        fps=round(fps, 3),
        has_audio=audio is not None,
        video_codec=video.get("codec_name", "unknown"),
        audio_codec=audio.get("codec_name") if audio else None,
        recording_started_at=_creation_time(fmt.get("tags", {}) or {}, video.get("tags", {}) or {}),
        byte_size=int(fmt["size"]) if fmt.get("size") else None,
    )
