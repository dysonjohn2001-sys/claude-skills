"""Run the real FFmpeg pipeline on a synthetic source.

Unit tests elsewhere check the argv this code builds. These check that FFmpeg
actually accepts those filter graphs, which is a different question and the one
that breaks in practice.

Skipped automatically when FFmpeg is not installed.
"""

from __future__ import annotations

import json
import shutil
import subprocess

import pytest

from phg.video.clipper import ClipSpec, SlowMotion, cut, thumbnail
from phg.video.overlays import BrandTheme, PlayerCardData, ScoreboardState, render_intro_card
from phg.video.render import MusicBed, ReelSpec, render_reel

pytestmark = pytest.mark.skipif(
    shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None,
    reason="ffmpeg and ffprobe are required",
)


def probe(path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)


def make_source(path, seconds: int = 30) -> str:
    """A 30-second colour-bar clip with a tone, standing in for game footage."""
    subprocess.run(
        [
            "ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
            "-f", "lavfi", "-i", f"testsrc=size=1280x720:rate=30:duration={seconds}",
            "-f", "lavfi", "-i", f"sine=frequency=440:duration={seconds}",
            "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest", str(path),
        ],
        capture_output=True, text=True, check=True,
    )
    return str(path)


@pytest.fixture(scope="module")
def source(tmp_path_factory) -> str:
    return make_source(tmp_path_factory.mktemp("src") / "game.mp4")


def theme() -> BrandTheme:
    return BrandTheme(team_name="Riverside Rays", primary_color="#0F2B5B", secondary_color="#C8102E")


def test_single_span_cut_produces_a_playable_clip(source, tmp_path):
    out = tmp_path / "clip.mp4"
    cut(ClipSpec(source_path=source, output_path=str(out), spans=[(5.0, 18.0)]))

    info = probe(out)
    assert float(info["format"]["duration"]) == pytest.approx(13.0, abs=0.6)
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    assert (video["width"], video["height"]) == (1920, 1080)
    assert any(s["codec_type"] == "audio" for s in info["streams"])


def test_dead_time_removal_shortens_the_clip(source, tmp_path):
    """Two kept spans out of a 13-second window yield a 9-second clip."""
    out = tmp_path / "trimmed.mp4"
    cut(ClipSpec(source_path=source, output_path=str(out), spans=[(5.0, 10.0), (14.0, 18.0)]))
    assert float(probe(out)["format"]["duration"]) == pytest.approx(9.0, abs=0.6)


def test_vertical_export_is_1080x1920(source, tmp_path):
    out = tmp_path / "vertical.mp4"
    cut(ClipSpec(source_path=source, output_path=str(out), spans=[(5.0, 12.0)], aspect="9:16"))
    video = next(s for s in probe(out)["streams"] if s["codec_type"] == "video")
    assert (video["width"], video["height"]) == (1080, 1920)


def test_slow_motion_lengthens_only_the_selected_section(source, tmp_path):
    """A 10-second clip with 4 seconds halved runs 14 seconds."""
    out = tmp_path / "slowmo.mp4"
    cut(ClipSpec(
        source_path=source, output_path=str(out), spans=[(5.0, 15.0)],
        slowmo=SlowMotion(start=3.0, end=7.0, rate=0.5),
    ))
    assert float(probe(out)["format"]["duration"]) == pytest.approx(14.0, abs=0.8)


def test_overlays_render_without_ffmpeg_rejecting_the_graph(source, tmp_path):
    out = tmp_path / "branded.mp4"
    cut(ClipSpec(
        source_path=source, output_path=str(out), spans=[(5.0, 15.0)],
        theme=theme(),
        scoreboard=ScoreboardState(
            us_label="RAY", them_label="OWL", score_us=4, score_them=3,
            inning=6, half="bottom", outs=2,
        ),
        lower_third=("Jake Smith #7", "2-for-3, 2 RBI: Smith's double"),
    ))
    assert out.stat().st_size > 0
    assert float(probe(out)["format"]["duration"]) == pytest.approx(10.0, abs=0.6)


