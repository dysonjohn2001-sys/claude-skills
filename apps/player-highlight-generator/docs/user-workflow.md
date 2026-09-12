# User workflow

Two people use this application: the coach, who does all the work, and the
parent, who watches one video. The whole design is about keeping that asymmetry.

---

## One-time setup (about 30 minutes, once per season)

### 1. Team and branding

*Team & branding.* Name, age group, timezone, primary and accent colours, logo
PNG. The intro card picks black or white text automatically depending on which
reads against the primary colour, so a light-jersey team does not get invisible
names.

The same screen holds the tunables:

| Setting | Default | Change it when |
|---|---|---|
| Seconds before the play | 5.0 | Your camera operator reacts late; try 7 |
| Seconds after the play | 8.0 | Your field is big and throws take longer |
| Trim dead time | on | Rarely; it never cuts below 4 seconds, and it removes the title card that exported clips open with |
| Auto-approve at or above | 0.80 | You have reviewed a few games and trust it; 0.85 sends more to review |
| Discard below | 0.45 | Your review queue is full of nonsense; raise it |
| Jersey recognition | on | Turn off if your numbers are small or the camera is far away |

### 2. Roster

*Roster.* Upload a CSV, or type players in. The importer reads either a single
`name` column (`First Last` or `Last, First`) or separate first and last name
columns, plus number, position, bats, throws, batting order and parent contact.

**Tick "Preview only" the first time.** It shows exactly what it would import
and what it could not read, and saves nothing. A duplicate jersey number is a
hard error with both row numbers, not a warning.

Ten minutes here pays for itself all season. Accurate names and unique numbers
are what the matcher runs on.

### 3. Consent

*Consent.* Nothing is generated for a player until a guardian grants
`media_capture` and `highlight_generation`. This is not a formality the
application nags about and then ignores: the matcher skips unconsented players
entirely, so their reels come out empty.

The screen shows a grid of players against the five consent types and flags
anyone blocking. See [privacy-and-consent.md](privacy-and-consent.md).

### 4. Music (optional)

*Music.* Upload a track and record its licence. Reels work fine without music,
using the clip audio, which many parents prefer anyway.

---

## Per game (about 20 minutes of the coach's attention)

### 1. Create the game

*Games → Add a game.* Date, opponent, home or away, location, tournament.

**Enter the first pitch time.** It takes five seconds and it is the fallback the
matcher uses if the play export turns out to have no timestamps.

### 2. Upload the video

Drop in the recording. Several files are fine if the camera stopped and
restarted; each gets its own timeline.

Processing starts immediately: the file is probed for duration, resolution and
recording start time, and then the coach can walk away. A 90-minute 1080p
recording takes a minute or two to probe.

### 3. Import the play-by-play

Export the scorebook as CSV from whatever app the team scores in, and upload it.
The importer matches column names itself and reports what it found. If the file
has no team column, pick which half-inning your team bats in.

Matching starts automatically once both the video and the plays are in.

### 4. Set a sync point (30 seconds, and the highest-value step)

Open *Review*. Scrub to any play you recognise, select it in the list, press
**Set sync point**. That tells the application that this moment in the video is
this moment in the game.

One anchor fixes the offset between the camera clock and the scorekeeper's. Two,
one early and one late, also correct drift. The difference between no anchor and
two anchors is roughly ±85 seconds of uncertainty versus ±5, which is the
difference between a review queue full of near-misses and one that is nearly
empty.

Then re-run matching from the game page.

### 5. Review

The review screen is built for speed, because this is the step a coach will
abandon if it is tedious.

- Clips appear as coloured bars on a timeline under the video, by category.
- Dashed outlines mark clips the application is unsure about.
- The list on the right defaults to **Needs review** only.
- Selecting a clip jumps the video there and shows *why* it is uncertain in
  plain sentences: "this player is not in the expected batting slot", "no sync
  anchor is set for this video".

Keyboard only, which is how a coach will actually work through 20 items:

| Key | Action |
|---|---|
| `space` | Play / pause |
| `J` / `L` | Nudge 2 seconds back / forward |
| `R` | Replay the selected clip from its start |
| `A` | Approve and advance |
| `X` | Reject and advance |
| `↑` / `↓` | Move through the list |

Anything can be corrected inline: reassign the player, change the category,
adjust the lead-in or follow-through. A manual assignment sets confidence to 1.0
and is never undone by a later re-match.

A clean game with a sync anchor set typically leaves 2–5 clips to review. A game
with no anchor and a name-less scorebook leaves most of them, which is the
application being honest rather than confident.

### 6. Build reels

*Players → a player → Build a reel.* Pick the scope (this game, a tournament, or
the whole season) and the format (16:9, 9:16, or both).

Only approved clips are used. Anything still in the review queue is left out, on
purpose: an unreviewed uncertain match is exactly the clip that would put
another child in this player's reel.

Rendering takes a few minutes per reel.

### 7. Share

*Player → a reel → Share.* Tick the families, set an expiry, decide whether
downloading is allowed. The link is shown once.

The link is bound to the guardians you ticked. Forwarding it does not grant
anyone else access, because the recipient still has to sign in as an invited
guardian. Links can be revoked at any time, and revoking a player's family
sharing consent revokes every existing link for that player automatically.

---

## What a parent does

1. Receives a link from the coach.
2. Signs in with the email the coach invited.
3. Watches the reel. Downloads it if the coach allowed that.

*My family's reels* lists everything shared with them, scoped by their own
guardian record rather than by anything in the URL. A parent cannot reach
another family's reels by guessing ids.

---

## Timings on real hardware

Measured on a 4-core machine, 1080p30 source, software x264 encoding.

| Step | 90-minute game |
|---|---|
| Upload (local network) | 3–6 min |
| Probe | ~1 min |
| Matching (all plays, all players) | under 10 s |
| Dead-time analysis | ~2 s per clip |
| Jersey OCR, when it runs | ~8 s per clip |
| Cutting | ~4 s per clip |
| Rendering a 12-clip reel | ~90 s |
| **Coach's actual attention** | **~20 min, mostly review** |

Nine players × two aspect ratios is 18 reels, about 30 minutes of unattended
rendering. Scale the worker across cores and it is proportionally less.

---

## Troubleshooting

**"Matching needs at least one processed video and an imported play-by-play
file."** One of the two is missing or still processing. The game page shows the
status of each.

**Everything landed in the review queue.** Almost always no sync anchor. Set one
and re-run. If it persists, the play export probably has no names, only batting
slots; set the lineup for that game.

**A player's reel is empty.** Check consent first, then the review queue.
Unconsented players get no clips at all, and unreviewed clips are excluded from
reels.

**Clips are consistently a few seconds early or late.** The roll settings are
per team on the branding page, and per clip in the review screen. If every clip
is off in the same direction, add a second sync anchor near the end of the
recording so drift is corrected rather than accumulated.

**The wrong team's plays got clipped.** The play file had no team column and the
half-inning setting was wrong. Re-import with the other setting; re-importing
replaces the game's plays rather than appending.
