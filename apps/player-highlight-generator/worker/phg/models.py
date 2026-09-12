"""Plain domain objects.

The matching engine operates entirely on these, never on a database cursor, so
every rule in it is unit-testable without a running PostgreSQL.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

# Play types the app recognises, grouped by the highlight category they belong
# to for the player in the given role.
OFFENSE_PLAYS = {
    "single", "double", "triple", "home_run", "walk", "hit_by_pitch",
    "sacrifice_fly", "sacrifice_bunt", "fielders_choice", "error_reached",
    "groundout", "flyout", "lineout", "popout", "strikeout",
}
BASERUNNING_PLAYS = {
    "stolen_base", "caught_stealing", "advanced_on_error", "scored",
    "picked_off", "tagged_out", "advanced_on_wild_pitch",
}
PITCHING_PLAYS = {"strikeout", "walk", "hit_by_pitch", "wild_pitch", "balk"}
DEFENSE_ROLES = {"fielder_putout", "fielder_assist", "fielder_error", "catcher"}


@dataclass(frozen=True)
class Player:
    id: str
    first_name: str
    last_name: str
    preferred_name: str | None = None
    jersey_number: str | None = None
    positions: tuple[str, ...] = ()
    batting_order: int | None = None        # for the game being matched
    entered_inning: int = 1
    exited_inning: int | None = None

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def display_name(self) -> str:
        return f"{self.preferred_name or self.first_name} {self.last_name}"

    def is_in_game(self, inning: int) -> bool:
        if inning < self.entered_inning:
            return False
        if self.exited_inning is not None and inning > self.exited_inning:
            return False
        return True


@dataclass(frozen=True)
class Play:
    id: str
    game_id: str
    sequence_no: int
    inning: int
    half: str                                # 'top' | 'bottom'
    play_type: str
    description: str
    is_our_offense: bool
    occurred_at: datetime | None = None
    batter_name_raw: str | None = None
    pitcher_name_raw: str | None = None
    result: str | None = None
    rbi: int = 0
    runs_scored: int = 0
    outs_before: int | None = None
    score_us: int | None = None
    score_them: int | None = None
    leverage_tag: str | None = None
    raw_row: dict[str, Any] = field(default_factory=dict)

    @property
    def is_our_defense(self) -> bool:
        return not self.is_our_offense


@dataclass(frozen=True)
class Participant:
    """A player credited with a role on a play, plus how we decided that."""

    play_id: str
    role: str
    player_id: str | None
    raw_name: str | None = None
    raw_jersey_number: str | None = None
    confidence: float = 0.0
    method: str = "unresolved"


@dataclass(frozen=True)
class SyncAnchor:
    """Ties a moment in a video file to a moment in game wall-clock time."""

    video_seconds: float
    wall_clock_at: datetime


@dataclass(frozen=True)
class MediaAsset:
    id: str
    game_id: str
    kind: str                                # 'full_game' | 'clip'
    path: str
    duration_seconds: float
    fps: float = 30.0
    width: int = 1920
    height: int = 1080
    has_audio: bool = True
    recording_started_at: datetime | None = None
    anchors: tuple[SyncAnchor, ...] = ()


@dataclass(frozen=True)
class JerseyObservation:
    video_seconds: float
    digits: str
    ocr_confidence: float
    bbox: tuple[int, int, int, int] | None = None


@dataclass
class ClipCandidate:
    """One proposed highlight: a player, a play and a window of source video."""

    play_id: str | None
    player_id: str
    media_asset_id: str
    category: str                            # offense | defense | pitching | baserunning
    source_start_seconds: float
    source_end_seconds: float
    pre_roll_seconds: float
    post_roll_seconds: float
    match_method: str                        # schedule | schedule_jersey | jersey_only | manual
    match_confidence: float
    confidence_factors: dict[str, float] = field(default_factory=dict)
    rank_score: float = 0.0
    rank_factors: dict[str, float] = field(default_factory=dict)
    title: str = ""

    @property
    def duration(self) -> float:
        return self.source_end_seconds - self.source_start_seconds

    @property
    def needs_review(self) -> bool:
        return self.match_confidence < 0.80


@dataclass(frozen=True)
class Segment:
    """A kept or discarded sub-window inside a clip, relative to clip start."""

    start: float
    end: float
    keep: bool
    motion_score: float = 0.0
    reason: str = ""

    @property
    def duration(self) -> float:
        return self.end - self.start
