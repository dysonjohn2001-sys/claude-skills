# Architecture

## Shape of the system

Three processes and one shared filesystem.

```
                    ┌─────────────────────────────────────────┐
                    │              PostgreSQL 16              │
                    │                                         │
                    │  teams · seasons · players · guardians  │
                    │  consents (append-only)                 │
                    │  games · plays · play_participants      │
                    │  media_assets · media_sync_anchors      │
                    │  clips · clip_segments · reels          │
                    │  share_links · audit_log                │
                    │  jobs  ← the queue lives here too       │
                    └──────────┬───────────────────┬──────────┘
                               │                   │
              reads/writes     │                   │  claims jobs, writes results
                               │                   │
        ┌──────────────────────┴──────┐   ┌────────┴────────────────────────┐
        │   Next.js 15 (App Router)   │   │      Python worker (1..n)       │
        │                             │   │                                 │
        │  coach + parent interface   │   │  play → player matching         │
        │  streaming uploads          │   │  OpenCV motion + jersey OCR     │
        │  CSV import + preview       │   │  FFmpeg cutting + rendering     │
        │  timeline review screen     │   │                                 │
        │  range-serving media        │   │                                 │
        └──────────────┬──────────────┘   └────────┬────────────────────────┘
                       │                           │
                       └────────────┬──────────────┘
                                    │
                        ┌───────────┴────────────┐
                        │   Media volume         │
                        │   games/  clips/       │
                        │   reels/  music/       │
                        │   teams/  (logos)      │
                        └────────────────────────┘
```

## Why these pieces

**Next.js App Router with server components.** Nearly every screen is a database
read rendered on the server. Server components mean no API layer to build and
maintain for data that only one page ever needs. The one genuinely interactive
screen, the review timeline, is a client component that talks to a small number
of purpose-built route handlers.

**PostgreSQL for the job queue.** The usual instinct is Redis or SQS. For a
single-team private deployment that is one more service to install, monitor and
back up, in exchange for a queue that cannot participate in the same transaction
as the rows it operates on. `SELECT ... FOR UPDATE SKIP LOCKED` gives safe
multi-worker claiming in one statement, and `docker compose up --scale worker=3`
is the whole scaling story. If this ever outgrows that, the queue is one table
and one module.

**Python for the worker.** OpenCV and the surrounding numeric tooling are Python
first, and the matching logic is the part most likely to need tuning by someone
reading it carefully. It is written as plain functions over plain dataclasses
with no database access, so every rule in it is unit-testable without a running
PostgreSQL. The database layer is a separate module that loads those dataclasses.

**FFmpeg for everything that touches pixels at scale.** OpenCV analyses frames;
it never encodes. One FFmpeg process per clip does trim, concatenate, slow
motion, canvas fit and every overlay in a single filter graph. A three-hour game
with 140 clips re-encoded three times each is the difference between a coach
getting reels the same evening and getting them tomorrow.

## The pipeline

```
  upload ──► probe_media ──┐
                           ├──► match_plays ──► analyze_clip ──► cut_clip ──► render_reel
  play CSV import ─────────┘         │              │                             ▲
                                     │              │                             │
                          writes clip rows   dead-time detection,        coach picks scope
                          with confidence    then jersey OCR only        and aspect ratio
                          and rank scores    if confidence is
                                             uncertain
```

Each arrow is a row in `jobs`. Every handler is idempotent enough to re-run: a
failed job is requeued with exponential backoff up to three attempts, then
marked failed with the error text kept for the coach to read.

### probe_media

Runs `ffprobe`, records duration, resolution, frame rate, audio presence and,
critically, the recording start time from container metadata. Phone footage
usually carries one; a dedicated camera often does not. Rotation metadata is
applied so that a phone-shot vertical video reports its real dimensions.

If the game already has play data, this queues matching automatically.

### match_plays

The heart of the system, described in full in [matching.md](matching.md).
Briefly: fit a wall-clock-to-video-time mapping per recording, fill in missing
play timestamps by interpolation, resolve each credited name against the roster,
score the assignment, and write a clip row per player per play per category.

Two guards live here. Players without an active `highlight_generation` consent
are skipped entirely. Clips a coach has already approved or rejected are left
untouched, so re-running after fixing a roster typo never undoes review work.

### analyze_clip

Samples the clip window with OpenCV, builds a smoothed motion-over-time profile,
and writes keep/drop segments. Then, **only if** the schedule-based confidence
landed in the uncertain band, reads jersey numbers and folds them in with a hard
cap. Finally re-decides the review status now that both signals are in.