@pytest.mark.parametrize(
    "text",
    [
        "Jake Smith double",                       # baseline, nothing special
        "Smith's double",                          # quote: once rendered nothing at all
        "Top 6: two on",                           # colon: once truncated the line
        "2-for-3, 2 RBI: Smith's double",          # the real lower-third shape
        "O'Brien [PH] 100% RISP; safe",            # brackets, percent, semicolon
    ],
)
def test_special_characters_in_overlay_text_draw(source, tmp_path, text):
    """Count lit pixels, because FFmpeg exits 0 whether the text drew or not.

    Both escaping bugs this guards against were silent: one rendered an empty
    lower third, the other truncated it at the colon.
    """
    from PIL import Image

    clip = tmp_path / "clip.mp4"
    cut(ClipSpec(
        source_path=source, output_path=str(clip), spans=[(5.0, 7.0)],
        theme=theme(), lower_third=("Jake Smith #7", text), aspect="16:9",
    ))
    frame = tmp_path / "frame.png"
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-ss", "1.0",
         "-i", str(clip), "-frames:v", "1",
         # Crop the second line of the lower third only.
         "-vf", "crop=880:44:60:958", str(frame)],
        capture_output=True, check=True,
    )
    lit = sum(Image.open(frame).convert("L").histogram()[201:])

    # Roughly 55 lit pixels per drawn character at this size; a truncated or
    # missing line falls far below that.
    assert lit > 30 * len(text), f"only {lit} lit pixels for {len(text)} characters"


def test_logo_overlay_composites(source, tmp_path):
    logo = tmp_path / "logo.png"
    from PIL import Image

    Image.new("RGBA", (256, 256), (200, 16, 46, 255)).save(logo)
    out = tmp_path / "logo_clip.mp4"
    cut(ClipSpec(
        source_path=source, output_path=str(out), spans=[(5.0, 11.0)],
        theme=BrandTheme(team_name="Rays", logo_path=str(logo)),
    ))
    assert out.stat().st_size > 0


def test_muted_clip_carries_a_silent_track_not_a_missing_one(source, tmp_path):
    """A missing audio stream would break the concat filter at reel time."""
    out = tmp_path / "silent.mp4"
    cut(ClipSpec(source_path=source, output_path=str(out), spans=[(5.0, 10.0)], mute_source=True))

    info = probe(out)
    audio = next(s for s in info["streams"] if s["codec_type"] == "audio")
    assert audio["sample_rate"] == "48000"
    assert float(info["format"]["duration"]) == pytest.approx(5.0, abs=0.6)

    # And it really is silent.
    measured = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(out), "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    assert "mean_volume: -91" in measured or "mean_volume: -inf" in measured


def test_thumbnail_extraction(source, tmp_path):
    out = tmp_path / "thumb.jpg"
    thumbnail(source, 7.5, str(out))
    assert out.stat().st_size > 0


def test_full_reel_with_intro_card_and_ducked_music(source, tmp_path):
    clips = []
    for i, (start, end) in enumerate([(2.0, 9.0), (12.0, 20.0)]):
        path = tmp_path / f"clip{i}.mp4"
        cut(ClipSpec(source_path=source, output_path=str(path), spans=[(start, end)]))
        clips.append(str(path))

    intro = render_intro_card(
        PlayerCardData(
            display_name="Jake Smith", jersey_number="7", positions=["SS"],
            subtitle="Spring 2026", stat_lines=[("AVG", ".412"), ("RBI", "18")],
        ),
        theme(), tmp_path / "intro.png", "16:9",
    )

    music = tmp_path / "bed.m4a"
    subprocess.run(
        ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y",
         "-f", "lavfi", "-i", "sine=frequency=220:duration=6", "-c:a", "aac", str(music)],
        capture_output=True, check=True,
    )

    out = tmp_path / "reel.mp4"
    render_reel(ReelSpec(
        clip_paths=clips, output_path=str(out), aspect="16:9",
        intro_card_png=intro, intro_seconds=3.0,
        music=MusicBed(path=str(music), volume_db=-18.0, duck=True),
        work_dir=str(tmp_path / "work"),
    ))

    info = probe(out)
    # 3s intro + 7s + 8s of clips.
    assert float(info["format"]["duration"]) == pytest.approx(18.0, abs=0.4)
    video = next(s for s in info["streams"] if s["codec_type"] == "video")
    audio = next(s for s in info["streams"] if s["codec_type"] == "audio")
    assert (video["width"], video["height"]) == (1920, 1080)

    # Audio and video must stay locked together. The concat demuxer used to
    # drop about 1.5s of audio across three segments; the concat filter does not.
    assert float(audio["duration"]) == pytest.approx(float(video["duration"]), abs=0.25)


def test_reel_without_music_still_renders(source, tmp_path):
    clip = tmp_path / "c.mp4"
    cut(ClipSpec(source_path=source, output_path=str(clip), spans=[(3.0, 11.0)]))
    out = tmp_path / "plain.mp4"
    render_reel(ReelSpec(clip_paths=[str(clip)], output_path=str(out), work_dir=str(tmp_path / "w2")))
    assert float(probe(out)["format"]["duration"]) == pytest.approx(8.0, abs=0.6)
