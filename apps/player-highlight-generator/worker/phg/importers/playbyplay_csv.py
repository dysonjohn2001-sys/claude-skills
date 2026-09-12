"""Import a play-by-play CSV into play records.

The importer is forgiving about columns and strict about semantics. It will
guess which header means "inning". It will not guess whether a row describes
our offense or our defense - if the file does not say, the coach is asked,
because getting that wrong assigns every clip to the wrong side of the ball.

Where a file has only a free-text description, `classify()` derives a play type
from the narrative, and records that it did so, so the review screen can show
which rows were inferred.
"""

from __future__ import annotations

import csv
import io
import re
from dataclasses import dataclass, field
from datetime import datetime

from dateutil import parser as date_parser

from phg.importers.columns import PLAY_ALIASES, build_map

# Ordered: first pattern to match wins, so "line drive double play" reads as a
# double play rather than a double.
_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("triple_play", re.compile(r"\btriple play\b|\bTP\b", re.I)),
    ("double_play", re.compile(r"\bdouble play\b|\bDP\b", re.I)),
    ("home_run", re.compile(r"\bhome ?runs?\b|\bHR\b|\bgrand slam\b|\bhomers?\b", re.I)),
    ("triple", re.compile(r"\btriples?\b|\b3B\b", re.I)),
    ("double", re.compile(r"\bdoubles?\b|\bground ?rule doubles?\b|\b2B\b", re.I)),
    ("single", re.compile(r"\bsingles?\b|\b1B\b|\bbase hit\b", re.I)),
    ("strikeout", re.compile(r"\bstrikes? out\b|\bstrikeout\b|\bstruck out\b|\bK\b|\bSO\b")),
    ("walk", re.compile(r"\bwalks?\b|\bwalked\b|\bbase on balls\b|\bBB\b", re.I)),
    ("hit_by_pitch", re.compile(r"\bhit by pitch\b|\bHBP\b", re.I)),
    ("sacrifice_fly", re.compile(r"\bsac(rifice)? fly\b|\bSF\b", re.I)),
    ("sacrifice_bunt", re.compile(r"\bsac(rifice)? bunt\b|\bSAC\b", re.I)),
    ("stolen_base", re.compile(r"\bstolen base\b|\bsteals?\b|\bSB\b", re.I)),
    ("caught_stealing", re.compile(r"\bcaught stealing\b|\bCS\b", re.I)),
    ("picked_off", re.compile(r"\bpicked off\b|\bpickoff\b", re.I)),
    ("wild_pitch", re.compile(r"\bwild pitch\b|\bWP\b", re.I)),
    ("balk", re.compile(r"\bbalk\b", re.I)),
    ("fielders_choice", re.compile(r"\bfielder'?s choice\b|\bFC\b", re.I)),
    ("error_reached", re.compile(r"\breach(es|ed)? on (an )?error\b|\bROE\b", re.I)),
    ("groundout", re.compile(r"\bground(s|ed)? out\b|\bgroundout\b|\bgrounder to\b", re.I)),
    ("flyout", re.compile(r"\bfl(y|ies|ied) out\b|\bflyout\b|\bfly ball to\b", re.I)),
    ("lineout", re.compile(r"\bline(s|d)? out\b|\blineout\b|\bliner to\b", re.I)),
    ("popout", re.compile(r"\bpop(s|ped)? out\b|\bpopout\b|\bpop fly\b", re.I)),
]

_FIELDER_NAME = re.compile(r"\bto (?:the )?([A-Z][a-zA-Z'\-]+(?: [A-Z][a-zA-Z'\-]+)?)")
_SPLIT = re.compile(r"[;,/|]")


@dataclass
class PlayRow:
    sequence_no: int
    inning: int
    half: str
    play_type: str
    description: str
    is_our_offense: bool
    occurred_at: datetime | None = None
    result: str | None = None
    batter: str | None = None
    pitcher: str | None = None
    runners: list[str] = field(default_factory=list)
    putout_by: list[str] = field(default_factory=list)
    assist_by: list[str] = field(default_factory=list)
    error_by: list[str] = field(default_factory=list)
    batting_order: int | None = None
    rbi: int = 0
    runs_scored: int = 0
    outs_before: int | None = None
    balls: int | None = None
    strikes: int | None = None
    score_us: int | None = None
    score_them: int | None = None
    leverage_tag: str | None = None
    inferred_play_type: bool = False
    source_row: int = 0
    raw: dict[str, str] = field(default_factory=dict)


@dataclass
class PlayImportResult:
    plays: list[PlayRow]
    errors: list[tuple[int, str]]
    warnings: list[tuple[int, str]]
    column_map: dict[str, str]
    unmatched_headers: list[str]
    needs_side_mapping: bool = False

    @property
    def ok(self) -> bool:
        return bool(self.plays) and not self.errors


def classify(description: str, result: str | None = None) -> tuple[str, bool]:
    """Return (play_type, was_inferred)."""
    explicit = (result or "").strip().lower().replace(" ", "_")
    if explicit and explicit.replace("-", "_") in {p for p, _ in _PATTERNS}:
        return explicit.replace("-", "_"), False
    text = f"{description} {result or ''}"
    for play_type, pattern in _PATTERNS:
        if pattern.search(text):
            return play_type, True
    return "other", True


