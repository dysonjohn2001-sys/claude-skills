# Database schema

PostgreSQL 16. Two migrations: `0001_init.sql` creates 31 tables and 15 enum
types, `0002_stat_views.sql` adds 5 derived views. Both have been applied
against a real PostgreSQL 16 instance, and the integration tests run against it.

## Enum types rather than check constraints

Fifteen enums (`clip_category`, `review_status`, `match_method`, `consent_type`,
`job_status`, and so on). The trade is known: adding a value needs a migration.
That is the point. `review_status` acquiring a sixth value should be a deliberate
act, not a typo in a string literal that silently creates a state nothing
handles.

---

## Identity and access

### `users`, `sessions`

Opaque session tokens, stored as SHA-256 hashes so a database leak does not hand
over live sessions. Passwords are scrypt with a 16-byte random salt, in
`scrypt$salt$hash` form. `password_hash` is nullable for magic-link accounts.

### `team_members`

Membership, checked on every team-scoped page. A user id in a URL is never taken
as authorisation.

---

## Team, season, roster

### `teams`, `team_settings`

Settings are a separate table keyed by `team_id`, holding the tunables a coach
can change: roll lengths, dead-time toggle, confidence thresholds, jersey OCR
on/off, music volume, ducking, which overlays to draw. A coach tunes once rather
than per clip.

### `players`

```sql
CREATE UNIQUE INDEX players_team_jersey_uniq
  ON players (team_id, jersey_number)
  WHERE is_active AND jersey_number IS NOT NULL;
```

A jersey number must be unique among active players. Two players sharing #7
breaks every number-based check downstream, and number-based matching that lies
is worse than none. Retired players keep their number, since the index is
partial.

`jersey_number` is **text**, not an integer: `07` and `7` are different on a
jersey, and matching is done on the number as printed.

`birth_year` is the year only. A full date of birth is more personal data than
this application ever needs; the year is enough for age-group checks.

### `player_positions`, `season_rosters`, `lineup_entries`

Positions are many-to-many with a primary flag. `lineup_entries` carries the
batting order plus `entered_inning` and `exited_inning`, which is what lets the
matcher refuse to put a substitute in a second-inning play.

---

## Guardians and consent

### `guardians`, `player_guardians`

A guardian record exists before an account does; `user_id` is nullable until an
invitation is accepted. Importing a roster with parent emails stages guardians
without sending anything.

### `consents` — append-only

```sql
CREATE TABLE consents (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  player_id    UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  guardian_id  UUID NOT NULL REFERENCES guardians(id) ON DELETE RESTRICT,
  type         consent_type NOT NULL,
  granted      BOOLEAN NOT NULL,
  granted_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  revoked_at   TIMESTAMPTZ,
  evidence_key TEXT,
  recorded_ip  INET,
  note         TEXT
);
```

The most important design decision in the schema. Consent rows are **never
updated**. A revocation is a new dated row. The record of what was permitted at
the moment a reel was made survives a later change of mind, which is exactly the
question that gets asked when something goes wrong.

`guardian_id` is `ON DELETE RESTRICT`, not `CASCADE`: deleting a guardian must
not silently erase the consent they gave.

The `effective_consents` view collapses this to current state with
`DISTINCT ON (player_id, type) ... ORDER BY granted_at DESC`. Application code
reads the view; only the consent route writes the table.

Five consent types, deliberately separate, because a parent who is happy for
their child to appear in team video is not thereby happy for the reel to be
posted publicly:

`media_capture` · `highlight_generation` · `family_sharing` · `team_sharing` ·
`external_sharing`

---

## Games and media

### `games`, `tournaments`

`first_pitch_at` is the anchor of last resort. With no per-play timestamps, it is
the only thing that lets the matcher pace plays through a recording.

### `media_assets`

`storage_key` is a relative key, not a path, so moving to object storage is a
narrow change. `recording_started_at` is read from container metadata by
`probe_media` and may be overridden by the coach.

### `media_sync_anchors`

```sql
CHECK (play_id IS NOT NULL OR wall_clock_at IS NOT NULL)
```

An anchor must point at *something*: either a known play or an explicit
wall-clock instant. An anchor with neither is not an anchor.

---

## Play-by-play

### `import_batches`

Every import keeps its filename, the column map that was inferred, the row
count, how many were applied, and the full error log as JSONB. When a coach asks
why a name did not match, the evidence is on disk.

