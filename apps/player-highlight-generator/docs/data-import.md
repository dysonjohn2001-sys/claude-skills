# Data import

## The GameChanger position

**This application contains no GameChanger API client and no scraper.** There is
no code here that authenticates to GameChanger, no endpoint list, no HTML
parsing of their pages, and no credential storage for their service.

That is a design constraint, not an oversight. Unofficial API clients for
scorekeeping services break on every deployment, violate terms of service, and
put a coach's account at risk for a feature they did not ask for. Scraping a
platform full of minors' data is worse.

What the application does instead: **read what a coach exports and uploads
themselves.** A coach with an account on any scorekeeping platform can export
their own team's data. That export is the input. Video is uploaded the same way.

If GameChanger, or any other platform, publishes a documented API with a real
authorisation flow, adding a connector for it is a contained piece of work: the
importers already normalise everything to `plays` and `play_participants`, and
a connector would populate those tables the same way the CSV path does. Until
then, the coach-upload path is the only path.

---

## Roster CSV

### Minimum

Either a single name column, or separate first and last name columns.

```csv
name
Jake Smith
Marcus Hernandez
```

### Typical

```csv
Number,Name,Position,Bats,Throws,Batting Order,Parent Name,Parent Email,Parent Phone
7,"Smith, Jake",SS/P,R,R,1,Dana Smith,dana.smith@example.com,555-0101
12,"Hernandez, Marcus",2B,L,R,2,Rosa Hernandez,rosa.h@example.com,555-0102
```

### Fields and what is accepted

| Field | Header spellings recognised | Notes |
|---|---|---|
| Name | `name`, `player`, `player_name`, `full_name`, `athlete` | `First Last` or `Last, First` |
| First / last | `first_name`/`first`, `last_name`/`last`/`surname` | Use instead of a single name column |
| Jersey | `jersey`, `number`, `no`, `num`, `uniform`, `uni` | Leading `#` stripped. Text, so `07` and `7` differ |
| Positions | `position`, `positions`, `pos` | Split on `,` `;` `/`. Unknown values warned and ignored |
| Bats | `bats`, `bat`, `b` | L, R or S |
| Throws | `throws`, `throw`, `t` | L or R |
| Batting order | `batting_order`, `order`, `spot`, `bo` | |
| Birth year | `birth_year`, `grad_year`, `yob` | Year only. Full dates are not stored |
| Guardian | `guardian`, `parent`, `contact` | Plus `_email` and `_phone` variants |

Accents, name suffixes (`Jr`, `III`) and punctuation are normalised for matching
but preserved for display.

### Errors versus warnings

**Errors reject the file.**

- No name column at all.
- A duplicate jersey number among active players, reported with both row
  numbers. Two players sharing #7 breaks every number-based check downstream.

**Warnings import anyway and tell you.**

- A player with no last name (matching will be weaker).
- A non-numeric jersey (kept as text).
- An unrecognised position or bats/throws value (ignored).

### Preview first

The roster import screen has a "Preview only" checkbox, ticked by default. It
parses the file, shows what it would import and everything it could not read,
and saves nothing.

Offline, without the application running:

```bash
cd worker
python -m phg.cli check-roster ../samples/roster.csv
```

### Re-importing

Matching is on jersey number first, then on name, so a corrected roster
**updates** players rather than duplicating them. Positions are replaced
wholesale. Guardians are staged, never invited: appearing in a spreadsheet does
not create an account or imply consent.

---

## Play-by-play CSV

### Minimum

An inning column and something describing the play.

```csv
inning,play
1,Jake Smith singles to right
1,Marcus Hernandez walks
2,Owen Brooks hits a home run to center
```

### Typical

```csv
Seq,Inning,Half,Timestamp,Team,Batting Order,Batter,Pitcher,Description,Result,RBI,Runs,Outs,Score Us,Score Them,Putout,Assist
1,1,top,2026-04-18T10:04:12-04:00,Riverside Rays,1,Jake Smith,A. Jones,Jake Smith doubles to left field,double,0,0,0,0,0,,
4,1,bottom,2026-04-18T10:15:22-04:00,Northside Owls,,B. Carter,Liam Nguyen,B. Carter grounds out to Jake Smith,groundout,0,0,0,1,0,Jake Smith,
```

### Fields