def _split_names(raw: str) -> list[str]:
    return [part.strip() for part in _SPLIT.split(raw or "") if part.strip()]


def _int(raw: str, default: int | None = None) -> int | None:
    raw = (raw or "").strip()
    if raw.lstrip("-").isdigit():
        return int(raw)
    return default


def _half(raw: str, fallback: str = "top") -> str:
    v = (raw or "").strip().lower()
    if v.startswith(("t", "^")):
        return "top"
    if v.startswith(("b", "v")):
        return "bottom"
    return fallback


def parse(
    content: str | bytes,
    *,
    our_team_name: str | None = None,
    we_bat_in: str | None = None,
) -> PlayImportResult:
    """Parse a play-by-play CSV.

    `our_team_name` matches a `team` column when present. `we_bat_in` ('top' or
    'bottom') is the fallback for files with no team column: the away team bats
    in the top of the inning. If neither is available the result is flagged
    `needs_side_mapping` and the import screen asks the coach.
    """
    if isinstance(content, bytes):
        content = content.decode("utf-8-sig", errors="replace")

    reader = csv.DictReader(io.StringIO(content))
    headers = reader.fieldnames or []
    mapping, unmatched = build_map(headers, PLAY_ALIASES)

    plays: list[PlayRow] = []
    errors: list[tuple[int, str]] = []
    warnings: list[tuple[int, str]] = []

    if "inning" not in mapping:
        errors.append((0, "no inning column found"))
    if "description" not in mapping and "play_type" not in mapping and "result" not in mapping:
        errors.append((0, "file has no description, play_type or result column to read plays from"))
    if errors:
        return PlayImportResult([], errors, warnings, mapping, unmatched)

    has_team_col = "team" in mapping
    needs_side = not has_team_col and we_bat_in not in {"top", "bottom"}

    last_inning, last_half = 1, "top"

    for line_no, row in enumerate(reader, start=2):
        get = lambda f: (row.get(mapping[f]) or "").strip() if f in mapping else ""  # noqa: E731

        inning = _int(get("inning"))
        if inning is None:
            warnings.append((line_no, "row has no inning; skipped"))
            continue
        half = _half(get("half"), last_half)
        last_inning, last_half = inning, half

        description = get("description") or get("result") or get("play_type")
        if not description:
            warnings.append((line_no, "row has no play text; skipped"))
            continue

        play_type = get("play_type").strip().lower().replace(" ", "_")
        if play_type:
            inferred = False
        else:
            play_type, inferred = classify(description, get("result") or None)

        if has_team_col and our_team_name:
            is_our_offense = get("team").strip().lower() == our_team_name.strip().lower()
        elif we_bat_in in {"top", "bottom"}:
            is_our_offense = half == we_bat_in
        else:
            is_our_offense = half == "top"     # provisional; needs_side_mapping is set

        seq = _int(get("sequence_no"), len(plays) + 1) or len(plays) + 1

        occurred_at = None
        raw_time = get("occurred_at")
        if raw_time:
            try:
                occurred_at = date_parser.parse(raw_time)
            except (ValueError, TypeError, OverflowError):
                warnings.append((line_no, f"could not read timestamp '{raw_time}'"))

        putout = _split_names(get("putout_by"))
        if not putout and not is_our_offense:
            # Many exports only name the fielder inside the narrative.
            hit = _FIELDER_NAME.search(description)
            if hit:
                putout = [hit.group(1)]

        score_us, score_them = _int(get("score_us")), _int(get("score_them"))
        leverage = None
        if score_us is not None and score_them is not None and abs(score_us - score_them) <= 1:
            leverage = "tying_run" if inning >= 5 else "risp"

        plays.append(
            PlayRow(
                sequence_no=seq,
                inning=inning,
                half=half,
                play_type=play_type,
                description=description,
                is_our_offense=is_our_offense,
                occurred_at=occurred_at,
                result=get("result") or None,
                batter=get("batter") or None,
                pitcher=get("pitcher") or None,
                runners=_split_names(get("runners")),
                putout_by=putout,
                assist_by=_split_names(get("assist_by")),
                error_by=_split_names(get("error_by")),
                batting_order=_int(get("batting_order")),
                rbi=_int(get("rbi"), 0) or 0,
                runs_scored=_int(get("runs_scored"), 0) or 0,
                outs_before=_int(get("outs_before")),
                balls=_int(get("balls")),
                strikes=_int(get("strikes")),
                score_us=score_us,
                score_them=score_them,
                leverage_tag=leverage,
                inferred_play_type=inferred,
                source_row=line_no,
                raw={k: (v or "") for k, v in row.items()},
            )
        )

    if not plays:
        errors.append((0, "file contained no readable plays"))

    inferred_count = sum(1 for p in plays if p.inferred_play_type)
    if inferred_count:
        warnings.append((0, f"{inferred_count} of {len(plays)} play types were inferred from text"))
    if not any(p.occurred_at for p in plays):
        warnings.append((0, "no timestamps in this file; plays will be paced from first pitch"))

    del last_inning
    return PlayImportResult(plays, errors, warnings, mapping, unmatched, needs_side_mapping=needs_side)
