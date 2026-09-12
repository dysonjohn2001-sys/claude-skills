"""Assemble finished reels: intro card + clips + music bed -> one MP4.

Every clip arriving here has already been normalised by clipper.py to the same
canvas, frame rate, pixel format and audio codec, which is what makes the
concat step cheap and predictable.

Assembly uses FFmpeg's concat *filter* rather than the concat *demuxer*. The
demuxer is cheaper, but AAC segments joined that way lose audio at every
boundary: a three-segment reel came out with 18.0s of video against 16.6s of
audio, drifting further out of sync with each clip. The filter re-encodes and
keeps the two streams locked together. Since the reel is re-encoded for the
music mix anyway, the demuxer bought nothing.

Music handling is the other fiddly part. A flat music bed buries the crack of
the bat and the parents in the stands, which is the entire reason to keep source
audio. So the default is sidechain ducking: the music drops whenever the clip
audio is loud, and comes back up between plays.
"""

from __future__ import annotations

import logging
import shlex
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

from phg.video.clipper import RenderError
from phg.video.overlays import CANVAS

log = logging.getLogger(__name__)


@dataclass
class MusicBed:
    path: str
    volume_db: float = -18.0
    duck: bool = True
    duck_amount_db: float = -8.0
    fade_in_seconds: float = 1.0
    fade_out_seconds: float = 2.5


@dataclass
class ReelSpec:
    clip_paths: list[str]
    output_path: str
    aspect: str = "16:9"
    intro_card_png: str | None = None
    intro_seconds: float = 3.0
    outro_card_png: str | None = None
    outro_seconds: float = 2.5
    music: MusicBed | None = None
    fps: int = 30
    crf: int = 20
    preset: str = "medium"
    ffmpeg: str = "ffmpeg"
    work_dir: str | None = None
    extra_segments: list[str] = field(default_factory=list)


def card_to_segment(
    png_path: str,
    out_path: str,
    seconds: float,
    aspect: str,
    fps: int = 30,
    ffmpeg: str = "ffmpeg",
    fade: float = 0.4,
) -> str:
    """Turn a still card into a silent video segment matching the clip format."""
    width, height = CANVAS[aspect]
    fade_out_start = max(0.0, seconds - fade)
    cmd = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-loop", "1", "-t", f"{seconds:.3f}", "-i", png_path,
        "-f", "lavfi", "-t", f"{seconds:.3f}", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        "-vf",
        (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1,fps={fps},"
            f"fade=t=in:st=0:d={fade:.2f},fade=t=out:st={fade_out_start:.2f}:d={fade:.2f}"
        ),
        "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-shortest",
        out_path,
    ]
    _run(cmd, f"building card segment {out_path}")
    return out_path


def render_reel(spec: ReelSpec, timeout: int = 3600) -> str:
    """Build the intro/outro cards, concatenate everything, lay in music."""
    if not spec.clip_paths:
        raise RenderError("reel has no clips")

    work = Path(spec.work_dir or tempfile.mkdtemp(prefix="phg-reel-"))
    work.mkdir(parents=True, exist_ok=True)

    segments: list[str] = []
    if spec.intro_card_png:
        segments.append(
            card_to_segment(
                spec.intro_card_png, str(work / "intro.mp4"), spec.intro_seconds,
                spec.aspect, spec.fps, spec.ffmpeg,
            )
        )
    segments.extend(spec.clip_paths)
    segments.extend(spec.extra_segments)
    if spec.outro_card_png:
        segments.append(
            card_to_segment(
                spec.outro_card_png, str(work / "outro.mp4"), spec.outro_seconds,
                spec.aspect, spec.fps, spec.ffmpeg,
            )
        )

    Path(spec.output_path).parent.mkdir(parents=True, exist_ok=True)
    _run(_reel_command(spec, segments), f"rendering reel {spec.output_path}", timeout=timeout)
    return spec.output_path


def _reel_command(spec: ReelSpec, segments: list[str]) -> list[str]:
    """Assemble the argv. Separated from render_reel so it can be tested dry."""
    if not segments:
        raise RenderError("reel has no segments")

    width, height = CANVAS[spec.aspect]
    args = [spec.ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
    for segment in segments:
        args += ["-i", str(segment)]

    n = len(segments)
    # Normalise before concatenating. Segments should already match, but a clip
    # cut before a settings change might not, and a mismatch here fails the
    # whole reel rather than one clip.
    chain: list[str] = []
    for i in range(n):
        chain.append(
            f"[{i}:v]scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"setsar=1,fps={spec.fps},format=yuv420p[nv{i}]"
        )
        chain.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo[na{i}]")

    pairs = "".join(f"[nv{i}][na{i}]" for i in range(n))
    chain.append(f"{pairs}concat=n={n}:v=1:a=1[vcat][acat]")

    if spec.music is None:
        graph = ";".join(chain)
        args += [
            "-filter_complex", graph,
            "-map", "[vcat]", "-map", "[acat]",
            "-c:v", "libx264", "-preset", spec.preset, "-crf", str(spec.crf),
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", spec.output_path,
        ]
        return args

    m = spec.music
    music_index = n
    # Loop the bed so a 40-second track still covers a three-minute reel.
    args += ["-stream_loop", "-1", "-i", m.path]

    chain.append(
        f"[{music_index}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
        f"volume={m.volume_db:.2f}dB,afade=t=in:st=0:d={m.fade_in_seconds:.2f}[music]"
    )

    if m.duck:
        chain.append("[acat]asplit=2[clipout][key]")
        # The clip audio drives the compressor, so the bed drops under a crack
        # of the bat and comes back up between plays.
        chain.append(
            "[music][key]sidechaincompress="
            "threshold=0.03:ratio=8:attack=20:release=450:makeup=1[ducked]"
        )
        chain.append(
            "[clipout][ducked]amix=inputs=2:duration=first:dropout_transition=0,"
            f"afade=t=out:st=0:d={m.fade_out_seconds:.2f}:curve=tri[aout]"
        )
    else:
        chain.append("[acat][music]amix=inputs=2:duration=first:dropout_transition=0[aout]")

    args += [
        "-filter_complex", ";".join(chain),
        "-map", "[vcat]", "-map", "[aout]",
        "-c:v", "libx264", "-preset", spec.preset, "-crf", str(spec.crf),
        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart",
        spec.output_path,
    ]
    return args


def _run(cmd: list[str], what: str, timeout: int = 1800) -> None:
    log.debug("ffmpeg: %s", " ".join(shlex.quote(c) for c in cmd))
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=True)
    except FileNotFoundError as exc:
        raise RenderError(f"ffmpeg not found while {what}") from exc
    except subprocess.CalledProcessError as exc:
        raise RenderError(f"ffmpeg failed while {what}: {exc.stderr.strip()[-800:]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise RenderError(f"ffmpeg timed out while {what}") from exc
