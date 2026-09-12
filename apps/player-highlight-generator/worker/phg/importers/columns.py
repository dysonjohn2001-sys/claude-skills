"""Header matching shared by the CSV importers.

Scorekeeping exports rename columns constantly. Rather than hardcode one
vendor's header row, each logical field carries a list of aliases, and anything
unmatched is surfaced to the coach as a mapping question in the import screen.
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

_NORMALIZE = re.compile(r"[^a-z0-9]+")

# The alias tables live in shared/column-aliases.json so the TypeScript importer
# in web/ and this one cannot drift apart. Adding a vendor's header spelling is
# a one-line change in one file.
# Resolves to <repo>/shared in a checkout and to /shared in the worker image.
# PHG_COLUMN_ALIASES overrides both for unusual deployment layouts.
_ALIAS_FILE = Path(
    os.environ.get(
        "PHG_COLUMN_ALIASES",
        Path(__file__).resolve().parents[3] / "shared" / "column-aliases.json",
    )
)


def norm(header: str) -> str:
    return _NORMALIZE.sub("_", (header or "").strip().lower()).strip("_")


def _load_aliases() -> dict[str, dict[str, list[str]]]:
    with _ALIAS_FILE.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return {"roster": data["roster"], "play_by_play": data["play_by_play"]}


_ALIASES = _load_aliases()


ROSTER_ALIASES: dict[str, list[str]] = _ALIASES["roster"]
PLAY_ALIASES: dict[str, list[str]] = _ALIASES["play_by_play"]


def build_map(headers: list[str], aliases: dict[str, list[str]]) -> tuple[dict[str, str], list[str]]:
    """Return (logical_field -> actual_header, unmatched_headers)."""
    normalized = {norm(h): h for h in headers}
    mapping: dict[str, str] = {}
    claimed: set[str] = set()

    for field, options in aliases.items():
        for option in options:
            if option in normalized and normalized[option] not in claimed:
                mapping[field] = normalized[option]
                claimed.add(normalized[option])
                break

    unmatched = [h for h in headers if h not in claimed]
    return mapping, unmatched
