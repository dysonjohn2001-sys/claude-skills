from PIL import Image

import pytest

from phg.video.overlays import (
    CANVAS,
    INK,
    PAPER,
    BrandTheme,
    PlayerCardData,
    ScoreboardState,
    _hex_to_rgb,
    _readable_text_on,
    contrast_ratio,
    lower_third_filter,
    relative_luminance,
    render_intro_card,
    scorebug_filter,
)


def theme(**kw) -> BrandTheme:
    base = dict(team_name="Riverside Rays", primary_color="#0F2B5B", secondary_color="#C8102E")
    base.update(kw)
    return BrandTheme(**base)


def card() -> PlayerCardData:
    return PlayerCardData(
        display_name="Jake Smith",
        jersey_number="7",
        positions=["SS", "P"],
        subtitle="Spring 2026 - Riverside Rays",
        stat_lines=[("AVG", ".412"), ("H", "21"), ("RBI", "18")],
    )


def test_intro_card_renders_at_the_horizontal_canvas_size(tmp_path):
    path = render_intro_card(card(), theme(), tmp_path / "c.png", "16:9")
    assert Image.open(path).size == CANVAS["16:9"]


def test_intro_card_renders_at_the_vertical_canvas_size(tmp_path):
    path = render_intro_card(card(), theme(), tmp_path / "v.png", "9:16")
    assert Image.open(path).size == CANVAS["9:16"]


def test_card_background_uses_the_team_primary_colour(tmp_path):
    path = render_intro_card(card(), theme(primary_color="#1A7F37"), tmp_path / "g.png", "16:9")
    # Sample a corner, which no text or accent bar reaches.
    assert Image.open(path).convert("RGB").getpixel((5, 5)) == (0x1A, 0x7F, 0x37)


def test_text_colour_flips_for_light_and_dark_brands():
    assert _readable_text_on(PAPER) == INK
    assert _readable_text_on((15, 43, 91)) == PAPER


def test_relative_luminance_matches_wcag_anchors():
    assert relative_luminance(PAPER) == pytest.approx(1.0, abs=0.001)
    assert relative_luminance((0, 0, 0)) == pytest.approx(0.0, abs=0.001)
    assert contrast_ratio(PAPER, (0, 0, 0)) == pytest.approx(21.0, abs=0.05)


@pytest.mark.parametrize(
    "brand",
    ["#E8641C", "#0F2B5B", "#FFC72C", "#C8102E", "#D9D9D9", "#1B5E20", "#6EC6FF", "#111111"],
)
def test_chosen_text_colour_always_clears_wcag_aa(brand):
    """Comparing raw channel values instead of linearized ones put a real team's
    orange on the wrong side: white at 3.35:1 over black at 5.64:1."""
    rgb = _hex_to_rgb(brand)
    chosen = _readable_text_on(rgb)
    other = INK if chosen == PAPER else PAPER
    assert contrast_ratio(chosen, rgb) >= contrast_ratio(other, rgb)
    assert contrast_ratio(chosen, rgb) >= 4.5


def test_mid_orange_takes_black_text():
    assert _readable_text_on(_hex_to_rgb("#E8641C")) == INK


def _box_width(fragment: str) -> int:
    import re

    return int(re.search(r"drawbox=x=\d+:y=\d+:w=(\d+)", fragment).group(1))


def test_scorebug_box_fits_its_text():
    """A fixed fraction of the frame leaves a short score line in a box two
    thirds empty, which reads as broken."""
    short = scorebug_filter(
        ScoreboardState("A", "B", 1, 0, 1, "top"), theme(), "16:9"
    )
    long = scorebug_filter(
        ScoreboardState("RIVERSIDE", "NORTHSIDE", 12, 11, 9, "bottom", outs=2), theme(), "16:9"
    )
    assert _box_width(short) < _box_width(long)
    assert _box_width(long) <= int(1920 * 0.62)


def test_lower_third_box_fits_the_wider_of_its_two_lines():
    narrow = lower_third_filter("Al Ray", "1-1", theme(), "16:9")
    wide = lower_third_filter(
        "Bartholomew Fitzwilliam", "4-for-4, 3 RBI, 2 stolen bases", theme(), "16:9"
    )
    assert _box_width(narrow) < _box_width(wide)
    assert _box_width(wide) <= int(1920 * 0.80)


def test_card_without_a_jersey_number_still_renders(tmp_path):
    data = card()
    data.jersey_number = None
    path = render_intro_card(data, theme(), tmp_path / "n.png", "16:9")
    assert Image.open(path).size == CANVAS["16:9"]


def test_card_with_no_stats_still_renders(tmp_path):
    data = card()
    data.stat_lines = []
    path = render_intro_card(data, theme(), tmp_path / "s.png", "16:9")
    assert Image.open(path).size == CANVAS["16:9"]
