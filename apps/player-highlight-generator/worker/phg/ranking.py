"""Rank clips so a reel leads with the play worth watching.

The score is deliberately explainable: every component is named, bounded and
written back to `clips.rank_factors`, so the review screen can show "ranked 1st:
go-ahead double in the 6th" instead of an opaque number.

Scores land on 0-100. Nothing here is a model; it is a weighted rubric a coach
can argue with and a settings screen can re-weight.
"""

from __future__ import annotations

from dataclasses import dataclass

from phg.models import ClipCandidate, Play

# Base merit of the play itself, by what happened.
PLAY_WEIGHT = {
    "home_run": 100.0,
    "triple": 82.0,
    "double": 68.0,
    "single": 52.0,
    "walk": 28.0,
    "hit_by_pitch": 26.0,
    "sacrifice_fly": 40.0,
    "sacrifice_bunt": 34.0,
    "fielders_choice": 24.0,
    "error_reached": 20.0,
    "stolen_base": 46.0,
    "advanced_on_error": 24.0,
    "advanced_on_wild_pitch": 20.0,
    "scored": 44.0,
    "strikeout": 30.0,          # excellent for the pitcher, poor for the batter
    "groundout": 14.0,
    "flyout": 14.0,
    "lineout": 16.0,
    "popout": 10.0,
    "double_play": 58.0,
    "triple_play": 95.0,
    "caught_stealing": 8.0,
    "picked_off": 6.0,
    "wild_pitch": 6.0,
    "balk": 4.0,
}

# Defensive credit is not in the play type, it is in the role.
ROLE_BONUS = {
    "fielder_putout": 34.0,
    "fielder_assist": 26.0,
    "fielder_error": 0.0,
    "pitcher": 18.0,
}

DEFAULT_WEIGHTS = {
    "play_merit": 0.40,
    "leverage": 0.22,
    "production": 0.14,
    "action_density": 0.12,
    "confidence": 0.12,
}


@dataclass(frozen=True)
class RankInputs:
    play: Play
    role: str
    category: str
    action_density: float = 0.5      # 0..1, from dead-time analysis
    total_innings: int = 7
    include_negative_plays: bool = False


def _play_merit(play: Play, role: str, category: str) -> float:
    base = PLAY_WEIGHT.get(play.play_type, 20.0)
    if category == "pitching" and play.play_type == "strikeout":
        base = 62.0                  # a K is a highlight for the pitcher
    if category == "offense" and play.play_type == "strikeout":
        base = 4.0                   # and an anti-highlight for the batter
    if category == "defense":
        base = max(base, 0.0) * 0.35 + ROLE_BONUS.get(role, 0.0)
    if role == "fielder_error":
        base *= 0.15
    return max(0.0, min(100.0, base))


def _leverage(play: Play, total_innings: int) -> float:
    """Late, close and run-producing situations score higher."""
    score = 30.0

    # Lateness: linear from the first inning to the last.
    if total_innings > 0:
        score += 30.0 * min(1.0, max(0.0, (play.inning - 1) / max(1, total_innings - 1)))

    # Closeness: a one-run game matters more than a blowout.
    if play.score_us is not None and play.score_them is not None:
        margin = abs(play.score_us - play.score_them)
        score += max(0.0, 25.0 - 6.0 * margin)

    if play.leverage_tag in {"walk_off", "tying_run", "go_ahead_run"}:
        score += 15.0
    elif play.leverage_tag in {"bases_loaded", "risp", "two_outs"}:
        score += 8.0

    return max(0.0, min(100.0, score))


def _production(play: Play) -> float:
    return max(0.0, min(100.0, 25.0 * play.rbi + 20.0 * play.runs_scored))


def score_clip(candidate: ClipCandidate, inputs: RankInputs, weights: dict[str, float] | None = None) -> float:
    """Return 0-100 and write the component breakdown onto the candidate."""
    w = {**DEFAULT_WEIGHTS, **(weights or {})}

    merit = _play_merit(inputs.play, inputs.role, inputs.category)
    leverage = _leverage(inputs.play, inputs.total_innings)
    production = _production(inputs.play)
    density = max(0.0, min(1.0, inputs.action_density)) * 100.0
    confidence = max(0.0, min(1.0, candidate.match_confidence)) * 100.0

    components = {
        "play_merit": merit,
        "leverage": leverage,
        "production": production,
        "action_density": density,
        "confidence": confidence,
    }
    total = sum(w[k] * v for k, v in components.items())

    # An outcome the player would not want in their own reel is suppressed
    # rather than deleted, so the coach can still find it in the review screen.
    if not inputs.include_negative_plays:
        if inputs.role == "fielder_error":
            total *= 0.25
        if inputs.category == "offense" and inputs.play.play_type in {"strikeout", "popout"}:
            total *= 0.35
        if inputs.category == "baserunning" and inputs.play.play_type in {"caught_stealing", "picked_off"}:
            total *= 0.3

    candidate.rank_score = round(max(0.0, min(100.0, total)), 3)
    candidate.rank_factors = {k: round(v, 2) for k, v in components.items()}
    return candidate.rank_score


def select_for_reel(
    candidates: list[ClipCandidate],
    *,
    max_clips: int = 12,
    max_duration_seconds: float = 180.0,
    min_confidence: float = 0.45,
    category_floor: int = 1,
) -> list[ClipCandidate]:
    """Pick the clips that make the reel, then restore chronological order.

    Two rules beyond "take the top N":

      * every category the player actually appeared in gets at least
        `category_floor` clips, so a pitcher's reel is not 100% batting;
      * the duration cap is a hard stop, because a 9-minute reel is not a
        highlight reel.
    """
    eligible = [c for c in candidates if c.match_confidence >= min_confidence]
    eligible.sort(key=lambda c: c.rank_score, reverse=True)

    chosen: list[ClipCandidate] = []
    used = 0.0
    seen_categories: set[str] = set()

    # Pass 1: guarantee category coverage.
    for category in ("offense", "pitching", "defense", "baserunning"):
        for c in eligible:
            if c.category != category or c in chosen:
                continue
            if len([x for x in chosen if x.category == category]) >= category_floor:
                break
            if used + c.duration > max_duration_seconds or len(chosen) >= max_clips:
                break
            chosen.append(c)
            used += c.duration
            seen_categories.add(category)

    # Pass 2: fill the rest by rank.
    for c in eligible:
        if c in chosen or len(chosen) >= max_clips:
            continue
        if used + c.duration > max_duration_seconds:
            continue
        chosen.append(c)
        used += c.duration

    chosen.sort(key=lambda c: (c.media_asset_id, c.source_start_seconds))
    return chosen
