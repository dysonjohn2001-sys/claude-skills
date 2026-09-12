import pytest

from phg.matching.confidence import WEIGHTS, ConfidenceResult, apply_jersey, compute, timeline_subscore


def test_weights_sum_to_one():
    assert sum(WEIGHTS.values()) == pytest.approx(1.0)


def base(**kw):
    args = dict(
        name_confidence=1.0, uncertainty_seconds=12.0, anchor_count=2,
        batting_order_agrees=True, in_lineup=True, play_type="double", role="batter",
        positions=("SS",),
    )
    args.update(kw)
    return compute(**args)


def test_ideal_case_clears_auto_approval():
    assert base().score >= 0.80


def test_unresolved_name_is_capped_however_good_the_timing():
    r = base(name_confidence=0.0)
    assert r.score <= 0.35
    assert any("did not resolve" in reason for reason in r.reasons)


def test_batting_order_mismatch_hurts_and_is_explained():
    r = base(batting_order_agrees=False)
    assert r.score < base().score
    assert any("batting slot" in reason for reason in r.reasons)


def test_missing_sync_anchor_is_surfaced():
    r = base(anchor_count=0, uncertainty_seconds=85.0)
    assert r.score < base().score
    assert any("sync anchor" in reason for reason in r.reasons)


def test_timeline_subscore_ordering():
    assert timeline_subscore(10, 2) > timeline_subscore(10, 1) > timeline_subscore(10, 0)
    assert timeline_subscore(10, 2) > timeline_subscore(70, 2)


def test_position_mismatch_penalises_a_pitching_credit():
    r = base(role="pitcher", positions=("1B",), play_type="strikeout")
    assert r.factors["position_fit"] < 0.5


def test_jersey_agreement_nudges_up_within_the_cap():
    r = base(name_confidence=0.7)
    before = r.score
    apply_jersey(r, expected_jersey="7", observations=[("7", 0.9), ("7", 0.8)], max_adjustment=0.18)
    assert before < r.score <= before + 0.18
    assert r.method == "schedule_jersey"


def test_jersey_disagreement_cannot_overturn_a_confident_match():
    r = ConfidenceResult(score=0.95, factors={}, method="schedule")
    apply_jersey(r, expected_jersey="7", observations=[("12", 0.9)] * 10, max_adjustment=0.18)
    assert r.score >= 0.95 - 0.18
    assert r.score > 0.45          # still above the discard floor


def test_jersey_with_no_reads_changes_nothing():
    r = base()
    before = r.score
    apply_jersey(r, expected_jersey="7", observations=[])
    assert r.score == before


def test_sparse_jersey_evidence_votes_less_than_plentiful():
    a, b = base(name_confidence=0.7), base(name_confidence=0.7)
    apply_jersey(a, expected_jersey="7", observations=[("7", 0.9)])
    apply_jersey(b, expected_jersey="7", observations=[("7", 0.9)] * 5)
    assert a.score < b.score
