# Wireframes

Screen layouts as built. The application uses a dark interface throughout: a
coach reviews footage, and a bright surround makes judging video harder.

Layout is a fixed 232px sidebar and a fluid main column capped at 1180px.
Everything collapses to a single column below 880px, because a coach standing in
a dugout has a phone, not a laptop.

---

## Dashboard — `/`

Everything waiting on the coach, and what the worker is doing.

```
┌────────────────┬──────────────────────────────────────────────────────────────┐
│ Player         │  Dashboard                                                   │
│ Highlight      │  Everything waiting on you, and what the worker is doing.    │
│ Generator      │                                                              │
│ Sam Rivera     │  ┌───────────┐ ┌───────────┐ ┌───────────┐                   │
│                │  │    9      │ │   12      │ │   147     │                   │
│ Dashboard   ◄  │  │  PLAYERS  │ │  GAMES    │ │  CLIPS    │                   │
│ Games          │  └───────────┘ └───────────┘ └───────────┘                   │
│ Review queue   │  ┌───────────┐ ┌───────────┐ ┌───────────┐                   │
│ Players        │  │    4      │ │   18      │ │    1      │                   │
│                │  │ AWAITING  │ │  REELS    │ │ MISSING   │                   │
│ SETUP          │  │ REVIEW    │ │ RENDERED  │ │ CONSENT   │                   │
│ Team & brand   │  └───────────┘ └───────────┘ └───────────┘                   │
│ Roster         │                                                              │
│ Consent        │  ⚠ 1 player has no active highlight-generation consent.      │
│ Music          │    No clips are produced for them. Review consent →          │
│                │                                                              │
│ [ Sign out ]   │  Recent games                                                │
│                │  ┌──────────────────────────────────────────────────────┐    │
│                │  │ GAME          VIDEO  PLAYS  CLIPS  TO REVIEW         │    │
│                │  │ Apr 18 vs …     1     112     24    ●4    Open Review│    │
│                │  │ Apr 11 vs …     1      98     19    clear  Open …    │    │
│                │  └──────────────────────────────────────────────────────┘    │
│                │                                                              │
│                │  Processing                                                  │
│                │  3 × cut_clip running · 1 × render_reel queued               │
└────────────────┴──────────────────────────────────────────────────────────────┘
```

The six tiles are the whole status of the system. "Awaiting review" and "Missing
consent" link straight to the screens that clear them.

---

## Game — `/games/[gameId]`

Two columns, because video and play data arrive independently and the coach
needs to see both states at once.

```
  Apr 18 vs Northside Owls
  Riverside Rays · Spring 2026 · Northside Park, Field 1 · final 5-4

  ⚠ None of this game's videos has a sync point yet. Matching will fall back to
    the file's recording timestamp, which on phone footage is often a minute
    out. Open the review screen, scrub to any play you recognise and press
    "Set sync point" — one is enough, two is better.

  ┌── Video ──────────────────────┐  ┌── Play-by-play ────────────────────┐
  │ game-apr18.mp4                │  │ Export the scorebook as CSV and    │
  │ Full game · 1:47:12 ·         │  │ upload it. The importer matches    │
  │ 1920×1080 · [ready] · 2 sync  │  │ columns itself and shows you what  │
  │                               │  │ it found before saving anything.   │
  │ Add a recording or clip       │  │                                    │
  │ [ Choose file          ]      │  │ 112 plays imported                 │
  │ Type      Recording started   │  │ · 112 with timestamps · 58 offense │
  │ [Full game▾] [           ]    │  │                                    │
  │ [ Upload ]                    │  │ [ Choose file ]                    │
  └───────────────────────────────┘  │ If the file has no team column,    │
                                     │ we bat in [the top ▾]              │
                                     │ [ Import plays ]                   │
                                     │                                    │
                                     │ Lineup                             │
                                     │ 1. Jake Smith #7                   │
                                     │ 2. Marcus Hernandez #12  …         │
                                     └────────────────────────────────────┘

  ┌── Matching ──────────────────────────────────────────────────────────────┐
  │ 24 clips matched · 4 awaiting review · 20 ready for reels                 │
  │ Re-running matching keeps every clip you have already approved.           │
  │                                    [ Re-run matching ] [ Open review ]    │
  └──────────────────────────────────────────────────────────────────────────┘
```

---

## Review — `/games/[gameId]/review`

The screen the whole application is built around.

