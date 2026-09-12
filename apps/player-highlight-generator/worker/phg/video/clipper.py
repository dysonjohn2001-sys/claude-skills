"""Cut one highlight clip out of a source recording with FFmpeg.

A single filter graph does all of it in one pass:

    trim kept spans -> concat -> optional slow-motion section -> fit to canvas
    -> scorebug -> lower third -> corner logo

Doing it in one pass matters. A three-hour game with 140 clips re-encoded three
times each is the difference between a coach getting reels the same evening and
getting them tomorrow.
"""

from __future__ import annotations

import logging
import shlex
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

from phg.video.overlays import (
    CANVAS,
    BrandTheme,
    ScoreboardState,
    logo_overlay_inputs,
    lower_third_filter,
    scorebug_filter,
)

log = logging.getLogger(__name__)


class RenderError(RuntimeError):
    pass


@dataclass
class SlowMotion:
    """A slow-motion section, in seconds relative to the trimmed clip."""

    start: float
    end: float
    rate: float = 0.5                     # 0.5 = half speed

    def valid_for(self, duration: float) -> bool:
        return 0.0 <= self.start < self.end <= duration + 0.01 and 0.1 <= self.rate < 1.0


@dataclass
class ClipSpec:
    source_path: str
    output_path: str
    spans: list[tuple[float, float]]       # absolute seconds in the source
    aspect: str = "16:9"
    theme: BrandTheme | None = None
    scoreboard: ScoreboardState | None = None
    lower_third: tuple[str, str] | None = None
    slowmo: SlowMotion | None = None
    mute_source: bool = False
    crf: int = 20
    preset: str = "medium"
    fps: int = 30
    ffmpeg: str = "ffmpeg"
    extra_filters: list[str] = field(default_factory=list)

    @property
    def trimmed_duration(self) -> float:
        return sum(max(0.0, e - s) for s, e in self.spans)


def build_command(spec: ClipSpec) -> list[str]:
    """Assemble the FFmpeg argv. Split out so it can be unit-tested dry."""
    if not spec.spans:
        raise RenderError("clip has no kept spans")
    width, height = CANVAS[spec.aspect]
    theme = spec.theme

    args: list[str] = [spec.ffmpeg, "-hide_banner", "-loglevel", "error", "-y"]
    args += ["-i", spec.source_path]

    logo = logo_overlay_inputs(theme, spec.aspect) if theme else None
    if logo:
        args += logo[0]

    # Every clip carries an audio track even when the source is muted. Uniform
    # stream layout is what lets the reel stage concatenate without gaps.
    silent_input_index = None
    if spec.mute_source:
        silent_input_index = 2 if logo else 1
        args += [
            "-f", "lavfi",
            "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
        ]

    v_chain: list[str] = []
    a_chain: list[str] = []

    # 1. Trim every kept span and concatenate them.
    for i, (start, end) in enumerate(spec.spans):
        v_chain.append(f"[0:v]trim=start={start:.3f}:end={end:.3f},setpts=PTS-STARTPTS[v{i}]")
        if not spec.mute_source:
            a_chain.append(f"[0:a]atrim=start={start:.3f}:end={end:.3f},asetpts=PTS-STARTPTS[a{i}]")

    n = len(spec.spans)
    if n == 1:
        v_label, a_label = "[v0]", "[a0]"
    else:
        v_inputs = "".join(f"[v{i}]" for i in range(n))
        v_chain.append(f"{v_inputs}concat=n={n}:v=1:a=0[vcat]")
        v_label = "[vcat]"
        if not spec.mute_source:
            a_inputs = "".join(f"[a{i}]" for i in range(n))
            a_chain.append(f"{a_inputs}concat=n={n}:v=0:a=1[acat]")
            a_label = "[acat]"
        else:
            a_label = ""

    # 2. Slow-motion section, if one was requested and fits.
    if spec.slowmo and spec.slowmo.valid_for(spec.trimmed_duration):
        v_label, a_label, slow_v, slow_a = _slow_motion_chain(
            spec.slowmo, spec.trimmed_duration, v_label, a_label, spec.mute_source
        )
        v_chain += slow_v
        a_chain += slow_a

    # 3. Fit to the export canvas without distorting the source.
    v_chain.append(
        f"{v_label}scale={width}:{height}:force_original_aspect_ratio=decrease,"
        f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=black,"
        f"setsar=1,fps={spec.fps}[fit]"
    )
    current = "[fit]"

    # 4. Branding overlays.
    overlay_filters = list(spec.extra_filters)
    if theme and spec.scoreboard:
        overlay_filters.append(scorebug_filter(spec.scoreboard, theme, spec.aspect))
    if theme and spec.lower_third:
        overlay_filters.append(lower_third_filter(*spec.lower_third, theme, spec.aspect))

    if overlay_filters:
        v_chain.append(f"{current}{','.join(overlay_filters)}[base]")
        current = "[base]"
    else:
        v_chain.append(f"{current}null[base]")
        current = "[base]"

    if logo:
        # logo_overlay_inputs writes its fragment against [base] and [logo].
        v_chain.append(f"[1:v]null[logo]")
        v_chain.append(logo[1] + "[out]")
        current = "[out]"
    else:
        v_chain.append(f"{current}null[out]")
        current = "[out]"

    graph = ";".join(v_chain + a_chain)
    args += ["-filter_complex", graph, "-map", current]
    if not spec.mute_source and a_label:
        args += ["-map", a_label]
    else:
        args += ["-map", f"{silent_input_index}:a", "-shortest"]
    args += ["-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2"]

    args += [
        "-c:v", "libx264",
        "-preset", spec.preset,
        "-crf", str(spec.crf),
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        spec.output_path,
    ]
    return args


