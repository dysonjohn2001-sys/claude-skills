"""Composite confidence for a player-to-clip assignment.

Every factor is recorded alongside the score, because the review screen has to
tell a coach *why* a clip is uncertain. "0.62" is useless; "we could not
confirm the batting slot and the lineup has two Hernandezes" is actionable.

Weights are deliberately lopsided toward the scheduling signals. Jersey
recognition is capped so that even a perfect digit read cannot carry a clip on
its own, and a wrong digit read cannot sink a clip the scorebook is sure of.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Primary weights, summing to 1.0. These apply to the schedule-based decision.
WEIGHTS = {
    "name_resolution": 0.42,
    "timeline_precision": 0.24,
    "batting_order": 0.16,
    "lineup_presence": 0.10,
    "position_fit": 0.08,
}


@dataclass
class ConfidenceResult:
    score: float
    factors: dict[str, float] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)
    method: str = "schedule"

    def as_dict(self) -> dict[str, float]:
        return dict(self.factors)


def timeline_subscore(uncertainty_seconds: float, anchor_count: int) -> float:
    """How tightly we located the play in the footage.

    A +/- 5s window on an interpolated two-anchor fit is near-certain. A +/- 85s
    window from a bare container timestamp is close to useless.
    """
    if anchor_count == 0:
        base = 0.30
    elif anchor_count == 1:
        base = 0.70
    else:
        base = 1.00
    # Decay linearly from full credit at 10s to no credit at 90s.
    span = max(0.0, min(1.0, (90.0 - uncertainty_seconds) / 80.0))
    return round(base * span, 4)


def position_subscore(play_type: str, role: str, positions: tuple[str, ...]) -> float:
    """Does this player actually play the position the play implies?"""
    if role not in {"fielder_putout", "fielder_assist", "fielder_error", "catcher", "pitcher"}:
        return 1.0                       # not a positional claim; no evidence either way
    if not positions:
        return 0.6                       # roster has no positions on file; neutral-ish
    implied = {
        "pitcher": {"P"},
        "catcher": {"C"},
    }.get(role)
    if implied is None:
        return 1.0 if len(positions) > 0 else 0.6
    return 1.0 if implied & set(positions) else 0.35


def compute(
    *,
    name_confidence: float,
    uncertainty_seconds: float,
    anchor_count: int,
    batting_order_agrees: bool | None,
    in_lineup: bool,
    play_type: str,
    role: str,
    positions: tuple[str, ...] = (),
) -> ConfidenceResult:
    """Score a schedule-based assignment before any jersey adjustment."""
    reasons: list[str] = []

    f_name = max(0.0, min(1.0, name_confidence))
    if f_name == 0.0:
        reasons.append("scorebook name did not resolve to anyone on the roster")
    elif f_name < 0.75:
        reasons.append("scorebook name matched only approximately")

    f_time = timeline_subscore(uncertainty_seconds, anchor_count)
    if anchor_count == 0:
        reasons.append("no sync anchor set for this video; timing is from file metadata only")
    elif uncertainty_seconds > 40:
        reasons.append(f"play located to within +/-{uncertainty_seconds:.0f}s only")

    if batting_order_agrees is None:
        f_order = 0.55                   # no lineup to check against; neither help nor harm
        reasons.append("no batting order on file for this game")
    elif batting_order_agrees:
        f_order = 1.0
    else:
        f_order = 0.10
        reasons.append("player does not match the expected batting slot")

    f_lineup = 1.0 if in_lineup else 0.25
    if not in_lineup:
        reasons.append("player was not recorded as in the game at this inning")

    f_pos = position_subscore(play_type, role, positions)
    if f_pos < 0.5:
        reasons.append(f"player is not listed at the position implied by a {role} credit")

    factors = {
        "name_resolution": round(f_name, 4),
        "timeline_precision": f_time,
        "batting_order": round(f_order, 4),
        "lineup_presence": f_lineup,
        "position_fit": round(f_pos, 4),
    }
    score = sum(WEIGHTS[k] * v for k, v in factors.items())

    # Hard gate: a clip whose subject we could not name is never high confidence,
    # however clean the timing is.
    if f_name == 0.0:
        score = min(score, 0.35)

    return ConfidenceResult(score=round(score, 4), factors=factors, reasons=reasons)


def apply_jersey(
    result: ConfidenceResult,
    *,
    expected_jersey: str | None,
    observations: list[tuple[str, float]],
    max_adjustment: float = 0.18,
) -> ConfidenceResult:
    """Fold in jersey-number reads as a bounded secondary signal.

    `observations` is a list of (digits, ocr_confidence). Agreement nudges the
    score up, disagreement nudges it down, and neither can move it by more than
    `max_adjustment`. Jersey evidence alone never produces an assignment.
    """
    if not expected_jersey or not observations:
        result.factors["jersey_agreement"] = 0.0
        return result

    want = expected_jersey.lstrip("0") or "0"
    agree = sum(c for d, c in observations if (d.lstrip("0") or "0") == want)
    disagree = sum(c for d, c in observations if (d.lstrip("0") or "0") != want)
    total = agree + disagree
    if total == 0:
        result.factors["jersey_agreement"] = 0.0
        return result

    # -1.0 (every read says someone else) .. +1.0 (every read says this player)
    balance = (agree - disagree) / total
    # Weak, sparse evidence gets a smaller vote than a dozen confident reads.
    evidence_weight = min(1.0, total / 4.0)
    adjustment = balance * evidence_weight * max_adjustment

    result.factors["jersey_agreement"] = round(balance, 4)
    result.factors["jersey_adjustment"] = round(adjustment, 4)
    result.score = round(max(0.0, min(1.0, result.score + adjustment)), 4)
    result.method = "schedule_jersey"
    if balance < -0.5:
        result.reasons.append(
            f"jersey reads in this clip mostly show a number other than #{expected_jersey}"
        )
    return result
