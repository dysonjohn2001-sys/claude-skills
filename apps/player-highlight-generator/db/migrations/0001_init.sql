-- Player Highlight Generator - initial schema
-- PostgreSQL 15+
-- Run: psql "$DATABASE_URL" -f db/migrations/0001_init.sql

BEGIN;

CREATE EXTENSION IF NOT EXISTS "pgcrypto";   -- gen_random_uuid()
CREATE EXTENSION IF NOT EXISTS "citext";     -- case-insensitive email

-- ---------------------------------------------------------------------------
-- Enumerated domains
-- ---------------------------------------------------------------------------

CREATE TYPE user_role          AS ENUM ('admin', 'coach', 'assistant_coach', 'guardian');
CREATE TYPE home_away          AS ENUM ('home', 'away', 'neutral');
CREATE TYPE media_kind         AS ENUM ('full_game', 'clip');
CREATE TYPE upload_status      AS ENUM ('pending', 'uploading', 'stored', 'probing', 'ready', 'failed');
CREATE TYPE import_kind        AS ENUM ('roster', 'play_by_play', 'lineup');
CREATE TYPE import_status      AS ENUM ('pending', 'parsing', 'needs_mapping', 'applied', 'failed');
CREATE TYPE participant_role   AS ENUM (
  'batter', 'pitcher', 'catcher', 'runner',
  'fielder_putout', 'fielder_assist', 'fielder_error', 'substitute'
);
CREATE TYPE clip_category      AS ENUM ('offense', 'defense', 'pitching', 'baserunning');
CREATE TYPE match_method       AS ENUM ('schedule', 'schedule_jersey', 'jersey_only', 'manual');
CREATE TYPE review_status      AS ENUM ('auto_approved', 'needs_review', 'approved', 'rejected');
CREATE TYPE reel_scope         AS ENUM ('game', 'tournament', 'season');
CREATE TYPE aspect_ratio       AS ENUM ('16:9', '9:16');
CREATE TYPE job_status         AS ENUM ('queued', 'running', 'succeeded', 'failed', 'cancelled');
CREATE TYPE consent_type       AS ENUM (
  'media_capture',        -- may appear in team-recorded video at all
  'highlight_generation', -- may have personal highlight reels built
  'family_sharing',       -- reels may be shared with that player's own guardians
  'team_sharing',         -- reels may be visible to other families on the team
  'external_sharing'      -- reels may be downloaded / posted off-platform
);

-- ---------------------------------------------------------------------------
-- Identity
-- ---------------------------------------------------------------------------

