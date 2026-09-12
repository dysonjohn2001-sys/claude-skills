"""Turn a game's play-by-play plus one or more videos into clip candidates.

Order of operations, and the reason for it:

  1. Fit a wall-clock -> video-time mapping per media asset (timeline.py).
  2. Fill in missing play timestamps by interpolating between the ones we have.
  3. For each play, decide which of our players earned a highlight and in what
     category.
  4. Resolve each credited name against the roster (name_resolver.py), using
     batting order as a cross-check rather than a guess.
  5. Score the assignment (confidence.py) and cut a window with roll.

Jersey recognition is not in this file. It runs afterwards, only on the clips
whose confidence landed in the uncertain band, and only ever adjusts a score
this module already produced.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from phg.matching.confidence import ConfidenceResult, compute
from phg.matching.name_resolver import NameResolver
from phg.matching.timeline import Timeline, TimelineError
from phg.models import (
    BASERUNNING_PLAYS,
    ClipCandidate,
    MediaAsset,
    Participant,
    Play,
    Player,
)

# Typical wall-clock length of a half inning in youth baseball, used only to
# spread plays that carry no timestamp of their own.
HALF_INNING_SECONDS = 9 * 60.0


@dataclass
class MatchReport:
    candidates: list[ClipCandidate]
    skipped: list[tuple[str, str]]          # (play_id, reason)
    anchor_count: int
    plays_with_inferred_time: int
    # Every credited participant with the identity we resolved for them. These
    # are written back to play_participants so the derived statistics views -
    # and therefore the stat overlays and intro cards - have player ids to join
    # on. Without this the scorebook knows who batted and the database does not.
    participants: list[Participant] = field(default_factory=list)


class PlayMatcher:
    def __init__(
        self,
        *,
        players: list[Player],
        pre_roll: float = 5.0,
        post_roll: float = 8.0,
        base_window_seconds: float = 25.0,
        drift_seconds_per_minute: float = 0.35,
    ) -> None:
        self.players = {p.id: p for p in players}
        self.resolver = NameResolver(players)
        self.pre_roll = pre_roll
        self.post_roll = post_roll
        self.base_window = base_window_seconds
        self.drift_per_minute = drift_seconds_per_minute

    # -- entry point ------------------------------------------------------

    def match_game(
        self,
        plays: list[Play],
        assets: list[MediaAsset],
        *,
        first_pitch_at: datetime | None = None,
    ) -> MatchReport:
        plays = sorted(plays, key=lambda p: p.sequence_no)
        timed, inferred_count = self._fill_times(plays, first_pitch_at)

        timelines: list[tuple[MediaAsset, Timeline]] = []
        skipped: list[tuple[str, str]] = []
        for asset in assets:
            try:
                timelines.append((asset, Timeline(
                    asset,
                    base_window_seconds=self.base_window,
                    drift_seconds_per_minute=self.drift_per_minute,
                )))
            except TimelineError as exc:
                skipped.append((asset.id, str(exc)))

        candidates: list[ClipCandidate] = []
        resolved: list[Participant] = []
        for play in plays:
            when = timed.get(play.id)
            if when is None:
                skipped.append((play.id, "no timestamp and none could be inferred"))
                continue

            placed = self._place(play, when, timelines)
            if placed is None:
                skipped.append((play.id, "projected outside every uploaded video"))
                continue
            asset, timeline, projection = placed

            participants = self.participants_for(play)
            resolved.extend(participants)
            for participant in participants:
                if participant.player_id is None:
                    continue
                player = self.players.get(participant.player_id)
                if player is None:
                    continue
                category = self.category_for(play, participant.role)
                if category is None:
                    continue

                conf = self._score(play, participant, player, projection)
                start, end = timeline.clamp(
                    projection.video_seconds - self.pre_roll,
                    projection.video_seconds + self.post_roll,
                )
                candidates.append(
                    ClipCandidate(
                        play_id=play.id,
                        player_id=player.id,
                        media_asset_id=asset.id,
                        category=category,
                        source_start_seconds=round(start, 3),
                        source_end_seconds=round(end, 3),
                        pre_roll_seconds=self.pre_roll,
                        post_roll_seconds=self.post_roll,
                        match_method="schedule",
                        match_confidence=conf.score,
                        confidence_factors=conf.as_dict(),
                        title=self._title(play, player, category),
                    )
                )

        # Plays that never reached a timeline still resolved their names, and
        # those identities are worth keeping for the statistics.
        placed_ids = {p.play_id for p in resolved}
        for play in plays:
            if play.id not in placed_ids:
                resolved.extend(self.participants_for(play))

        return MatchReport(
            candidates=candidates,
            skipped=skipped,
            anchor_count=sum(t.anchor_count for _, t in timelines),
            plays_with_inferred_time=inferred_count,
            participants=resolved,
        )

    # -- timestamps -------------------------------------------------------

    def _fill_times(
        self, plays: list[Play], first_pitch_at: datetime | None
    ) -> tuple[dict[str, datetime], int]:
        """Give every play a wall-clock instant, interpolating where needed.

        Exports vary: some carry a timestamp per play, some only per half
        inning, some none at all. Known timestamps are kept exactly; unknown
        ones are placed by linear interpolation on sequence number between the
        nearest known neighbours, and extrapolated by inning pacing outside
        them.
        """
        known = [(i, p) for i, p in enumerate(plays) if p.occurred_at is not None]
        out: dict[str, datetime] = {p.id: p.occurred_at for _, p in known if p.occurred_at}
        inferred = 0

        if not known:
            if first_pitch_at is None:
                return out, 0
            # Nothing but a first-pitch time: pace by inning and half.
            for p in plays:
                half_index = (p.inning - 1) * 2 + (1 if p.half == "bottom" else 0)
                offset = half_index * HALF_INNING_SECONDS
                out[p.id] = first_pitch_at + timedelta(seconds=offset)
                inferred += 1
            return out, inferred

        for idx, play in enumerate(plays):
            if play.id in out:
                continue
            before = max((k for k in known if k[0] < idx), default=None, key=lambda k: k[0])
            after = min((k for k in known if k[0] > idx), default=None, key=lambda k: k[0])

            if before and after:
                b_i, b_p = before
                a_i, a_p = after
                span = (a_p.occurred_at - b_p.occurred_at).total_seconds()   # type: ignore[operator]
                frac = (idx - b_i) / (a_i - b_i)
                out[play.id] = b_p.occurred_at + timedelta(seconds=span * frac)  # type: ignore[operator]
            elif before:
                b_i, b_p = before
                out[play.id] = b_p.occurred_at + timedelta(seconds=45.0 * (idx - b_i))  # type: ignore[operator]
            elif after:
                a_i, a_p = after
                out[play.id] = a_p.occurred_at - timedelta(seconds=45.0 * (a_i - idx))  # type: ignore[operator]
            else:
                continue
            inferred += 1

        return out, inferred

    def _place(
        self,
        play: Play,
        when: datetime,
        timelines: list[tuple[MediaAsset, Timeline]],
    ):
        """Pick the video that actually contains this instant."""
        best = None
        for asset, timeline in timelines:
            projection = timeline.project(when)
            t = projection.video_seconds
            if -projection.uncertainty_seconds <= t <= asset.duration_seconds + projection.uncertainty_seconds:
                # Prefer the asset whose interior the play lands furthest inside.
                margin = min(t, asset.duration_seconds - t)
                if best is None or margin > best[0]:
                    best = (margin, asset, timeline, projection)
        if best is None:
            return None
        _, asset, timeline, projection = best
        return asset, timeline, projection

    # -- participants and categories --------------------------------------

    def participants_for(self, play: Play) -> list[Participant]:
        """Who on our team earned a highlight from this play.

        Only our own players are ever clipped. On plays where we are batting,
        that is the batter and any of our runners; on plays where we are in the
        field, it is our pitcher and the credited fielders.
        """
        out: list[Participant] = []
        expected_order = play.raw_row.get("batting_order")
        expected_order = int(expected_order) if expected_order not in (None, "") else None

        if play.is_our_offense:
            res = self.resolver.resolve(
                play.batter_name_raw, expected_batting_order=expected_order, inning=play.inning
            )
            out.append(
                Participant(
                    play_id=play.id,
                    role="batter",
                    player_id=res.player_id,
                    raw_name=play.batter_name_raw,
                    confidence=res.confidence,
                    method=res.method,
                )
            )
            for raw in play.raw_row.get("runners") or []:
                r = self.resolver.resolve(raw, inning=play.inning)
                out.append(
                    Participant(
                        play_id=play.id, role="runner", player_id=r.player_id,
                        raw_name=raw, confidence=r.confidence, method=r.method,
                    )
                )
        else:
            res = self.resolver.resolve(play.pitcher_name_raw, inning=play.inning)
            out.append(
                Participant(
                    play_id=play.id, role="pitcher", player_id=res.player_id,
                    raw_name=play.pitcher_name_raw, confidence=res.confidence, method=res.method,
                )
            )
            for role_key, role in (
                ("putout_by", "fielder_putout"),
                ("assist_by", "fielder_assist"),
                ("error_by", "fielder_error"),
            ):
                for raw in play.raw_row.get(role_key) or []:
                    r = self.resolver.resolve(raw, inning=play.inning)
                    out.append(
                        Participant(
                            play_id=play.id, role=role, player_id=r.player_id,
                            raw_name=raw, confidence=r.confidence, method=r.method,
                        )
                    )
        return out

    @staticmethod
    def category_for(play: Play, role: str) -> str | None:
        if role == "batter":
            return "baserunning" if play.play_type in BASERUNNING_PLAYS else "offense"
        if role == "runner":
            return "baserunning"
        if role == "pitcher":
            return "pitching"
        if role in {"fielder_putout", "fielder_assist", "fielder_error", "catcher"}:
            return "defense"
        return None

    # -- scoring ----------------------------------------------------------

    def _score(self, play: Play, participant: Participant, player: Player, projection) -> ConfidenceResult:
        expected_order = play.raw_row.get("batting_order")
        expected_order = int(expected_order) if expected_order not in (None, "") else None
        agrees = (
            self.resolver.confirms_batting_order(player.id, expected_order)
            if participant.role == "batter"
            else None
        )
        return compute(
            name_confidence=participant.confidence,
            uncertainty_seconds=projection.uncertainty_seconds,
            anchor_count=projection.anchor_count,
            batting_order_agrees=agrees,
            in_lineup=player.is_in_game(play.inning),
            play_type=play.play_type,
            role=participant.role,
            positions=player.positions,
        )

    @staticmethod
    def _title(play: Play, player: Player, category: str) -> str:
        half = "Top" if play.half == "top" else "Bot"
        label = play.result or play.play_type.replace("_", " ").title()
        return f"{player.display_name} - {label} ({half} {play.inning})"
