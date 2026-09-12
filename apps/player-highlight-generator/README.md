# Player Highlight Generator

A private web application that turns a youth baseball team's game footage and
scorebook into a separate highlight reel for every player.

A coach uploads the recording and exports the play-by-play from whatever
scorekeeping app the team already uses. The application works out which moments
in the footage belong to which child, cuts them, ranks them, brands them, and
produces per-player reels the coach can share with that child's family and
nobody else.

**Status: working MVP.** 141 automated tests pass, including eight that run
against a real PostgreSQL database and twenty-eight that run real FFmpeg renders
and read the resulting pixels back. The video pipeline has been run end to end
on a real exported GameChanger clip, which is where several of those tests came
from.

---

## What it does

| | |
|---|---|
| **Team setup** | Teams, seasons, rosters, jersey numbers, positions, batting orders, guardians |
| **Games** | Date, opponent, home/away, location, tournament, first pitch time |
| **Uploads** | Full-game recordings or individual clips, streamed to disk, probed on arrival |
| **Play-by-play** | CSV import with automatic column matching and a preview before anything is saved |
| **Matching** | Scorebook and video timestamps first; jersey recognition only as a tiebreaker; no facial recognition ever |
| **Review** | Timeline screen with confidence badges, plain-English reasons, keyboard shortcuts |
| **Editing** | Adjustable lead-in and follow-through, category, player reassignment, slow motion |
| **Clips** | Automatic dead-time trimming, four categories, explainable ranking |
| **Reels** | Intro cards, scorebugs, stat lower-thirds, team colours and logo, ducked music |
| **Export** | 16:9 horizontal and 9:16 vertical MP4 |
| **Sharing** | Links bound to named guardians, expiring, revocable, never public |
| **Consent** | Per player, per purpose, append-only, enforced in the UI, the API and the worker |

## What it deliberately does not do

- **No GameChanger API and no scraping.** There is no unofficial API client and
  no code that fetches anything from GameChanger. The application reads video,
  rosters and play data that a coach exports and uploads themselves. See
  [docs/data-import.md](docs/data-import.md).
- **No facial recognition, no biometrics.** Jersey digits on fabric are the only
  thing read from a frame, and only for clips the scorebook already left
  uncertain. Only a year of birth is stored, never a full date.
- **No public links.** Every share is bound to named guardian accounts.

---

## Architecture at a glance

```
Next.js (App Router, TypeScript)          PostgreSQL 16              Python worker
  coach and parent interface        <-->    schema + job queue  <-->   OpenCV analysis
  uploads, imports, review screen           consent records            FFmpeg rendering
```

Jobs live in PostgreSQL rather than a separate queue, claimed with
`FOR UPDATE SKIP LOCKED`. One fewer service to run, and a job is transactionally
consistent with the rows it operates on. Full detail in
[docs/architecture.md](docs/architecture.md).

---

## Setup

### With Docker (recommended)

```bash
cp .env.example .env
$EDITOR .env                    # set POSTGRES_PASSWORD at minimum

docker compose up -d --build
docker compose exec -T db psql -U phg -d phg < db/migrations/0001_init.sql
docker compose exec -T db psql -U phg -d phg < db/migrations/0002_stat_views.sql

# Create your account. The password is prompted, never passed as an argument.
docker compose exec worker python3 /app/../scripts/create-user.py \
  coach@example.com "Your Name" --role coach
```

Open <http://localhost:3000>. Put a TLS-terminating reverse proxy in front of it
before anyone outside your house uses it; the compose file binds to localhost on
purpose.

### Without Docker

Requires PostgreSQL 16+, Node 22+, Python 3.11+, FFmpeg 6+, and optionally
Tesseract for jersey recognition.

```bash
# 1. Database
createdb phg
psql phg -f db/migrations/0001_init.sql
psql phg -f db/migrations/0002_stat_views.sql

# 2. Worker
cd worker
python3 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
cd ..

# 3. Web
cd web && npm install && npm run build && cd ..

# 4. Configuration
cp .env.example .env && $EDITOR .env
export $(grep -v '^#' .env | xargs)
mkdir -p "$PHG_MEDIA_ROOT"

# 5. Your account
python3 scripts/create-user.py coach@example.com "Your Name" --role coach

# 6. Run both processes
cd worker && python -m phg.cli worker &
cd web && npm start
```