CREATE TABLE users (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email           CITEXT NOT NULL UNIQUE,
  full_name       TEXT   NOT NULL,
  password_hash   TEXT,                    -- NULL when the account is magic-link only
  role            user_role NOT NULL DEFAULT 'guardian',
  is_active       BOOLEAN NOT NULL DEFAULT TRUE,
  last_login_at   TIMESTAMPTZ,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE sessions (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id       UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token_hash    TEXT NOT NULL UNIQUE,      -- sha256 of the opaque cookie value
  expires_at    TIMESTAMPTZ NOT NULL,
  created_ip    INET,
  user_agent    TEXT,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX sessions_user_idx ON sessions (user_id);

-- ---------------------------------------------------------------------------
-- Team / season / roster
-- ---------------------------------------------------------------------------

CREATE TABLE teams (
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name               TEXT NOT NULL,
  organization       TEXT,
  age_group          TEXT,                 -- '10U', '12U', ...
  logo_key           TEXT,                 -- object-storage key
  primary_color      TEXT NOT NULL DEFAULT '#0F2B5B',
  secondary_color    TEXT NOT NULL DEFAULT '#C8102E',
  timezone           TEXT NOT NULL DEFAULT 'America/New_York',
  created_by         UUID REFERENCES users(id),
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Render + matching defaults live per team so a coach tunes once, not per clip.
CREATE TABLE team_settings (
  team_id                 UUID PRIMARY KEY REFERENCES teams(id) ON DELETE CASCADE,
  pre_roll_seconds        NUMERIC(5,2) NOT NULL DEFAULT 5.0  CHECK (pre_roll_seconds  BETWEEN 0 AND 30),
  post_roll_seconds       NUMERIC(5,2) NOT NULL DEFAULT 8.0  CHECK (post_roll_seconds BETWEEN 0 AND 60),
  dead_time_removal       BOOLEAN NOT NULL DEFAULT TRUE,
  motion_threshold        NUMERIC(5,4) NOT NULL DEFAULT 0.0150,
  auto_approve_threshold  NUMERIC(4,3) NOT NULL DEFAULT 0.800, -- >= this ships without review
  review_floor_threshold  NUMERIC(4,3) NOT NULL DEFAULT 0.450, -- <  this is discarded, not queued
  jersey_ocr_enabled      BOOLEAN NOT NULL DEFAULT TRUE,
  default_music_track_id  UUID,
  music_volume_db         NUMERIC(5,2) NOT NULL DEFAULT -18.0,
  duck_music_on_action    BOOLEAN NOT NULL DEFAULT TRUE,
  show_intro_card         BOOLEAN NOT NULL DEFAULT TRUE,
  show_score_overlay      BOOLEAN NOT NULL DEFAULT TRUE,
  show_stat_overlay       BOOLEAN NOT NULL DEFAULT TRUE,
  updated_at              TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE team_members (
  team_id     UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
  user_id     UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  role        user_role NOT NULL,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  PRIMARY KEY (team_id, user_id)
);

CREATE TABLE seasons (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  team_id     UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
  name        TEXT NOT NULL,               -- 'Spring 2026'
  starts_on   DATE NOT NULL,
  ends_on     DATE,
  is_active   BOOLEAN NOT NULL DEFAULT TRUE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (team_id, name)
);

CREATE TABLE players (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  team_id        UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
  first_name     TEXT NOT NULL,
  last_name      TEXT NOT NULL,
  preferred_name TEXT,
  jersey_number  TEXT,                     -- text: '07' and '7' are different on a jersey
  bats           CHAR(1) CHECK (bats  IN ('L','R','S')),
  throws         CHAR(1) CHECK (throws IN ('L','R')),
  birth_year     INT CHECK (birth_year BETWEEN 1990 AND 2100), -- year only; no full DOB stored
  photo_key      TEXT,
  is_active      BOOLEAN NOT NULL DEFAULT TRUE,
  created_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at     TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX players_team_idx ON players (team_id) WHERE is_active;
-- A jersey number must be unique among active players, or number-based matching lies.
CREATE UNIQUE INDEX players_team_jersey_uniq
  ON players (team_id, jersey_number)
  WHERE is_active AND jersey_number IS NOT NULL;

CREATE TABLE player_positions (
  player_id   UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  position    TEXT NOT NULL CHECK (position IN ('P','C','1B','2B','3B','SS','LF','CF','RF','DH','EH','UTIL')),
  is_primary  BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (player_id, position)
);

CREATE TABLE season_rosters (
  season_id   UUID NOT NULL REFERENCES seasons(id) ON DELETE CASCADE,
  player_id   UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  joined_on   DATE,
  left_on     DATE,
  PRIMARY KEY (season_id, player_id)
);

-- ---------------------------------------------------------------------------
-- Guardians, access and consent
-- ---------------------------------------------------------------------------

CREATE TABLE guardians (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id     UUID REFERENCES users(id) ON DELETE SET NULL, -- NULL until they accept an invite
  full_name   TEXT NOT NULL,
  email       CITEXT NOT NULL,
  phone       TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE player_guardians (
  player_id          UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  guardian_id        UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
  relationship       TEXT,                 -- 'mother', 'father', 'grandparent', 'legal guardian'
  is_primary_contact BOOLEAN NOT NULL DEFAULT FALSE,
  can_download       BOOLEAN NOT NULL DEFAULT TRUE,
  PRIMARY KEY (player_id, guardian_id)
);

-- Consent is per player, per type, and append-only: a revocation is a new row
-- with revoked_at set, never an UPDATE that erases the original grant.
CREATE TABLE consents (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  player_id     UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  guardian_id   UUID NOT NULL REFERENCES guardians(id) ON DELETE RESTRICT,
  type          consent_type NOT NULL,
  granted       BOOLEAN NOT NULL,
  granted_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
  revoked_at    TIMESTAMPTZ,
  evidence_key  TEXT,                      -- signed PDF / screenshot of the form
  recorded_ip   INET,
  note          TEXT
);
CREATE INDEX consents_player_type_idx ON consents (player_id, type, granted_at DESC);

-- Current effective consent, newest row wins.
CREATE VIEW effective_consents AS
SELECT DISTINCT ON (player_id, type)
  player_id, type, granted, granted_at, revoked_at,
  (granted AND revoked_at IS NULL) AS is_active
FROM consents
ORDER BY player_id, type, granted_at DESC;

-- ---------------------------------------------------------------------------
-- Games, tournaments
-- ---------------------------------------------------------------------------

CREATE TABLE tournaments (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  season_id   UUID NOT NULL REFERENCES seasons(id) ON DELETE CASCADE,
  name        TEXT NOT NULL,
  location    TEXT,
  starts_on   DATE,
  ends_on     DATE,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE games (
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  season_id          UUID NOT NULL REFERENCES seasons(id) ON DELETE CASCADE,
  tournament_id      UUID REFERENCES tournaments(id) ON DELETE SET NULL,
  played_on          DATE NOT NULL,
  first_pitch_at     TIMESTAMPTZ,          -- wall clock; anchors play timestamps
  opponent_name      TEXT NOT NULL,
  home_away          home_away NOT NULL DEFAULT 'home',
  location           TEXT,
  score_us           INT,
  score_them         INT,
  notes              TEXT,
  created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at         TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX games_season_date_idx ON games (season_id, played_on DESC);

CREATE TABLE lineup_entries (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id          UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
  player_id        UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  batting_order    INT CHECK (batting_order BETWEEN 1 AND 20),
  starting_position TEXT,
  entered_inning   INT NOT NULL DEFAULT 1,
  exited_inning    INT,
  UNIQUE (game_id, player_id, entered_inning)
);
CREATE INDEX lineup_game_order_idx ON lineup_entries (game_id, batting_order);

-- ---------------------------------------------------------------------------
-- Media
-- ---------------------------------------------------------------------------

CREATE TABLE media_assets (
  id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id              UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
  kind                 media_kind NOT NULL DEFAULT 'full_game',
  storage_key          TEXT NOT NULL,
  original_filename    TEXT,
  byte_size            BIGINT,
  checksum_sha256      TEXT,
  duration_seconds     NUMERIC(10,3),
  width                INT,
  height               INT,
  fps                  NUMERIC(7,3),
  has_audio            BOOLEAN,
  -- Wall-clock instant corresponding to video time 0. Read from container
  -- metadata when present, otherwise entered by the coach.
  recording_started_at TIMESTAMPTZ,
  status               upload_status NOT NULL DEFAULT 'pending',
  error_message        TEXT,
  uploaded_by          UUID REFERENCES users(id),
  created_at           TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX media_game_idx ON media_assets (game_id);

-- A coach marks "this moment in the video is this moment in the game". Two or
-- more anchors let the worker solve for clock drift as well as offset.
CREATE TABLE media_sync_anchors (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  media_asset_id    UUID NOT NULL REFERENCES media_assets(id) ON DELETE CASCADE,
  video_seconds     NUMERIC(10,3) NOT NULL,
  play_id           UUID,                  -- FK added after plays exists
  wall_clock_at     TIMESTAMPTZ,
  source            TEXT NOT NULL DEFAULT 'manual',
  created_by        UUID REFERENCES users(id),
  created_at        TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (play_id IS NOT NULL OR wall_clock_at IS NOT NULL)
);

-- ---------------------------------------------------------------------------
-- Play-by-play
-- ---------------------------------------------------------------------------

CREATE TABLE import_batches (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id      UUID REFERENCES games(id) ON DELETE CASCADE,
  team_id      UUID REFERENCES teams(id) ON DELETE CASCADE,
  kind         import_kind NOT NULL,
  filename     TEXT,
  source_label TEXT,                        -- 'gamechanger_export_csv', 'manual', ...
  row_count    INT NOT NULL DEFAULT 0,
  applied_count INT NOT NULL DEFAULT 0,
  status       import_status NOT NULL DEFAULT 'pending',
  column_map   JSONB NOT NULL DEFAULT '{}'::jsonb,
  error_log    JSONB NOT NULL DEFAULT '[]'::jsonb,
  created_by   UUID REFERENCES users(id),
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE plays (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  game_id          UUID NOT NULL REFERENCES games(id) ON DELETE CASCADE,
  import_batch_id  UUID REFERENCES import_batches(id) ON DELETE SET NULL,
  sequence_no      INT NOT NULL,
  inning           INT NOT NULL CHECK (inning BETWEEN 1 AND 30),
  half             TEXT NOT NULL CHECK (half IN ('top','bottom')),
  occurred_at      TIMESTAMPTZ,            -- wall clock, when the export carries it
  play_type        TEXT NOT NULL,          -- 'single','strikeout','stolen_base','putout',...
  result           TEXT,
  description      TEXT NOT NULL,
  batter_name_raw  TEXT,
  pitcher_name_raw TEXT,
  is_our_offense   BOOLEAN NOT NULL,
  outs_before      INT CHECK (outs_before BETWEEN 0 AND 2),
  balls            INT CHECK (balls   BETWEEN 0 AND 3),
  strikes          INT CHECK (strikes BETWEEN 0 AND 2),
  rbi              INT NOT NULL DEFAULT 0,
  runs_scored      INT NOT NULL DEFAULT 0,
  score_us         INT,
  score_them       INT,
  leverage_tag     TEXT,                   -- 'tying_run','walk_off','bases_loaded', ...
  raw_row          JSONB NOT NULL DEFAULT '{}'::jsonb,
  created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  UNIQUE (game_id, sequence_no)
);
CREATE INDEX plays_game_time_idx ON plays (game_id, occurred_at);

ALTER TABLE media_sync_anchors
  ADD CONSTRAINT media_sync_anchors_play_fk
  FOREIGN KEY (play_id) REFERENCES plays(id) ON DELETE SET NULL;

CREATE TABLE play_participants (
  id                 UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  play_id            UUID NOT NULL REFERENCES plays(id) ON DELETE CASCADE,
  player_id          UUID REFERENCES players(id) ON DELETE SET NULL,
  role               participant_role NOT NULL,
  raw_name           TEXT,
  raw_jersey_number  TEXT,
  resolve_confidence NUMERIC(4,3) NOT NULL DEFAULT 0.0,
  resolve_method     TEXT,                 -- 'exact_name','fuzzy_name','batting_order','jersey','manual'
  UNIQUE (play_id, role, player_id)
);
CREATE INDEX play_participants_player_idx ON play_participants (player_id);

-- ---------------------------------------------------------------------------
-- Clips
-- ---------------------------------------------------------------------------

CREATE TABLE clips (
  id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  play_id              UUID REFERENCES plays(id) ON DELETE CASCADE,
  player_id            UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  media_asset_id       UUID NOT NULL REFERENCES media_assets(id) ON DELETE CASCADE,
  category             clip_category NOT NULL,
  -- Window into the source asset, already including roll.
  source_start_seconds NUMERIC(10,3) NOT NULL,
  source_end_seconds   NUMERIC(10,3) NOT NULL,
  pre_roll_seconds     NUMERIC(5,2) NOT NULL DEFAULT 5.0,
  post_roll_seconds    NUMERIC(5,2) NOT NULL DEFAULT 8.0,
  match_method         match_method NOT NULL,
  match_confidence     NUMERIC(4,3) NOT NULL,
  confidence_factors   JSONB NOT NULL DEFAULT '{}'::jsonb,
  review_status        review_status NOT NULL DEFAULT 'needs_review',
  reviewed_by          UUID REFERENCES users(id),
  reviewed_at          TIMESTAMPTZ,
  rank_score           NUMERIC(6,3) NOT NULL DEFAULT 0,
  rank_factors         JSONB NOT NULL DEFAULT '{}'::jsonb,
  slowmo_start_seconds NUMERIC(10,3),      -- offsets relative to clip start
  slowmo_end_seconds   NUMERIC(10,3),
  slowmo_rate          NUMERIC(4,2) CHECK (slowmo_rate BETWEEN 0.1 AND 1.0),
  thumbnail_key        TEXT,
  preview_key          TEXT,
  title                TEXT,
  coach_note           TEXT,
  created_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at           TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (source_end_seconds > source_start_seconds)
);
CREATE INDEX clips_player_idx ON clips (player_id, rank_score DESC);
CREATE INDEX clips_review_idx  ON clips (review_status) WHERE review_status = 'needs_review';
CREATE UNIQUE INDEX clips_play_player_uniq ON clips (play_id, player_id, category)
  WHERE play_id IS NOT NULL;

-- Dead-time removal result: the sub-windows of a clip actually worth keeping.
CREATE TABLE clip_segments (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  clip_id        UUID NOT NULL REFERENCES clips(id) ON DELETE CASCADE,
  position       INT NOT NULL,
  start_seconds  NUMERIC(10,3) NOT NULL,   -- relative to clip start
  end_seconds    NUMERIC(10,3) NOT NULL,
  keep           BOOLEAN NOT NULL DEFAULT TRUE,
  motion_score   NUMERIC(6,4),
  reason         TEXT,
  UNIQUE (clip_id, position),
  CHECK (end_seconds > start_seconds)
);

-- Every jersey-number read the vision pass produced, kept for audit. Jersey
-- recognition never overrides the schedule match on its own; it only adjusts
-- confidence or breaks a tie.
CREATE TABLE jersey_observations (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  media_asset_id  UUID NOT NULL REFERENCES media_assets(id) ON DELETE CASCADE,
  clip_id         UUID REFERENCES clips(id) ON DELETE CASCADE,
  video_seconds   NUMERIC(10,3) NOT NULL,
  digits          TEXT NOT NULL,
  ocr_confidence  NUMERIC(4,3) NOT NULL,
  bbox            JSONB,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX jersey_obs_clip_idx ON jersey_observations (clip_id);

-- ---------------------------------------------------------------------------
-- Reels, music, rendering
-- ---------------------------------------------------------------------------

CREATE TABLE music_tracks (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  team_id       UUID REFERENCES teams(id) ON DELETE CASCADE, -- NULL = library default
  title         TEXT NOT NULL,
  artist        TEXT,
  license       TEXT NOT NULL,             -- 'CC0', 'licensed:<ref>', 'coach_upload'
  storage_key   TEXT NOT NULL,
  duration_seconds NUMERIC(10,3),
  loudness_lufs NUMERIC(6,2),
  is_default    BOOLEAN NOT NULL DEFAULT FALSE,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

ALTER TABLE team_settings
  ADD CONSTRAINT team_settings_music_fk
  FOREIGN KEY (default_music_track_id) REFERENCES music_tracks(id) ON DELETE SET NULL;

CREATE TABLE reels (
  id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  player_id        UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
  scope            reel_scope NOT NULL,
  game_id          UUID REFERENCES games(id) ON DELETE CASCADE,
  tournament_id    UUID REFERENCES tournaments(id) ON DELETE CASCADE,
  season_id        UUID REFERENCES seasons(id) ON DELETE CASCADE,
  title            TEXT NOT NULL,
  aspect           aspect_ratio NOT NULL DEFAULT '16:9',
  music_track_id   UUID REFERENCES music_tracks(id) ON DELETE SET NULL,
  music_volume_db  NUMERIC(5,2) NOT NULL DEFAULT -18.0,
  settings         JSONB NOT NULL DEFAULT '{}'::jsonb,
  output_key       TEXT,
  duration_seconds NUMERIC(10,3),
  byte_size        BIGINT,
  rendered_at      TIMESTAMPTZ,
  created_by       UUID REFERENCES users(id),
  created_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
  CHECK (
    (scope = 'game'       AND game_id       IS NOT NULL) OR
    (scope = 'tournament' AND tournament_id IS NOT NULL) OR
    (scope = 'season'     AND season_id     IS NOT NULL)
  )
);
CREATE INDEX reels_player_idx ON reels (player_id, created_at DESC);

CREATE TABLE reel_clips (
  reel_id        UUID NOT NULL REFERENCES reels(id) ON DELETE CASCADE,
  clip_id        UUID NOT NULL REFERENCES clips(id) ON DELETE CASCADE,
  position       INT NOT NULL,
  include_slowmo BOOLEAN NOT NULL DEFAULT FALSE,
  PRIMARY KEY (reel_id, clip_id),
  UNIQUE (reel_id, position) DEFERRABLE INITIALLY DEFERRED
);

CREATE TABLE jobs (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_type      TEXT NOT NULL,             -- 'probe_media','match_plays','detect_jersey','cut_clips','render_reel'
  target_type   TEXT NOT NULL,
  target_id     UUID NOT NULL,
  payload       JSONB NOT NULL DEFAULT '{}'::jsonb,
  status        job_status NOT NULL DEFAULT 'queued',
  progress      NUMERIC(5,2) NOT NULL DEFAULT 0,
  attempts      INT NOT NULL DEFAULT 0,
  max_attempts  INT NOT NULL DEFAULT 3,
  locked_by     TEXT,
  locked_at     TIMESTAMPTZ,
  error         TEXT,
  log           JSONB NOT NULL DEFAULT '[]'::jsonb,
  run_after     TIMESTAMPTZ NOT NULL DEFAULT now(),
  started_at    TIMESTAMPTZ,
  finished_at   TIMESTAMPTZ,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX jobs_claim_idx ON jobs (status, run_after) WHERE status = 'queued';
CREATE INDEX jobs_target_idx ON jobs (target_type, target_id);

-- ---------------------------------------------------------------------------
-- Sharing
-- ---------------------------------------------------------------------------

CREATE TABLE share_links (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  reel_id         UUID NOT NULL REFERENCES reels(id) ON DELETE CASCADE,
  token_hash      TEXT NOT NULL UNIQUE,    -- sha256; the raw token is shown once
  label           TEXT,
  allow_download  BOOLEAN NOT NULL DEFAULT FALSE,
  expires_at      TIMESTAMPTZ NOT NULL,
  max_views       INT,
  view_count      INT NOT NULL DEFAULT 0,
  revoked_at      TIMESTAMPTZ,
  created_by      UUID REFERENCES users(id),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- A share link is bound to named guardians. There are no public links.
CREATE TABLE share_link_grants (
  share_link_id  UUID NOT NULL REFERENCES share_links(id) ON DELETE CASCADE,
  guardian_id    UUID NOT NULL REFERENCES guardians(id) ON DELETE CASCADE,
  PRIMARY KEY (share_link_id, guardian_id)
);

CREATE TABLE share_views (
  id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  share_link_id  UUID NOT NULL REFERENCES share_links(id) ON DELETE CASCADE,
  guardian_id    UUID REFERENCES guardians(id) ON DELETE SET NULL,
  viewed_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
  ip             INET,
  user_agent     TEXT
);

CREATE TABLE audit_log (
  id           BIGSERIAL PRIMARY KEY,
  actor_user_id UUID REFERENCES users(id) ON DELETE SET NULL,
  action       TEXT NOT NULL,
  entity_type  TEXT NOT NULL,
  entity_id    UUID,
  metadata     JSONB NOT NULL DEFAULT '{}'::jsonb,
  ip           INET,
  created_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX audit_entity_idx ON audit_log (entity_type, entity_id, created_at DESC);

COMMIT;
