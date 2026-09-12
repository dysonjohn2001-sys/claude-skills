import pytest

from phg.video.clipper import RenderError
from phg.video.render import MusicBed, ReelSpec, _reel_command, render_reel

SEGMENTS = ["/media/clips/intro.mp4", "/media/clips/a.mp4", "/media/clips/b.mp4"]


def spec(**kw) -> ReelSpec:
    base = dict(clip_paths=["/media/clips/a.mp4", "/media/clips/b.mp4"],
                output_path="/media/reels/r.mp4")
    base.update(kw)
    return ReelSpec(**base)


def graph_of(args: list[str]) -> str:
    return args[args.index("-filter_complex") + 1]


def test_reel_with_no_clips_is_refused(tmp_path):
    with pytest.raises(RenderError):
        render_reel(spec(clip_paths=[], work_dir=str(tmp_path)))


def test_every_segment_becomes_an_input():
    args = _reel_command(spec(), SEGMENTS)
    assert args.count("-i") == len(SEGMENTS)
    for segment in SEGMENTS:
        assert segment in args


def test_segments_are_joined_with_the_concat_filter_not_the_demuxer():
    """The demuxer drops audio at segment boundaries; the filter does not."""
    args = _reel_command(spec(), SEGMENTS)
    graph = graph_of(args)
    assert f"concat=n={len(SEGMENTS)}:v=1:a=1[vcat][acat]" in graph
    assert "concat" not in [args[i + 1] for i, a in enumerate(args) if a == "-f"]


def test_segments_are_normalised_before_concatenating():
    graph = graph_of(_reel_command(spec(), SEGMENTS))
    assert graph.count("scale=1920:1080") == len(SEGMENTS)
    assert graph.count("aformat=sample_rates=48000") == len(SEGMENTS)


def test_vertical_reel_uses_the_vertical_canvas():
    graph = graph_of(_reel_command(spec(aspect="9:16"), SEGMENTS))
    assert "scale=1080:1920" in graph and "pad=1080:1920" in graph


def test_without_music_the_clip_audio_passes_through():
    args = _reel_command(spec(), SEGMENTS)
    assert "-map" in args and "[acat]" in args
    assert "sidechaincompress" not in graph_of(args)


def test_ducking_uses_sidechain_compression_keyed_on_clip_audio():
    graph = graph_of(_reel_command(spec(music=MusicBed(path="/media/music/bed.mp3", duck=True)), SEGMENTS))
    assert "sidechaincompress" in graph
    assert "[acat]asplit=2[clipout][key]" in graph


def test_flat_music_mix_when_ducking_is_off():
    graph = graph_of(_reel_command(spec(music=MusicBed(path="/media/music/bed.mp3", duck=False)), SEGMENTS))
    assert "sidechaincompress" not in graph
    assert "amix=inputs=2" in graph


def test_music_volume_is_applied_in_decibels():
    graph = graph_of(_reel_command(spec(music=MusicBed(path="/media/music/bed.mp3", volume_db=-24.0)), SEGMENTS))
    assert "volume=-24.00dB" in graph


def test_music_is_looped_so_a_short_bed_covers_a_long_reel():
    args = _reel_command(spec(music=MusicBed(path="/media/music/bed.mp3")), SEGMENTS)
    assert "-stream_loop" in args
    assert args[args.index("-stream_loop") + 1] == "-1"


def test_music_mix_truncates_to_the_video_not_the_bed():
    graph = graph_of(_reel_command(spec(music=MusicBed(path="/media/music/bed.mp3")), SEGMENTS))
    assert "duration=first" in graph


def test_faststart_is_set_so_parents_can_stream_without_downloading():
    assert "+faststart" in _reel_command(spec(), SEGMENTS)