### cut_clip

Builds one FFmpeg filter graph: trim each kept span, concatenate, apply the
slow-motion section if there is one, fit to the export canvas, then the
scorebug, lower third and logo. One pass, one output file.

### render_reel

Composes the intro card as a PNG with Pillow (real text metrics beat wrestling
`drawtext` into a layout), turns it into a video segment, then concatenates
everything and mixes the music bed.

## Two decisions worth knowing about

**The concat filter, not the concat demuxer.** The demuxer is cheaper and was
the first implementation. It silently drops audio at every segment boundary: a
three-segment reel came out with 18.0s of video against 16.6s of audio, drifting
further apart with each clip added. The concat filter re-encodes and keeps the
streams locked. Since the reel is re-encoded for the music mix anyway, the
demuxer was buying nothing. A test asserts audio and video durations match
within 0.25s.

**Optional signals must degrade, never fail.** Jersey recognition is built on
two optional dependencies. Its job also carries the dead-time result and queues
the cut, so letting a missing dependency fail that job would cost the coach the
clip entirely. The reader constructs without raising, reports why it is
unavailable, and the call site catches anything it throws.

**Uniform stream layout everywhere.** A muted clip still gets a silent 48 kHz
stereo track rather than no audio stream at all, because a missing stream breaks
concatenation later. Cheap to produce, and it removes a whole category of
assembly failure.

## Shared code between the two languages

The CSV header alias tables live in `shared/column-aliases.json`. Both the
Python importer and the TypeScript importer read it, so adding a vendor's header
spelling is a one-line change in one file rather than two implementations
drifting apart. The Python side resolves it relative to the repository root and
honours `PHG_COLUMN_ALIASES`; the worker image places it at `/shared`.

Password hashing is scrypt with a 16-byte random salt, stored as
`scrypt$salt$hash`. Python's `hashlib.scrypt` defaults and Node's `crypto.scrypt`
defaults agree (N=16384, r=8, p=1), which is verified rather than assumed:
accounts created by `scripts/create-user.py` are checked to authenticate through
the Next.js login route.

## Media serving

`/api/media/[...key]` serves files with HTTP range support so the review screen
can scrub a three-hour recording without downloading it. Three guards:

1. Signed-in users only.
2. The resolved absolute path must stay inside the media root, so a key
   containing `..` cannot escape.
3. Guardians may read only reel outputs covered by an active, unexpired share
   link that names them. Coaches may read their team's files.

For a deployment larger than one machine, replace this route with signed URLs
from object storage. It exists so the application runs end to end without one.

## Deployment and scaling

The compose file binds both PostgreSQL and the web app to `127.0.0.1`. Put a
TLS-terminating reverse proxy in front. Nothing in the application is designed
to face the internet directly.

Scaling, in the order it will actually be needed:

1. **More workers.** `--scale worker=3`. Encoding is CPU-bound and jobs are
   independent. The queue handles it with no configuration.
2. **Hardware encoding.** Swap `libx264` for `h264_nvenc` or `h264_vaapi` in
   `worker/phg/video/clipper.py` and `render.py`. Roughly an order of magnitude
   on the encode step.
3. **Object storage.** Move the media volume to S3-compatible storage and swap
   the media route for signed URLs. The storage key column already holds a
   relative key rather than a path, so this is a narrow change.
4. **Read replicas.** Only if a single team's dashboard somehow becomes hot,
   which it will not.

## Failure modes and what happens

| Failure | Behaviour |
|---|---|
| Upload interrupted | Asset marked `failed` with the error; the coach sees it on the game page and re-uploads |
| `ffprobe` rejects the file | Asset marked `failed` with the message; matching is not queued |
| No recording timestamp and no sync anchor | Matching skips that asset and reports why; the review screen prompts for a sync point |
| Play-by-play with no timestamps | Plays are paced from first pitch, confidence drops, everything lands in the review queue |
| A play lands outside every uploaded video | Reported in the job result, no clip written |
| A worker dies mid-job | The job stays `running` until its lock ages out, then is retried. Handlers rewrite rather than append, so a partial run is not corrupting |
| FFmpeg fails on one clip | That job fails after three attempts; every other clip is unaffected |
| Guardian consent revoked | New clips stop immediately; revoking family sharing also revokes every existing share link for that player in the same transaction |
