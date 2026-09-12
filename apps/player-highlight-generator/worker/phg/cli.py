"""Command line entry points.

    python -m phg.cli worker                       run the job loop
    python -m phg.cli probe game.mp4               show what ffprobe sees
    python -m phg.cli check-roster roster.csv      dry-run a roster import
    python -m phg.cli check-plays plays.csv        dry-run a play-by-play import
    python -m phg.cli match --game <uuid>          re-run matching for one game
    python -m phg.cli render --reel <uuid>         re-render one reel
    python -m phg.cli card --name "Jake Smith"     preview an intro card PNG

The `check-*` commands need no database and no FFmpeg. They exist so a coach
can be told exactly what is wrong with a CSV before anything is uploaded.
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path


def _print_issues(label: str, issues: list[tuple[int, str]]) -> None:
    if not issues:
        return
    print(f"\n{label}:")
    for line_no, message in issues:
        where = f"row {line_no}" if line_no else "file"
        print(f"  {where}: {message}")


def cmd_check_roster(args: argparse.Namespace) -> int:
    from phg.importers import roster_csv

    result = roster_csv.parse(Path(args.path).read_bytes())
    print(f"Parsed {len(result.players)} players from {args.path}")
    print(f"Columns recognised: {json.dumps(result.column_map, indent=2)}")
    if result.unmatched_headers:
        print(f"Ignored columns: {', '.join(result.unmatched_headers)}")
    for p in result.players[:10]:
        jersey = f"#{p.jersey_number}" if p.jersey_number else "no number"
        print(f"  {p.first_name} {p.last_name:<16} {jersey:<11} {'/'.join(p.positions) or '-'}")
    if len(result.players) > 10:
        print(f"  ... and {len(result.players) - 10} more")
    _print_issues("Errors", result.errors)
    _print_issues("Warnings", result.warnings)
    return 0 if result.ok else 1


def cmd_check_plays(args: argparse.Namespace) -> int:
    from phg.importers import playbyplay_csv

    result = playbyplay_csv.parse(
        Path(args.path).read_bytes(),
        our_team_name=args.team,
        we_bat_in=args.we_bat_in,
    )
    print(f"Parsed {len(result.plays)} plays from {args.path}")
    print(f"Columns recognised: {json.dumps(result.column_map, indent=2)}")
    if result.needs_side_mapping:
        print("\n  ATTENTION: this file does not say which team is batting.")
        print("  Re-run with --team 'Your Team Name' or --we-bat-in top|bottom.")
    counts: dict[str, int] = {}
    for p in result.plays:
        counts[p.play_type] = counts.get(p.play_type, 0) + 1
    print("\nPlay types:")
    for play_type, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {play_type:<20} {n}")
    _print_issues("Errors", result.errors)
    _print_issues("Warnings", result.warnings)
    return 0 if result.ok else 1


def cmd_probe(args: argparse.Namespace) -> int:
    from phg.video.probe import ProbeError, probe

    try:
        result = probe(args.path)
    except ProbeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({
        "duration_seconds": result.duration_seconds,
        "resolution": f"{result.width}x{result.height}",
        "fps": result.fps,
        "has_audio": result.has_audio,
        "video_codec": result.video_codec,
        "recording_started_at": result.recording_started_at.isoformat() if result.recording_started_at else None,
        "orientation": "vertical" if result.is_vertical else "horizontal",
    }, indent=2))
    if result.recording_started_at is None:
        print(
            "\nNo recording start time in this file. Set one sync anchor in the review "
            "screen or matching will rely on play order alone.",
            file=sys.stderr,
        )
    return 0


def cmd_match(args: argparse.Namespace) -> int:
    from phg import config
    from phg.db import Database

    cfg = config.load()
    db = Database(cfg.database_url)
    job_id = db.enqueue("match_plays", "game", args.game, {})
    print(f"queued match_plays job {job_id} for game {args.game}")
    return 0


def cmd_render(args: argparse.Namespace) -> int:
    from phg import config
    from phg.db import Database

    cfg = config.load()
    db = Database(cfg.database_url)
    job_id = db.enqueue("render_reel", "reel", args.reel, {})
    print(f"queued render_reel job {job_id} for reel {args.reel}")
    return 0


def cmd_card(args: argparse.Namespace) -> int:
    from phg.video.overlays import BrandTheme, PlayerCardData, render_intro_card

    path = render_intro_card(
        PlayerCardData(
            display_name=args.name,
            jersey_number=args.number,
            positions=args.positions.split(",") if args.positions else [],
            subtitle=args.subtitle,
            stat_lines=[("AVG", ".412"), ("H", "21"), ("RBI", "18"), ("HR", "3")],
        ),
        BrandTheme(
            team_name=args.subtitle or "Team",
            primary_color=args.primary,
            secondary_color=args.secondary,
        ),
        args.out,
        args.aspect,
    )
    print(f"wrote {path}")
    return 0


def cmd_worker(_: argparse.Namespace) -> int:
    from phg.worker import main

    main()
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="phg", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--verbose", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("worker", help="run the job loop").set_defaults(fn=cmd_worker)

    p = sub.add_parser("probe", help="show media metadata")
    p.add_argument("path")
    p.set_defaults(fn=cmd_probe)

    p = sub.add_parser("check-roster", help="dry-run a roster CSV")
    p.add_argument("path")
    p.set_defaults(fn=cmd_check_roster)

    p = sub.add_parser("check-plays", help="dry-run a play-by-play CSV")
    p.add_argument("path")
    p.add_argument("--team", help="our team name as it appears in the file")
    p.add_argument("--we-bat-in", choices=["top", "bottom"],
                   help="which half we bat in, when the file has no team column")
    p.set_defaults(fn=cmd_check_plays)

    p = sub.add_parser("match", help="queue a re-match for one game")
    p.add_argument("--game", required=True)
    p.set_defaults(fn=cmd_match)

    p = sub.add_parser("render", help="queue a re-render for one reel")
    p.add_argument("--reel", required=True)
    p.set_defaults(fn=cmd_render)

    p = sub.add_parser("card", help="preview a player introduction card")
    p.add_argument("--name", required=True)
    p.add_argument("--number", default="7")
    p.add_argument("--positions", default="SS,P")
    p.add_argument("--subtitle", default="Spring 2026")
    p.add_argument("--primary", default="#0F2B5B")
    p.add_argument("--secondary", default="#C8102E")
    p.add_argument("--aspect", default="16:9", choices=["16:9", "9:16"])
    p.add_argument("--out", default="intro-card.png")
    p.set_defaults(fn=cmd_card)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)-7s %(name)s %(message)s",
    )
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
