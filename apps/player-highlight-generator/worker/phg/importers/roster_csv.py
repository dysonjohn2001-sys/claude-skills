"""Import a roster CSV into player records.

Accepts either `first_name,last_name` or a single `name` column, and carries
optional guardian contact columns so a coach can seed parent access in the same
upload. Guardian rows are staged, never auto-invited: an invitation goes out
only after the coach confirms it and consent is on file.
"""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass, field

from phg.importers.columns import ROSTER_ALIASES, build_map

VALID_POSITIONS = {"P", "C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "DH", "EH", "UTIL"}


@dataclass
class GuardianRow:
    full_name: str
    email: str
    phone: str | None = None


@dataclass
class PlayerRow:
    first_name: str
    last_name: str
    jersey_number: str | None = None
    positions: list[str] = field(default_factory=list)
    bats: str | None = None
    throws: str | None = None
    birth_year: int | None = None
    batting_order: int | None = None
    guardians: list[GuardianRow] = field(default_factory=list)
    source_row: int = 0


@dataclass
class RosterImportResult:
    players: list[PlayerRow]
    errors: list[tuple[int, str]]
    warnings: list[tuple[int, str]]
    column_map: dict[str, str]
    unmatched_headers: list[str]

    @property
    def ok(self) -> bool:
        return bool(self.players) and not self.errors


def _split_name(full: str) -> tuple[str, str]:
    full = full.strip()
    if "," in full:
        last, _, first = full.partition(",")
        return first.strip(), last.strip()
    parts = full.split()
    if len(parts) == 1:
        return parts[0], ""
    return " ".join(parts[:-1]), parts[-1]


def _positions(raw: str) -> tuple[list[str], list[str]]:
    out, bad = [], []
    for token in raw.replace(";", ",").replace("/", ",").split(","):
        token = token.strip().upper()
        if not token:
            continue
        if token in VALID_POSITIONS:
            out.append(token)
        else:
            bad.append(token)
    return out, bad


def parse(content: str | bytes) -> RosterImportResult:
    if isinstance(content, bytes):
        content = content.decode("utf-8-sig", errors="replace")

    reader = csv.DictReader(io.StringIO(content))
    headers = reader.fieldnames or []
    mapping, unmatched = build_map(headers, ROSTER_ALIASES)

    players: list[PlayerRow] = []
    errors: list[tuple[int, str]] = []
    warnings: list[tuple[int, str]] = []

    has_name = "full_name" in mapping or ("first_name" in mapping and "last_name" in mapping)
    if not has_name:
        errors.append((0, "no name column found; expected 'name' or 'first_name' + 'last_name'"))
        return RosterImportResult([], errors, warnings, mapping, unmatched)

    seen_jerseys: dict[str, int] = {}

    for line_no, row in enumerate(reader, start=2):
        get = lambda f: (row.get(mapping[f]) or "").strip() if f in mapping else ""  # noqa: E731

        if "first_name" in mapping and "last_name" in mapping:
            first, last = get("first_name"), get("last_name")
        else:
            first, last = _split_name(get("full_name"))

        if not first and not last:
            continue                       # blank spacer row
        if not last:
            warnings.append((line_no, f"'{first}' has no last name; matching will be weaker"))

        jersey = get("jersey_number") or None
        if jersey:
            jersey = jersey.lstrip("#").strip()
            if not jersey.isdigit():
                warnings.append((line_no, f"jersey '{jersey}' is not numeric; kept as text"))
            elif jersey in seen_jerseys:
                errors.append(
                    (line_no, f"jersey #{jersey} is already used on row {seen_jerseys[jersey]}")
                )
            else:
                seen_jerseys[jersey] = line_no

        positions, bad = _positions(get("positions"))
        for token in bad:
            warnings.append((line_no, f"unrecognised position '{token}' ignored"))

        bats = (get("bats") or "").upper()[:1] or None
        if bats and bats not in {"L", "R", "S"}:
            warnings.append((line_no, f"unrecognised bats value '{bats}' ignored"))
            bats = None
        throws = (get("throws") or "").upper()[:1] or None
        if throws and throws not in {"L", "R"}:
            warnings.append((line_no, f"unrecognised throws value '{throws}' ignored"))
            throws = None

        birth_year = None
        if get("birth_year").isdigit():
            birth_year = int(get("birth_year"))

        batting_order = None
        if get("batting_order").isdigit():
            batting_order = int(get("batting_order"))

        guardians: list[GuardianRow] = []
        g_email = get("guardian_email")
        if g_email:
            guardians.append(
                GuardianRow(
                    full_name=get("guardian_name") or f"{first} {last} guardian",
                    email=g_email,
                    phone=get("guardian_phone") or None,
                )
            )

        players.append(
            PlayerRow(
                first_name=first, last_name=last, jersey_number=jersey,
                positions=positions, bats=bats, throws=throws, birth_year=birth_year,
                batting_order=batting_order, guardians=guardians, source_row=line_no,
            )
        )

    if not players:
        errors.append((0, "file contained no player rows"))

    return RosterImportResult(players, errors, warnings, mapping, unmatched)