def _slow_motion_chain(
    slow: SlowMotion, duration: float, v_label: str, a_label: str, muted: bool
) -> tuple[str, str, list[str], list[str]]:
    """Split into head / slowed middle / tail and re-concat."""
    v: list[str] = []
    a: list[str] = []
    factor = 1.0 / slow.rate            # 0.5 rate -> PTS * 2

    v.append(f"{v_label}split=3[sv0][sv1][sv2]")
    v.append(f"[sv0]trim=start=0:end={slow.start:.3f},setpts=PTS-STARTPTS[sh]")
    v.append(
        f"[sv1]trim=start={slow.start:.3f}:end={slow.end:.3f},"
        f"setpts={factor:.4f}*(PTS-STARTPTS)[sm]"
    )
    v.append(f"[sv2]trim=start={slow.end:.3f}:end={duration:.3f},setpts=PTS-STARTPTS[st]")
    v.append("[sh][sm][st]concat=n=3:v=1:a=0[vslow]")

    if muted or not a_label:
        return "[vslow]", "", v, a

    # atempo keeps audio in sync with the stretched video. Below 0.5 it has to
    # be chained, which sounds worse than simply dropping to silence.
    a.append(f"{a_label}asplit=3[sa0][sa1][sa2]")
    a.append(f"[sa0]atrim=start=0:end={slow.start:.3f},asetpts=PTS-STARTPTS[ah]")
    if slow.rate >= 0.5:
        a.append(
            f"[sa1]atrim=start={slow.start:.3f}:end={slow.end:.3f},asetpts=PTS-STARTPTS,"
            f"atempo={slow.rate:.3f}[am]"
        )
    else:
        a.append(
            f"[sa1]atrim=start={slow.start:.3f}:end={slow.end:.3f},asetpts=PTS-STARTPTS,"
            f"volume=0,atempo=0.5,atempo={max(0.5, slow.rate / 0.5):.3f}[am]"
        )
    a.append(f"[sa2]atrim=start={slow.end:.3f}:end={duration:.3f},asetpts=PTS-STARTPTS[at]")
    a.append("[ah][am][at]concat=n=3:v=0:a=1[aslow]")
    return "[vslow]", "[aslow]", v, a


def cut(spec: ClipSpec, timeout: int = 900) -> str:
    """Run the cut and return the output path."""
    Path(spec.output_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = build_command(spec)
    log.debug("ffmpeg: %s", " ".join(shlex.quote(c) for c in cmd))
    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=True)
    except FileNotFoundError as exc:
        raise RenderError(f"ffmpeg not found ({spec.ffmpeg})") from exc
    except subprocess.CalledProcessError as exc:
        raise RenderError(f"ffmpeg failed cutting {spec.output_path}: {exc.stderr.strip()[-800:]}") from exc
    except subprocess.TimeoutExpired as exc:
        raise RenderError(f"ffmpeg timed out cutting {spec.output_path}") from exc
    return spec.output_path


def thumbnail(source: str, at_seconds: float, out_path: str, ffmpeg: str = "ffmpeg") -> str:
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
        "-ss", f"{at_seconds:.3f}", "-i", source,
        "-frames:v", "1", "-vf", "scale=640:-2", out_path,
    ]
    subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=True)
    return out_path