```
  Review · Apr 18 vs Northside Owls
  24 clips matched, 4 flagged as uncertain.

  [game-apr18.mp4 ▾]  [Needs review (4) ▾]        [ Set sync point at playhead ]

  ┌─────────────────────────────────────────────┐ ┌───────────────────────────┐
  │                                             │ │ ┌───┐ Jake Smith      92% │
  │                                             │ │ │▓▓▓│ Offense · Top 1     │
  │               video player                  │ │ └───┘ 5:12                │
  │                                             │ │───────────────────────────│
  │                                             │ │ ┌───┐ M. Hernandez    64% │
  │                                             │ │ │▓▓▓│ Offense · Top 1  ●  │
  └─────────────────────────────────────────────┘ │ └───┘ 7:41                │
  ┌─────────────────────────────────────────────┐ │───────────────────────────│
  │ ▌ ▬▬  ▬▬▬   ┊ ▬▬▬▬  ▬▬   ▬▬▬▬▬   ▬▬  ▬▬▬▬  │ │ ┌───┐ Liam Nguyen     58% │
  │   ░░  ▓▓▓   ┊ ████  ░░   ▒▒▒▒▒   ▓▓  ████  │ │ │▓▓▓│ Pitching · Bot 1 ●  │
  └─────────────────────────────────────────────┘ │ └───┘ 12:03               │
  0:00  13:45  27:30  41:15  55:00  1:08  1:22    └───────────────────────────┘
  ■ Offense ■ Defense ■ Pitching ■ Baserunning
  Dashed outline = awaiting your review           Shortcuts: space play ·
                                                  J/L nudge 2s · R replay ·
  ┌── Marcus Hernandez — Single (Top 1) ──── 64% — check this ──┐   A approve ·
  │ Marcus Hernandez singles to right; Smith scores             │   X reject ·
  │ rank 71 · matched by schedule + jersey                      │   ↑/↓ move
  │                                                             │
  │ ⚠ Why this needs a look                                     │
  │   · The scorebook name only matched approximately.          │
  │   · This player is not in the expected batting slot.        │
  │                                                             │
  │ Player            Category    Before (s)  After (s)         │
  │ [M. Hernandez ▾]  [Offense ▾] [  5.0   ]  [  8.0  ]         │
  │                                                             │
  │ [ Approve ] [ Reject ] [ Replay ]  Window 7:41–7:54 (13.0s) │
  └─────────────────────────────────────────────────────────────┘
```

Four things make this fast:

1. **Colour carries category, dashes carry uncertainty.** A coach reads the
   timeline without reading any text.
2. **The filter defaults to "Needs review".** The default view is the work.
3. **The uncertainty is explained in sentences.** `0.64` tells a coach nothing;
   "this player is not in the expected batting slot" tells them exactly where to
   look.
4. **Approve advances.** `A A A X A` clears five clips without touching the
   mouse.

Clicking anywhere on the timeline seeks. Clicking a marker selects that clip and
jumps to it.

---

## Review queue — `/review`

Cross-game, grouped by game, ordered highest rank first and lowest confidence
first: the clip most likely to reach a reel while being wrong comes first.

```
  Review queue
  7 uncertain assignments across all games, most consequential first.

  Apr 18 vs Northside Owls   open review screen
  ┌───────────────────────────────────────────────────────────────────────┐
  │ PLAYER          CATEGORY   PLAY                    CONFIDENCE    RANK │
  │ M. Hernandez    Offense    Top 1 · singles to …    64% check      71  │
  │ Liam Nguyen     Pitching   Bot 1 · strikes out…    58% check      63  │
  └───────────────────────────────────────────────────────────────────────┘
```

---

## Player — `/players/[playerId]`

```
  Jake Smith #7
  Riverside Rays · bats R · throws R

  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
  │   14   │ │    6   │ │    3   │ │    2   │
  │OFFENSE │ │DEFENSE │ │PITCHING│ │BASERUN │
  │ clips  │ │ clips  │ │ clips  │ │ clips  │
  └────────┘ └────────┘ └────────┘ └────────┘

  Build a reel
  Scope          Which one                        Format
  [Single game▾] [Apr 18 vs Northside (6 clips)▾] [16:9 ▾]  [ Render reel ]
  Only approved clips are used. Anything still in review is left out.

  Reels
  ┌──────────────────────────────────────────────────────────────────────┐
  │ TITLE                  SCOPE  FORMAT  LENGTH  STATUS  SHARED         │
  │ Jake Smith — Apr 18    game   16:9    1:52    ready   2   Watch·Share│
  │ Jake Smith — Spring26  season 9:16    2:48    ready   3   Watch·Share│
  └──────────────────────────────────────────────────────────────────────┘

  Consent on file
  · Appears in team video: granted
  · Personal highlight reels may be generated: granted
  · Reels may be shared with this player's own family: granted
  · Reels may be visible to other families on the team: granted
  · Reels may be downloaded and posted elsewhere: not granted
```

