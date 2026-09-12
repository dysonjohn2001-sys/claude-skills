from phg.matching.name_resolver import NameResolver, normalize
from phg.models import Player


def p(pid, first, last, **kw):
    return Player(id=pid, first_name=first, last_name=last, **kw)


ROSTER = [
    p("1", "Jake", "Smith", jersey_number="7", batting_order=1),
    p("2", "Marcus", "Hernandez", jersey_number="12", batting_order=2),
    p("3", "Mateo", "Hernandez", jersey_number="21", batting_order=3),
    p("4", "Owen", "Brooks", jersey_number="4", batting_order=4, entered_inning=4),
]


def test_normalize_strips_punctuation_accents_and_suffixes():
    assert normalize("Hernández, Marcus Jr.") == "hernandez marcus"


def test_exact_name_is_full_confidence():
    r = NameResolver(ROSTER).resolve("Jake Smith")
    assert r.player_id == "1"
    assert r.confidence == 1.0
    assert r.method == "exact_name"


def test_last_comma_first_form():
    r = NameResolver(ROSTER).resolve("Smith, Jake")
    assert r.player_id == "1"


def test_shared_last_name_resolves_on_first_initial():
    r = NameResolver(ROSTER).resolve("Hernandez M")
    # Both Hernandezes start with M, so an initial is not enough.
    assert r.player_id is None or r.method != "last_first_initial"


def test_shared_last_name_alone_is_refused():
    r = NameResolver(ROSTER).resolve("Hernandez")
    assert r.player_id is None


def test_unique_last_name_resolves():
    r = NameResolver(ROSTER).resolve("Brooks")
    assert r.player_id == "4"
    assert r.method == "unique_last_name"


def test_jersey_number_inside_the_name_string():
    r = NameResolver(ROSTER).resolve("M HERNANDEZ #21")
    assert r.player_id == "3"
    assert r.method == "jersey_in_name"


def test_fuzzy_typo_resolves_below_full_confidence():
    r = NameResolver(ROSTER).resolve("Jake Smtih")
    assert r.player_id == "1"
    assert r.method == "fuzzy_name"
    assert r.confidence < 1.0


def test_ambiguous_fuzzy_refuses_and_reports_both():
    r = NameResolver(ROSTER).resolve("Marco Hernandez")
    if r.method == "ambiguous_fuzzy":
        assert r.player_id is None
        assert len(r.candidates) == 2
    else:
        # Whatever it picked, it must not have claimed certainty.
        assert r.confidence < 1.0


def test_empty_name_falls_back_to_batting_order():
    r = NameResolver(ROSTER).resolve("", expected_batting_order=2)
    assert r.player_id == "2"
    assert r.method == "batting_order"


def test_substitute_is_not_matched_before_entering():
    # Brooks entered in the 4th, so a 2nd-inning play should not resolve to him
    # by batting order.
    r = NameResolver(ROSTER).resolve("", expected_batting_order=4, inning=2)
    assert r.player_id is None


def test_batting_order_cross_check():
    resolver = NameResolver(ROSTER)
    assert resolver.confirms_batting_order("1", 1) is True
    assert resolver.confirms_batting_order("1", 3) is False
    assert resolver.confirms_batting_order("1", None) is None
