# Phased development plan

The MVP is Phase 1 and Phase 2, and it is built. What follows records what
shipped, what is next, and what is deliberately out of scope.

---

## Phase 0 — Foundations *(complete)*

Schema, job queue, identity, and the two CSV importers.

- 31 tables, 15 enum types, 5 derived views. Applied and exercised against a
  real PostgreSQL 16 instance.
- PostgreSQL-backed job queue with `FOR UPDATE SKIP LOCKED` claiming, backoff
  and retry.
- Session auth with scrypt password hashing, verified to interoperate between
  Python account creation and Node login.
- Roster and play-by-play importers with automatic column matching, sharing one
  alias table between the two languages.
- 141 automated tests.

## Phase 1 — Matching *(complete)*

The part that has to be right.

- Wall-clock to video-time fitting with one, two or zero sync anchors, including
  drift correction and a sanity bound on the fit.
- Timestamp interpolation for exports that only partly carry them.
- Name resolution across six strategies, refusing rather than guessing when two
  candidates are equally good.
- Five-factor confidence model with stored factors and a hard gate on unnamed
  subjects.
- Jersey recognition as a bounded, banded, capped secondary signal.
- Consent gate enforced in the worker, not only the interface.

## Phase 2 — Clips and reels *(complete)*

- Dead-time detection with OpenCV, conservative by construction.
- Single-pass FFmpeg cutting: trim, concatenate, slow motion, canvas fit,
  scorebug, lower third, logo.
- Intro cards composed with Pillow, with automatic text-contrast selection.
- Reel assembly with the concat filter and sidechain-ducked music.
- 16:9 and 9:16 export.
- Explainable ranking with category coverage in reel selection.
- Timeline review screen with keyboard-driven approval.
- Guardian-bound share links, expiry, revocation, view logging.

---

## Phase 3 — Make the coach faster *(next)*

Everything here comes from the same observation: the coach's time is the scarce
resource, and review is where it goes.

**Read the title card on single-play exports.** A clip exported from a
scorekeeping app opens with a card naming the play, the inning and the side
("Home Run / 4th / Offense"). That is the answer to the matching question,
printed on screen in a clean sans-serif on a flat background, which is the
easiest possible OCR target. Reading it would match a one-play clip to its play
with near-certainty and no sync anchor at all. The leader is already detected
and its boundaries known, so the work is OCR on frames already being decoded
plus a parser for a short, highly structured string. This is now the
highest-value item on the list: coaches export single plays far more often than
full games.

**Automatic sync-point suggestion.** Scoreboard OCR, or audio-based detection of
the crack of a bat matched against the first few play timestamps, to propose an
anchor the coach confirms rather than sets. This is the single highest-value
item on the list: it turns the one manual step that most affects accuracy into a
confirmation.

**Batch review.** "Approve all above 70%" after the coach has spot-checked a
few, with a one-click undo. Most review sessions are a coach agreeing with the
matcher twenty times.

**Progress that a coach can watch.** The `jobs` table already has a progress
column and a log; the dashboard should stream it rather than showing counts.

**Clip trimming by dragging.** The review screen adjusts roll numerically. Drag
handles on the timeline would be faster for the cases where 5 and 8 are wrong.

**Better guardian invitations.** Roster import stages guardians; sending the
invitation is still manual. An invite flow with an acceptance page closes it.

## Phase 4 — Better output

**Transitions and pacing.** Hard cuts throughout at the moment. Crossfades
between clips of the same at-bat, hard cuts between innings.

**Automatic slow motion.** The motion profile already identifies the action
peak. Proposing a half-speed section around it, for the coach to accept, is a
small step from data the pipeline already computes.

**Multi-camera.** Some clubs run a backstop camera and an outfield camera. The
timeline model already supports several assets per game; picking the better
angle per play needs a quality heuristic.

**Season montages.** A team-wide reel rather than per-player, which needs its own
consent handling since it mixes children whose families made different choices.

**Vertical-first framing.** 9:16 currently pillarboxes. Cropping toward the
action using the motion centroid would fill the frame.

## Phase 5 — Scale beyond one team

Only worth doing if a club adopts it.

**Object storage.** Storage keys are already relative rather than paths, so this
is swapping the media route for signed URLs.

**Hardware encoding.** `h264_nvenc` or `h264_vaapi` in place of `libx264`, worth
roughly an order of magnitude on the encode step.

**Multi-team isolation.** The schema has `teams` throughout, but the application
assumes one. Row-level security and a team switcher would make it real.

**Documented-API connectors.** If a scorekeeping platform publishes a real API
with a real authorisation flow, a connector populates `plays` and
`play_participants` the same way the CSV path does. Not before.

---

## Deliberately out of scope

**Unofficial GameChanger integration.** No reverse-engineered API client, no
scraper, no credential storage for a third-party service. See
[data-import.md](data-import.md). This is a permanent constraint, not a
phase that has not happened yet.

**Facial recognition.** Not a performance decision. No face detection, no
embeddings, no biometric templates, on footage of children. The scorebook
already knows who was batting.

**Public sharing.** No public links, no social posting, no embeddable player.
Sharing is guardian-bound by design and the schema has no way to express
anything else.

**Live streaming.** A different application with different hard problems.

**Opponent analysis.** Opponent children appear in the footage and are never
named, matched, clipped or recorded. Adding that would make this a surveillance
tool.

**Automated deletion.** The machinery is there; the policy belongs to the club,
because getting it wrong destroys memories.

---

## Known limitations today

| Limitation | Workaround | Fixed in |
|---|---|---|
| Sync points are set by hand | 30 seconds per game, and it is the highest-value 30 seconds | Phase 3 |
| A single-play export is matched by timestamp, which may be the export time | Assign it to its play in the review screen | Phase 3 |
| Review is one clip at a time | Keyboard shortcuts make it fast | Phase 3 |
| No live job progress | The dashboard shows queue counts | Phase 3 |
| Slow motion must be set manually | The motion peak is already computed | Phase 4 |
| Hard cuts only | — | Phase 4 |
| 9:16 pillarboxes rather than crops | — | Phase 4 |
| Single-team assumption in the UI | Schema already supports more | Phase 5 |
| Local filesystem media | Storage keys are relative already | Phase 5 |
| Software encoding only | Scale workers across cores | Phase 5 |

## Effort estimates

For one developer, assuming the MVP as the starting point.

| Phase | Estimate |
|---|---|
| Phase 3 — coach speed | 3–4 weeks, of which sync-point suggestion is half |
| Phase 4 — output quality | 3–4 weeks |
| Phase 5 — scale | 4–6 weeks, mostly multi-team isolation and its testing |
