# Player-to-play matching

This is the part of the application that has to be right. Everything else is
plumbing around it. If a clip of one child ends up in another child's reel and
gets sent to a family, that is not a bug report, it is an apology.

The design principle throughout: **the scorebook and the clock decide; the
camera only breaks ties.**

## The two questions

Matching answers two separate questions, and it is worth keeping them apart.

1. **Where in the footage did this play happen?** Answered by clock arithmetic
   in `matching/timeline.py`.
2. **Which of our players earned a highlight from it?** Answered by the
   scorebook, the roster and the batting order in `matching/name_resolver.py`
   and `matching/play_matcher.py`.

Jersey recognition contributes to neither. It only adjusts a confidence score
that has already been computed.

## Question one: locating the play

A recording has its own clock. The scorekeeper's phone has another. They
disagree, sometimes by minutes, and they drift apart over a three-hour game.

`Timeline` fits a mapping from wall-clock time to video time, with an honest
error bar. Three levels of information:

| What is available | Mapping | Typical error bar |
|---|---|---|
| Two or more sync anchors | Least-squares fit, correcting clock drift as well as offset | ±25s, tighter between the anchors |
| One sync anchor | Fixed offset; drift accumulates with distance | ±25s, growing 0.35s per minute away |
| Container timestamp only | Recording start from file metadata | ±85s |

A **sync anchor** is a coach scrubbing to a play they recognise in the review
screen and pressing *Set sync point*. It takes about ten seconds. One anchor
near the first inning and one near the last holds a three-hour recording within
a couple of seconds throughout.

Two guards in the fit:

- A slope outside 0.98–1.02 is rejected and pinned to 1.0. A camera clock that
  disagrees by more than 2% is a data-entry error, not drift, and warping the
  whole game to fit it would be worse than ignoring it.
- Error bars shrink by 60% when the play falls *between* two anchors, because
  interpolating is materially more trustworthy than extrapolating.

### Plays with no timestamp

Exports vary. Some carry a timestamp per play, some per half inning, some none.
Known timestamps are kept exactly. Unknown ones are placed by linear
interpolation on sequence number between the nearest known neighbours, and
extrapolated at 45 seconds per play outside them. With no timestamps at all, the
game is paced from first pitch at nine minutes per half inning.

Every inferred timestamp is counted and reported, and inference drives the
confidence score down, so pace-estimated games land in the review queue where
they belong.

## Question two: identifying the player

### Resolving a name

Scorekeepers write names inconsistently: `Smith, J.`, `Jake Smith`,
`J SMITH #12`, `Smith`. `NameResolver` walks progressively weaker strategies and
reports which one fired, so the confidence model can price it:

| Strategy | Confidence | Note |
|---|---|---|
| Exact match on any accepted spelling | 1.00 | Includes `Last, First` and preferred names |
| Jersey number inside the name string | 0.95 | `M HERNANDEZ #21` |
| Last name plus first initial | 0.92 | Only when it is unambiguous |
| A last name unique on this roster | 0.88 | |
| Fuzzy match | 0.70 × quality | Floor 0.86 similarity |
| Batting order, when the name is blank | 0.65 | |
| Nothing | 0.00 | Clip is not created |

**No strategy ever picks between two equally good candidates.** If the top fuzzy
match is within 0.06 of the runner-up, the resolver refuses and hands both
candidates to the review screen. A roster with two Hernandezes will produce
review items, not coin flips.

Substitutions are respected: a player who entered in the fourth is not matched
to a play in the second.

### Who gets a clip from a play

Only the team's own players, and only in the role the play gives them:

| We are batting | We are fielding |
|---|---|
| Batter → **offense** (or **baserunning** for a steal) | Pitcher → **pitching** |
| Runners → **baserunning** | Credited fielders → **defense** |

A single play can produce several clips. A double play credits the pitcher, the
fielder recording the putout and the fielder credited with the assist, each in
their own reel.

## The confidence model

Five weighted factors, summing to 1.0:

| Factor | Weight | What it measures |
|---|---|---|
| `name_resolution` | 0.42 | How the scorebook name resolved |
| `timeline_precision` | 0.24 | Anchor count and the error bar |
| `batting_order` | 0.16 | Whether the player matches the expected slot |
| `lineup_presence` | 0.10 | Whether they were in the game that inning |
| `position_fit` | 0.08 | Whether a positional credit matches their position |

Plus one hard gate: a clip whose subject could not be named is capped at 0.35,
however clean the timing is.