---

## Consent — `/team/consent`

A grid, because the question a coach has is "who is blocking?" and a grid
answers it at a glance.

```
  Parental consent
  These are minors. Nothing is generated, stored as a reel, or shared without a
  guardian granting it, and every grant and revocation is kept as a dated record.

  ⚠ 1 player has no highlight-generation consent. The matcher skips them
    entirely, so they will not appear in any reel.

  ┌──────────────────────────────────────────────────────────────────────────┐
  │ PLAYER        GUARDIAN      TEAM   REELS  FAMILY  TEAM   EXTERNAL        │
  │                             VIDEO  BUILT  SHARE   SHARE  SHARE           │
  │ Sofia Alvarez Pilar A.      yes    yes    yes     yes    no      [Record]│
  │ Owen Brooks   Tim Brooks    yes    yes    yes     yes    no      [Record]│
  │ Cole Whitfield Kim W.       no     no     no      no     no      [Record]│
  └──────────────────────────────────────────────────────────────────────────┘
```

---

## Share a reel — `/reels/[reelId]/share`

```
  Share · Jake Smith — Apr 18 vs Northside Owls
  Links are bound to the families you name here. Forwarding one does not grant
  anybody else access.

  Share with
  ☑ Dana Smith    dana.smith@example.com
  ☐ Rob Smith     rob.smith@example.com   [no account yet]

  Expires in (days)  Label                    ☐ Allow downloading the MP4
  [ 30 ]             [ Grandparents      ]
  [ Create link ]

  Existing links
  ┌────────────────────────────────────────────────────────────────┐
  │ LABEL        RECIPIENTS    EXPIRES    DOWNLOAD  VIEWS          │
  │ Grandparents Dana Smith    18 May     no        4      [Revoke]│
  └────────────────────────────────────────────────────────────────┘
```

---

## Parent view — `/family` and `/share/[token]`

Deliberately plain. A parent has one job.

```
  Your family's highlights
  Reels your coach has shared with you. These are private to your account.

  ┌─────────────────────────────┐  ┌─────────────────────────────┐
  │ Jake Smith — Apr 18         │  │ Jake Smith — Spring 2026    │
  │ Jake Smith · game · 16:9    │  │ Jake Smith · season · 9:16  │
  │ ┌─────────────────────────┐ │  │ ┌─────────────────────────┐ │
  │ │      video player       │ │  │ │      video player       │ │
  │ └─────────────────────────┘ │  │ └─────────────────────────┘ │
  │ Download MP4                │  │                             │
  └─────────────────────────────┘  └─────────────────────────────┘
```

A link that does not resolve says why in a sentence a parent can act on: "This
link has expired", "This link was shared with specific families, and your
account is not one of them", "This reel is still rendering. Check back shortly."

---

## Reel output layout

What the rendered MP4 actually looks like.

```
  16:9 (1920×1080)                          9:16 (1080×1920)
  ┌──────────────────────────────────┐      ┌──────────────────┐
  │ ┌──────────────┐                 │      │  ┌────────────┐  │
  │ │RAY 4 - 3 OWL │  scorebug       │      │  │RAY 4-3 OWL │  │
  │ │      ▾6  2OUT│  top-left       │      │  └────────────┘  │
  │ └──────────────┘                 │      │   centred        │
  │                                  │      │                  │
  │           game footage           │      │  game footage    │
  │                                  │      │  pillarboxed     │
  │ ┌────────────────────┐      ┌──┐ │      │                  │
  │ │ Jake Smith #7      │      │▩ │ │      │ ┌──────────────┐ │
  │ │ 2-for-3, 2 RBI     │ logo └──┘ │      │ │Jake Smith #7 │ │
  │ └────────────────────┘           │      │ │2-for-3, 2 RBI│ │
  │  lower third, fades after 3.5s   │      │ └──────────────┘ │
  └──────────────────────────────────┘      └──────────────────┘

  Intro card (first 3 seconds, team primary colour)
  ┌──────────────────────────────────┐
  │              #7                  │  ← accent colour, 30% of height
  │          JAKE SMITH              │
  │   SS, P  |  Spring 2026 — Rays   │
  │                                  │
  │  .412      21       18       3   │
  │  AVG        H      RBI       HR  │
  │                             ▩    │
  └──────────────────────────────────┘  ← accent bar
```

Text colour on the intro card is chosen by relative luminance against the team's
primary colour, so both a navy team and a gold team get readable cards without
anyone configuring it.