### Optional demo data

`db/seed.sql` creates a team, a season, a nine-player roster, a game and the
consent records, matching `samples/roster.csv` and `samples/plays.csv`. It
creates no user accounts on purpose, so run `scripts/create-user.py` first.

```bash
psql "$DATABASE_URL" -f db/seed.sql
```

---

## Checking your data before you upload it

Both importers are available offline, so a coach can find out what is wrong with
a CSV without touching the application:

```bash
cd worker
python -m phg.cli check-roster ../samples/roster.csv
python -m phg.cli check-plays  ../samples/plays.csv --team "Riverside Rays"
python -m phg.cli probe /path/to/game.mp4
```

`probe` is worth running on any new camera: if it reports no recording start
time, matching will rely on sync points you set by hand in the review screen.

---

## Running the tests

```bash
cd worker
pip install -r requirements-dev.txt
python -m pytest tests/ -q                       # unit tests, no services needed
PHG_TEST_DSN=postgresql:///phg_test python -m pytest tests/test_db_integration.py
# FFmpeg tests run automatically when ffmpeg and ffprobe are on PATH
```

```bash
cd web
npm run typecheck
npm run build
```

The FFmpeg tests render real video and read the resulting frames back, because
FFmpeg exits 0 whether an overlay drew correctly, drew wrongly, or did not draw
at all. Two real bugs were caught that way during development; both are now
guarded by named regression tests.

---

## Validated against real footage

The video pipeline has been run end to end on an exported GameChanger home-run
clip from a 10U game. That produced four fixes no synthetic test would have
found:

- A fixed motion threshold of 0.015 matched **none** of the clip's 113 footage
  samples. A locked-off wide shot of a youth field has a motion median of
  0.0023. The threshold is now derived from each clip's own distribution.
- The clip opened with a title card and cut to footage at 4.0 seconds, changing
  93% of the pixels in one frame. The detector read that as the action peak and
  kept the title card. Cuts and leaders are now identified and excluded.
- A slow-motion request that overran the clip end by 0.03 seconds was silently
  dropped, so the render succeeded and nothing happened. It now clamps.
- The intro card chose white text on the team's orange at 3.35:1 where black
  gave 5.64:1, because the contrast check compared raw channel values instead of
  linearized ones.

Thirteen regression tests reproduce that clip's shape synthetically, so none of
the four can come back without a 17 MB video in the repository.

## Documentation

| Document | What is in it |
|---|---|
| [docs/architecture.md](docs/architecture.md) | Components, data flow, job pipeline, deployment, scaling |
| [docs/database-schema.md](docs/database-schema.md) | Every table, why it is shaped that way, the indexes that matter |
| [docs/matching.md](docs/matching.md) | How a play becomes a clip, the confidence model, where jersey reading fits |
| [docs/user-workflow.md](docs/user-workflow.md) | What a coach actually does, start to finish, with timings |
| [docs/wireframes.md](docs/wireframes.md) | Screen-by-screen layouts and interaction notes |
| [docs/data-import.md](docs/data-import.md) | Accepted CSV shapes, column aliases, the GameChanger position |
| [docs/privacy-and-consent.md](docs/privacy-and-consent.md) | Consent model, retention, what is and is not stored |
| [docs/roadmap.md](docs/roadmap.md) | Phased plan: what shipped, what is next, what is deliberately out |

## Repository layout

```
db/migrations/      PostgreSQL schema and derived stat views
shared/             Column aliases, read by both importers so they cannot drift
web/                Next.js application (coach and parent interface)
worker/             Python worker: matching, OpenCV analysis, FFmpeg rendering
worker/tests/       141 tests
infra/              Dockerfiles
scripts/            Operational scripts
samples/            Example roster and play-by-play CSVs
docs/               Design documentation
```

## Licence and use

Private application for a single team. Music you upload is your responsibility:
record the licence in the music screen, because that is what you will be asked
for if a parent reposts a reel.