### `plays`

`UNIQUE (game_id, sequence_no)` and an index on `(game_id, occurred_at)`, which
is the access pattern the matcher uses.

`is_our_offense` is a stored boolean rather than something derived at read time.
Getting it wrong assigns every clip to the wrong side of the ball, so it is
decided once, at import, where the team column or the coach's answer is in hand.

`raw_row` keeps the original CSV row as JSONB. Re-deriving anything later never
requires the original file.

### `play_participants`

One row per credited player per role. `player_id` is nullable, because an
unresolved name is still worth recording: `raw_name` plus `resolve_method`
becomes a review item rather than being thrown away.

---

## Clips

### `clips`

```sql
CREATE UNIQUE INDEX clips_play_player_uniq
  ON clips (play_id, player_id, category) WHERE play_id IS NOT NULL;

CREATE INDEX clips_review_idx
  ON clips (review_status) WHERE review_status = 'needs_review';
```

The unique index makes re-matching idempotent: the same play cannot produce two
identical clips for the same player. The partial review index stays small
because it only covers rows in one state, which is the queue the coach works
from.

`confidence_factors` and `rank_factors` are JSONB. They exist so the review
screen can explain itself. A number a coach cannot interrogate is a number they
will not trust.

### `clip_segments`

The dead-time result: sub-windows with a `keep` flag, stored rather than applied.
A coach can see what was trimmed and why.

### `jersey_observations`

Every digit read, with timestamp, OCR confidence and bounding box. Kept for
audit. Jersey recognition never overrides the scorebook, and this table is how
that claim is checkable after the fact.

---

## Reels and sharing

### `reels`

```sql
CHECK (
  (scope = 'game'       AND game_id       IS NOT NULL) OR
  (scope = 'tournament' AND tournament_id IS NOT NULL) OR
  (scope = 'season'     AND season_id     IS NOT NULL)
)
```

The scope and its target cannot disagree.

### `share_links`, `share_link_grants`, `share_views`

A share link is bound to named guardians through `share_link_grants`. **There is
no public link option in the schema.** A token that is not on a grant list opens
nothing, so a forwarded URL is inert for anyone who was not invited.

`token_hash` is SHA-256; the raw token is shown once at creation and cannot be
recovered. Links carry an expiry, an optional view cap and a revocation
timestamp.

### `audit_log`

Append-only: logins and failures, uploads, imports, matching runs, review
decisions, consent changes, share creation and revocation, reel renders.

---

## Job queue

### `jobs`

```sql
CREATE INDEX jobs_claim_idx ON jobs (status, run_after) WHERE status = 'queued';
```

Claimed with:

```sql
WITH next AS (
  SELECT id FROM jobs
   WHERE status = 'queued' AND run_after <= now()
   ORDER BY created_at
   FOR UPDATE SKIP LOCKED
   LIMIT 1
)
UPDATE jobs j SET status = 'running', locked_by = $1, ...
```

`SKIP LOCKED` is what makes multi-worker safe with no coordination: a worker
that would block on a locked row takes the next one instead. An integration test
asserts two workers polling simultaneously cannot claim the same job.

Failures requeue with exponential backoff (30s, 60s, 120s) up to `max_attempts`,
then fail with the error text kept.

---

## Derived views

`0002_stat_views.sql` computes statistics rather than storing them, so a
corrected play-by-play import instantly corrects every overlay with no
recomputation job:

| View | Feeds |
|---|---|
| `player_game_batting` | Per-game stat overlays, reel intro cards |
| `player_game_pitching` | Pitching stat lines |
| `player_game_fielding` | Putouts, assists, errors |
| `player_season_batting` | Season intro cards, batting average |
| `review_queue` | The cross-game review queue, ordered highest rank first, lowest confidence first |

`review_queue`'s ordering is the point: the clip most likely to end up in a reel
while being wrong is the one the coach should look at first.

---

## Applying the schema

```bash
psql "$DATABASE_URL" -f db/migrations/0001_init.sql
psql "$DATABASE_URL" -f db/migrations/0002_stat_views.sql
psql "$DATABASE_URL" -f db/seed.sql     # optional demo data
```

`pgcrypto` (for `gen_random_uuid()`) and `citext` (for case-insensitive emails)
are created by the first migration.