Every factor is stored on the clip, and the review screen turns them back into
sentences. A coach sees *"this player is not in the expected batting slot"* and
*"no sync anchor is set for this video"*, not `0.62`.

The two thresholds are per team and adjustable:

- **at or above 0.80** the clip ships without review
- **below 0.45** the clip is discarded rather than queued, because a queue full
  of noise does not get reviewed
- **in between** it goes to the review queue

## Where jersey recognition fits

`matching/jersey_ocr.py` reads printed digits on fabric. It is bounded in four
separate ways, on purpose:

1. **It never assigns a player.** It returns digit observations. The confidence
   model folds them in.
2. **It only runs in the uncertain band** (0.45–0.85 by default). Clips the
   scorebook is sure about never pay for it, and it is the most expensive step
   in the pipeline.
3. **It can move a score by at most 0.18** in either direction. A perfect read
   cannot carry a clip on its own, and a wrong read cannot sink one the
   scorebook is sure of.
4. **Its vote scales with evidence.** One weak read counts for a quarter of what
   four confident reads count for.

The pipeline: OpenCV's stock HOG pedestrian detector finds person boxes, the
upper-back band of each box is cropped, upscaled, CLAHE-equalised and
Otsu-thresholded, and Tesseract reads it restricted to digits. Both polarities
are tried, because numbers are printed light-on-dark about as often as the
reverse.

Every observation is stored in `jersey_observations` with its timestamp,
confidence and bounding box. If a coach ever asks why a clip was flagged, the
evidence is there.

**No facial recognition. No face detection. No biometric template of any kind.**
The only thing extracted from a frame is printed digits on cloth.

Both of its dependencies are optional, and missing either degrades matching
rather than breaking it. Tesseract does the digit reading. The person detector
needs OpenCV 4.x: version 5 removed `HOGDescriptor`, so on 5.x the reader
reports why it is unavailable and matching carries on with the schedule signals
it leads on anyway. Failures inside the jersey step are caught and logged rather
than failing the job, because that job also carries the dead-time result and
queues the cut.

## Dead-time detection

Youth baseball is mostly standing around. A 13-second window around a scored
play still contains a batter adjusting a glove and an umpire dusting the plate.

`video/deadtime.py` samples the window at 6 fps, computes downscaled blurred
frame differences, smooths the result and finds where the action is. Blurring
first matters: camera shake and grass texture read as motion otherwise.

It is conservative by design:

- It returns keep/drop segments rather than cutting anything.
- A clip is never trimmed below 4 seconds.
- A 1.5-second lead-in before the first motion is always kept, so the viewer
  sees the pitch and not just the swing.
- If nothing crosses the motion threshold, the centre of the clip is kept rather
  than the clip dropped. A quiet frame is more often a distant camera than a
  dead play.

The mean motion also feeds clip ranking as `action_density`.

## Ranking

A 0–100 rubric, not a model, so a coach can argue with it and a settings screen
can re-weight it:

| Component | Weight |
|---|---|
| Play merit (home run 100, single 52, groundout 14) | 0.40 |
| Leverage (late innings, close score, walk-off tag) | 0.22 |
| Production (RBI, runs scored) | 0.14 |
| Action density (from dead-time analysis) | 0.12 |
| Match confidence | 0.12 |

The asymmetries are deliberate. A strikeout is worth 62 to the pitcher and 4 to
the batter. Errors and caught-stealings are suppressed to a quarter of their
score rather than deleted, so the coach can still find them in the review screen
but they do not lead a reel.

Reel selection then guarantees that every category a player actually appeared in
gets at least one clip, before filling the rest by rank. A pitcher's reel should
not be 100% batting. The duration cap is a hard stop: a nine-minute reel is not
a highlight reel.

## What this gets wrong, and what to do about it

**Two players with the same last name and the same first initial.** The resolver
refuses rather than guessing. Give one of them a preferred name on the roster.

**A scorebook with no names at all, only batting slots.** Works, at 0.65
confidence, which means everything lands in the review queue. Set the lineup for
the game and it improves.

**A camera that stops and restarts mid-game.** Upload both files. Each gets its
own timeline and its own sync anchors, and the matcher picks whichever video
actually contains the instant.

**A play at the very start of a recording.** The lead-in is clamped to the file
bounds, so the clip is shorter rather than invalid.

**Jersey numbers that are not unique.** The schema refuses two active players
sharing a number, and the roster importer rejects the file with the row numbers.
Number-based matching that lies is worse than none.
