"""Branding: intro cards, scorebugs, stat lower-thirds and the team logo.

Two mechanisms, chosen per element:

  * Static, text-heavy graphics (the player introduction card) are composed as
    PNGs with Pillow. Laying out a name, a number and a stat line with FFmpeg's
    drawtext is possible and miserable; Pillow gives real text metrics.
  * Anything that has to sit over moving video (scorebug, lower-third, logo) is
    an FFmpeg filter fragment, so it costs one pass rather than a pre-render.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# Canvas sizes per aspect. The pipeline renders everything at these and letter-
# or pillar-boxes the source to fit.
CANVAS = {
    "16:9": (1920, 1080),
    "9:16": (1080, 1920),
}

_DEFAULT_FONTS = (
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
)


def _find_font() -> str | None:
    for path in _DEFAULT_FONTS:
        if os.path.exists(path):
            return path
    return None


def _load_font(size: int, path: str | None = None) -> ImageFont.FreeTypeFont:
    candidate = path or _find_font()
    if candidate:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    v = value.lstrip("#")
    if len(v) == 3:
        v = "".join(c * 2 for c in v)
    return tuple(int(v[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore[return-value]


def _readable_text_on(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    """Pick black or white text for contrast, by relative luminance."""
    r, g, b = (c / 255.0 for c in rgb)
    lum = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return (17, 17, 17) if lum > 0.55 else (255, 255, 255)


@dataclass
class BrandTheme:
    team_name: str
    primary_color: str = "#0F2B5B"
    secondary_color: str = "#C8102E"
    logo_path: str | None = None
    font_path: str | None = None
    font_scale: float = 1.0

    @property
    def primary_rgb(self) -> tuple[int, int, int]:
        return _hex_to_rgb(self.primary_color)

    @property
    def secondary_rgb(self) -> tuple[int, int, int]:
        return _hex_to_rgb(self.secondary_color)

    @property
    def on_primary(self) -> tuple[int, int, int]:
        return _readable_text_on(self.primary_rgb)


@dataclass
class PlayerCardData:
    display_name: str
    jersey_number: str | None
    positions: list[str] = field(default_factory=list)
    subtitle: str = ""                      # "Spring 2026 - Riverside Rays"
    stat_lines: list[tuple[str, str]] = field(default_factory=list)  # [("AVG", ".412"), ...]
    photo_path: str | None = None


def render_intro_card(
    data: PlayerCardData,
    theme: BrandTheme,
    out_path: str | Path,
    aspect: str = "16:9",
) -> str:
    """Compose the player introduction card as a PNG and return its path."""
    width, height = CANVAS[aspect]
    vertical = aspect == "9:16"
    image = Image.new("RGB", (width, height), theme.primary_rgb)
    draw = ImageDraw.Draw(image)

    # Accent bar keeps the card from reading as a flat colour field.
    bar_h = int(height * 0.014)
    draw.rectangle([0, height - bar_h, width, height], fill=theme.secondary_rgb)

    scale = theme.font_scale * (0.62 if vertical else 1.0)
    f_number = _load_font(int(height * 0.30 * scale), theme.font_path)
    f_name = _load_font(int(height * 0.095 * scale), theme.font_path)
    f_sub = _load_font(int(height * 0.040 * scale), theme.font_path)
    f_stat_v = _load_font(int(height * 0.058 * scale), theme.font_path)
    f_stat_k = _load_font(int(height * 0.028 * scale), theme.font_path)

    fg = theme.on_primary
    muted = tuple(int(c * 0.72 + 128 * 0.28) for c in fg)

    cursor_y = int(height * (0.12 if vertical else 0.16))

    if data.jersey_number:
        text = f"#{data.jersey_number}"
        w = draw.textlength(text, font=f_number)
        draw.text(((width - w) / 2, cursor_y), text, font=f_number, fill=theme.secondary_rgb)
        cursor_y += int(height * 0.30 * scale) + int(height * 0.02)

    name = data.display_name.upper()
    w = draw.textlength(name, font=f_name)
    draw.text(((width - w) / 2, cursor_y), name, font=f_name, fill=fg)
    cursor_y += int(height * 0.095 * scale) + int(height * 0.015)

    subtitle_bits = [b for b in (", ".join(data.positions), data.subtitle) if b]
    if subtitle_bits:
        sub = "  |  ".join(subtitle_bits)
        w = draw.textlength(sub, font=f_sub)
        draw.text(((width - w) / 2, cursor_y), sub, font=f_sub, fill=muted)
        cursor_y += int(height * 0.04 * scale) + int(height * 0.05)

    if data.stat_lines:
        _draw_stat_row(draw, data.stat_lines, width, cursor_y, f_stat_v, f_stat_k, fg, muted)

    if theme.logo_path and os.path.exists(theme.logo_path):
        _paste_logo(image, theme.logo_path, width, height, corner="bottom-right")

    out = Path(out_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    image.save(out, "PNG")
    return str(out)


def _draw_stat_row(draw, stats, width, y, f_value, f_key, fg, muted) -> None:
    columns = len(stats)
    col_w = width / columns
    for i, (key, value) in enumerate(stats):
        centre = col_w * (i + 0.5)
        vw = draw.textlength(value, font=f_value)
        draw.text((centre - vw / 2, y), value, font=f_value, fill=fg)
        kw = draw.textlength(key, font=f_key)
        draw.text((centre - kw / 2, y + f_value.size * 1.15), key.upper(), font=f_key, fill=muted)


def _paste_logo(image: Image.Image, logo_path: str, width: int, height: int, corner: str) -> None:
    try:
        logo = Image.open(logo_path).convert("RGBA")
    except OSError:
        return
    target_w = int(width * 0.12)
    ratio = target_w / logo.width
    logo = logo.resize((target_w, max(1, int(logo.height * ratio))), Image.LANCZOS)
    pad = int(width * 0.03)
    positions = {
        "bottom-right": (width - logo.width - pad, height - logo.height - pad * 2),
        "top-right": (width - logo.width - pad, pad),
        "top-left": (pad, pad),
    }
    image.paste(logo, positions.get(corner, positions["bottom-right"]), logo)


# ---------------------------------------------------------------------------
# FFmpeg filter fragments
# ---------------------------------------------------------------------------


def escape_drawtext(text: str) -> str:
    """Escape a string to sit inside a ``text='...'`` option in a filtergraph.

    A filtergraph description is unescaped twice - once when the graph is split
    into filters, and again when each filter parses its own options - so the
    rules are not the obvious ones. Each was established by rendering a frame
    and reading back how many pixels lit up, because FFmpeg exits 0 whether the
    text drew, drew wrongly, or did not draw at all:

      backslash   doubled; one unescape pass consumes one
      quote       close the string, emit an escaped quote, reopen it. Writing
                  it as ``\'`` ends the string early and shifts the rest of the
                  graph, which silently renders nothing
      colon       single backslash; once the quotes are gone it separates options
      everything  left alone. Escaping a comma or bracket the way one would
      else        outside quotes draws a visible backslash on the video

    Percent signs and braces need no handling because every drawtext filter this
    module emits carries ``expansion=none``.

    Verified against FFmpeg 6.1; see
    tests/test_ffmpeg_pipeline.py::test_special_characters_in_overlay_text_draw.
    """
    out = text.replace("\\", "\\\\")
    out = out.replace("'", "'\\\\\\''")
    return out.replace(":", "\\:")


def _rgb_to_ffmpeg(rgb: tuple[int, int, int], alpha: float = 1.0) -> str:
    return "0x{:02X}{:02X}{:02X}@{:.2f}".format(*rgb, alpha)


@dataclass
class ScoreboardState:
    us_label: str
    them_label: str
    score_us: int
    score_them: int
    inning: int
    half: str                                # 'top' | 'bottom'
    outs: int | None = None

    def as_text(self) -> str:
        arrow = "^" if self.half == "top" else "v"
        line = f"{self.us_label} {self.score_us}  -  {self.score_them} {self.them_label}   {arrow}{self.inning}"
        if self.outs is not None:
            line += f"   {self.outs} OUT"
        return line


def scorebug_filter(state: ScoreboardState, theme: BrandTheme, aspect: str = "16:9") -> str:
    """A single drawbox+drawtext pair pinned to the top-left (top-centre on 9:16)."""
    width, height = CANVAS[aspect]
    font_size = int(height * (0.030 if aspect == "16:9" else 0.024))
    pad = int(height * 0.022)
    box_h = int(font_size * 2.0)
    box_w = int(width * (0.40 if aspect == "16:9" else 0.86))
    x = pad if aspect == "16:9" else int((width - box_w) / 2)

    font_arg = f":fontfile='{theme.font_path}'" if theme.font_path else ""
    return (
        f"drawbox=x={x}:y={pad}:w={box_w}:h={box_h}:"
        f"color={_rgb_to_ffmpeg(theme.primary_rgb, 0.78)}:t=fill,"
        f"drawbox=x={x}:y={pad + box_h - 4}:w={box_w}:h=4:"
        f"color={_rgb_to_ffmpeg(theme.secondary_rgb, 0.95)}:t=fill,"
        f"drawtext=expansion=none:text='{escape_drawtext(state.as_text())}'"
        f":x={x + int(font_size * 0.7)}:y={pad + int((box_h - font_size) / 2)}"
        f":fontsize={font_size}:fontcolor={_rgb_to_ffmpeg(theme.on_primary)}{font_arg}"
    )


def lower_third_filter(
    primary: str,
    secondary: str,
    theme: BrandTheme,
    aspect: str = "16:9",
    hold_seconds: float = 3.5,
    fade_seconds: float = 0.4,
) -> str:
    """Name and stat line that fades in at the head of a clip and out again."""
    width, height = CANVAS[aspect]
    f1 = int(height * (0.040 if aspect == "16:9" else 0.032))
    f2 = int(height * (0.026 if aspect == "16:9" else 0.022))
    pad = int(height * 0.035)
    box_h = int(f1 * 1.4 + f2 * 1.6)
    box_w = int(width * (0.46 if aspect == "16:9" else 0.90))
    y = height - box_h - pad * 2
    x = pad if aspect == "16:9" else int((width - box_w) / 2)

    enable = f"between(t,0,{hold_seconds:.2f})"
    alpha = (
        f"if(lt(t,{fade_seconds:.2f}),t/{fade_seconds:.2f},"
        f"if(gt(t,{hold_seconds - fade_seconds:.2f}),({hold_seconds:.2f}-t)/{fade_seconds:.2f},1))"
    )
    font_arg = f":fontfile='{theme.font_path}'" if theme.font_path else ""

    return (
        f"drawbox=x={x}:y={y}:w={box_w}:h={box_h}:"
        f"color={_rgb_to_ffmpeg(theme.primary_rgb, 0.80)}:t=fill:enable='{enable}',"
        f"drawbox=x={x}:y={y}:w=6:h={box_h}:"
        f"color={_rgb_to_ffmpeg(theme.secondary_rgb, 0.95)}:t=fill:enable='{enable}',"
        f"drawtext=expansion=none:text='{escape_drawtext(primary)}'"
        f":x={x + int(f1 * 0.6)}:y={y + int(f1 * 0.3)}:fontsize={f1}"
        f":fontcolor={_rgb_to_ffmpeg(theme.on_primary)}:alpha='{alpha}':enable='{enable}'{font_arg},"
        f"drawtext=expansion=none:text='{escape_drawtext(secondary)}'"
        f":x={x + int(f1 * 0.6)}:y={y + int(f1 * 1.5)}:fontsize={f2}"
        f":fontcolor={_rgb_to_ffmpeg(theme.on_primary)}:alpha='{alpha}':enable='{enable}'{font_arg}"
    )


def logo_overlay_inputs(theme: BrandTheme, aspect: str = "16:9") -> tuple[list[str], str] | None:
    """Return (extra ffmpeg input args, filter fragment) for the corner logo."""
    if not theme.logo_path or not os.path.exists(theme.logo_path):
        return None
    width, height = CANVAS[aspect]
    logo_w = int(width * 0.085)
    margin = int(width * 0.025)
    args = ["-i", theme.logo_path]
    fragment = (
        f"[logo]scale={logo_w}:-1[lg];"
        f"[base][lg]overlay=W-w-{margin}:H-h-{margin}"
    )
    return args, fragment