| Field | Header spellings | Notes |
|---|---|---|
| Inning | `inning`, `inn` | **Required** |
| Half | `half`, `top_bottom`, `tb` | `t`/`^` → top, `b`/`v` → bottom. Carries forward if blank |
| Timestamp | `timestamp`, `time`, `clock`, `datetime` | **The single most valuable column** |
| Team | `team`, `batting_team`, `side` | Which team is batting |
| Description | `description`, `play`, `text`, `narrative` | Free text; play type is derived from it if needed |
| Play type | `play_type`, `type`, `event` | Used directly when present |
| Batter / pitcher | `batter`, `hitter` / `pitcher` | |
| Runners | `runners`, `baserunners`, `on_base` | Split on `,` `;` `/` `|` |
| Fielders | `putout`, `assist`, `error` (+ `_by`) | |
| Batting order | `batting_order`, `order`, `spot` | Cross-checks the batter |
| RBI / runs / outs / balls / strikes | as named | Feed ranking |
| Score | `score_us`/`home_score`, `score_them`/`away_score` | Feed the scorebug and leverage |

### The two things that matter most

**Timestamps.** With them, each play is located in the footage directly. Without
them, plays are paced from first pitch at nine minutes per half inning, which is
a guess, and confidence drops accordingly. If your scorekeeping app can export
timestamps, export them.

**Which team is batting.** Getting this wrong assigns every clip to the wrong
side of the ball. If the file has a team column, it is matched against the team
name. If it does not, the import screen asks which half-inning your team bats in,
and the result is flagged so you know to check a few clips.

### Play-type inference

With no `play_type` column, the type is derived from the description text by an
ordered pattern list. Order matters: "grounds into a 6-4-3 double play" is a
double play, not a double.

Recognised: home run, triple, double, single, walk, hit by pitch, strikeout,
sacrifice fly, sacrifice bunt, stolen base, caught stealing, picked off, wild
pitch, balk, fielder's choice, reached on error, groundout, flyout, lineout,
popout, double play, triple play.

Every inferred type is counted and reported in the import summary, and the count
appears as a warning, so a coach knows how much of the file was guessed at.

On defensive plays with no fielder column, the fielder is pulled out of the
narrative: "grounds out to Jake Smith" credits Jake Smith with the putout.

### Re-importing

Re-importing **replaces** a game's plays rather than appending, because a coach
re-uploads precisely when the first file was wrong.

Offline check:

```bash
cd worker
python -m phg.cli check-plays ../samples/plays.csv --team "Riverside Rays"
python -m phg.cli check-plays ../samples/plays.csv --we-bat-in top
```

---

## Video

MP4, MOV, M4V, MKV and AVI. Files are streamed to disk rather than buffered: a
full-game recording is routinely several gigabytes, and holding one in memory
would take the application down. The default cap is 16 GB, enough for a long
game at 1080p60 from a phone.

On arrival each file is probed for duration, resolution, frame rate, audio
presence and recording start time. Rotation metadata is applied, so a
phone-shot vertical video reports its real dimensions.

```bash
cd worker
python -m phg.cli probe /path/to/game.mp4
```

If that reports no recording start time, matching will depend on sync points set
by hand in the review screen. It is worth running once on any new camera.

Multiple files per game are fine. Each gets its own timeline and its own sync
anchors, and the matcher places each play in whichever video actually contains
it.

### Single-play exports

A clip exported from a scorekeeping app is usually one play, about 20 to 30
seconds, opening with a branded title card that names the play. Upload these
with the type set to **Individual clip**.

Two things to know about them.

The title card is detected and dropped automatically. It is a run of perfectly
still frames followed by a hard cut, and real footage is never perfectly still,
so the two are distinguishable without any configuration. On a measured example
the card ran 0 to 4.0 seconds and the cut changed 93% of the pixels in one
frame.

The recording timestamp in an exported file may be the export time rather than
the moment of the play. Run `phg probe` on one and compare the reported
`recording_started_at` against when that play actually happened. If they
disagree, the clip still works, but assign it to its play in the review screen
rather than relying on automatic matching. Matching a one-play clip to its play
by reading the title card is the top item in
[the roadmap](roadmap.md).

---

## One source of truth for column names

The header alias tables live in `shared/column-aliases.json`. Both the Python
importer (`worker/phg/importers/columns.py`) and the TypeScript importer
(`web/src/lib/csv.ts`) read that file, so adding a vendor's header spelling is a
one-line change in one place rather than two implementations drifting apart.

To teach the importer a new spelling, add it to the relevant array:

```json
{
  "roster": {
    "jersey_number": ["jersey", "number", "no", "num", "uniform", "uni", "shirt_no"]
  }
}
```

Spellings are normalised before comparison: lowercased, with runs of
non-alphanumeric characters collapsed to underscores. `Jersey #` and `jersey_no`
both normalise to `jersey_no`.
