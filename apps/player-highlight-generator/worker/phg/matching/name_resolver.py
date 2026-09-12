"""Resolve a name string from a play-by-play export to a roster player.

Scorekeeper exports write names inconsistently: "Smith, J.", "Jake Smith",
"J SMITH #12", "Smith". The resolver walks progressively weaker strategies and
reports which one fired, so the confidence model downstream can price it.

No strategy here ever guesses between two equally good candidates. An
ambiguous name resolves to nothing, and the clip goes to the review queue.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from difflib import SequenceMatcher

from phg.models import Player

_JERSEY_IN_NAME = re.compile(r"#\s*(\d{1,2})\b")
_NON_NAME = re.compile(r"[^a-z\s]")
_SUFFIXES = {"jr", "sr", "ii", "iii", "iv"}

# Confidence by strategy. These are deliberately spread far apart: the gap
# between an exact match and a fuzzy one should dominate any later adjustment.
CONFIDENCE = {
    "exact_name": 1.00,
    "jersey_in_name": 0.95,
    "last_first_initial": 0.92,
    "unique_last_name": 0.88,
    "fuzzy_name": 0.70,
    "batting_order": 0.65,
    "unresolved": 0.00,
}

FUZZY_FLOOR = 0.86          # SequenceMatcher ratio below which we do not guess
FUZZY_MARGIN = 0.06         # runner-up must be this much worse, or it is ambiguous


@dataclass(frozen=True)
class Resolution:
    player_id: str | None
    confidence: float
    method: str
    candidates: tuple[str, ...] = ()   # populated when ambiguous, for the review UI

    @property
    def resolved(self) -> bool:
        return self.player_id is not None


def normalize(raw: str) -> str:
    """Lowercase, strip accents, drop punctuation and name suffixes."""
    s = unicodedata.normalize("NFKD", raw)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower().replace(",", " ")
    s = _NON_NAME.sub(" ", s)
    parts = [p for p in s.split() if p not in _SUFFIXES]
    return " ".join(parts)


def _name_forms(player: Player) -> set[str]:
    """Every spelling of a roster player we are willing to accept."""
    first = normalize(player.first_name)
    last = normalize(player.last_name)
    pref = normalize(player.preferred_name) if player.preferred_name else ""
    forms = {f"{first} {last}", f"{last} {first}"}
    if pref:
        forms |= {f"{pref} {last}", f"{last} {pref}"}
    return {f for f in forms if f.strip()}


class NameResolver:
    """Built once per game from that game's active roster."""

    def __init__(self, players: list[Player]) -> None:
        self.players = players
        self._by_form: dict[str, list[Player]] = {}
        self._by_last: dict[str, list[Player]] = {}
        self._by_jersey: dict[str, list[Player]] = {}
        self._by_order: dict[int, Player] = {}

        for p in players:
            for form in _name_forms(p):
                self._by_form.setdefault(form, []).append(p)
            self._by_last.setdefault(normalize(p.last_name), []).append(p)
            if p.jersey_number:
                self._by_jersey.setdefault(p.jersey_number.lstrip("0") or "0", []).append(p)
            if p.batting_order:
                self._by_order[p.batting_order] = p

    # -- public -----------------------------------------------------------

    def resolve(
        self,
        raw_name: str | None,
        *,
        expected_batting_order: int | None = None,
        inning: int = 1,
    ) -> Resolution:
        """Resolve one name. `expected_batting_order` is a cross-check, not a guess."""
        if not raw_name or not raw_name.strip():
            return self._from_batting_order(expected_batting_order, inning)

        jersey_hit = _JERSEY_IN_NAME.search(raw_name)
        norm = normalize(raw_name)

        # 1. Exact, on any accepted spelling.
        exact = self._eligible(self._by_form.get(norm, []), inning)
        if len(exact) == 1:
            return Resolution(exact[0].id, CONFIDENCE["exact_name"], "exact_name")

        # 2. An explicit jersey number inside the name string.
        if jersey_hit:
            key = jersey_hit.group(1).lstrip("0") or "0"
            by_num = self._eligible(self._by_jersey.get(key, []), inning)
            if len(by_num) == 1:
                return Resolution(by_num[0].id, CONFIDENCE["jersey_in_name"], "jersey_in_name")

        tokens = norm.split()

        # 3. "Smith J" / "J Smith" - last name plus a first initial.
        if len(tokens) >= 2:
            for last_tok, other in ((tokens[0], tokens[-1]), (tokens[-1], tokens[0])):
                pool = self._eligible(self._by_last.get(last_tok, []), inning)
                if len(other) == 1:
                    initial_hits = [p for p in pool if normalize(p.first_name).startswith(other)]
                    if len(initial_hits) == 1:
                        return Resolution(
                            initial_hits[0].id, CONFIDENCE["last_first_initial"], "last_first_initial"
                        )

        # 4. A last name that is unique on this roster.
        if tokens:
            for tok in (tokens[-1], tokens[0]):
                pool = self._eligible(self._by_last.get(tok, []), inning)
                if len(pool) == 1:
                    return Resolution(pool[0].id, CONFIDENCE["unique_last_name"], "unique_last_name")

        # 5. Fuzzy, with a hard ambiguity guard.
        fuzzy = self._fuzzy(norm, inning)
        if fuzzy is not None:
            return fuzzy

        # 6. Nothing matched the text; fall back to who was due up.
        return self._from_batting_order(expected_batting_order, inning, raw_name=raw_name)

    # -- internals --------------------------------------------------------

    def _eligible(self, pool: list[Player], inning: int) -> list[Player]:
        """Players who were actually in the game at that inning."""
        in_game = [p for p in pool if p.is_in_game(inning)]
        # If the lineup data says nobody was in, trust the name over the lineup
        # rather than dropping a real play on the floor.
        return in_game or pool

    def _fuzzy(self, norm: str, inning: int) -> Resolution | None:
        scored: list[tuple[float, Player]] = []
        for p in self.players:
            if not p.is_in_game(inning):
                continue
            best = max(SequenceMatcher(None, norm, form).ratio() for form in _name_forms(p))
            scored.append((best, p))
        if not scored:
            return None

        scored.sort(key=lambda t: t[0], reverse=True)
        top_score, top_player = scored[0]
        if top_score < FUZZY_FLOOR:
            return None
        if len(scored) > 1 and (top_score - scored[1][0]) < FUZZY_MARGIN:
            # Two roster names are about equally close. Refuse, and hand the
            # coach both options in the review screen.
            return Resolution(
                None,
                0.0,
                "ambiguous_fuzzy",
                candidates=(top_player.id, scored[1][1].id),
            )
        # Scale the fuzzy confidence by how good the match actually was.
        scaled = CONFIDENCE["fuzzy_name"] * (0.5 + 0.5 * top_score)
        return Resolution(top_player.id, round(scaled, 3), "fuzzy_name")

    def _from_batting_order(
        self, order: int | None, inning: int, raw_name: str | None = None
    ) -> Resolution:
        if order is None:
            return Resolution(None, 0.0, "unresolved")
        player = self._by_order.get(order)
        if player is None or not player.is_in_game(inning):
            return Resolution(None, 0.0, "unresolved")
        method = "batting_order" if raw_name is None else "batting_order_fallback"
        confidence = CONFIDENCE["batting_order"] if raw_name is None else CONFIDENCE["batting_order"] * 0.8
        return Resolution(player.id, round(confidence, 3), method)

    def confirms_batting_order(self, player_id: str, expected_order: int | None) -> bool | None:
        """True/False if we can check the slot, None if there is nothing to check."""
        if expected_order is None:
            return None
        expected = self._by_order.get(expected_order)
        if expected is None:
            return None
        return expected.id == player_id
