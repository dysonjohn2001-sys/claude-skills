-- Demo data: one team, one season, one game, a nine-player roster and the
-- consent records that unblock highlight generation.
--
-- Create your coach account FIRST, so this file can attach it to the team:
--
--   python3 scripts/create-user.py coach@example.com "Your Name" --role coach
--   psql "$DATABASE_URL" -f db/seed.sql
--
-- No user is created here on purpose. A seeded account with a known password is
-- how a private application ends up not being private.

BEGIN;

INSERT INTO teams (id, name, organization, age_group, primary_color, secondary_color, timezone, created_by)
VALUES ('22222222-2222-2222-2222-222222222222', 'Riverside Rays', 'Riverside Youth Baseball',
        '12U', '#0F2B5B', '#C8102E', 'America/New_York',
        (SELECT id FROM users WHERE role IN ('coach','admin') ORDER BY created_at LIMIT 1))
ON CONFLICT DO NOTHING;

INSERT INTO team_settings (team_id) VALUES ('22222222-2222-2222-2222-222222222222')
ON CONFLICT DO NOTHING;

-- Attach every existing coach or admin account to the demo team.
INSERT INTO team_members (team_id, user_id, role)
SELECT '22222222-2222-2222-2222-222222222222', id, role
  FROM users WHERE role IN ('coach', 'admin')
ON CONFLICT DO NOTHING;

INSERT INTO seasons (id, team_id, name, starts_on, ends_on)
VALUES ('33333333-3333-3333-3333-333333333333', '22222222-2222-2222-2222-222222222222',
        'Spring 2026', '2026-03-01', '2026-07-15')
ON CONFLICT DO NOTHING;

INSERT INTO tournaments (id, season_id, name, location, starts_on, ends_on)
VALUES ('44444444-4444-4444-4444-444444444444', '33333333-3333-3333-3333-333333333333',
        'Riverside Memorial Day Classic', 'Riverside Complex', '2026-05-23', '2026-05-25')
ON CONFLICT DO NOTHING;

INSERT INTO games (id, season_id, played_on, first_pitch_at, opponent_name, home_away, location)
VALUES ('55555555-5555-5555-5555-555555555555', '33333333-3333-3333-3333-333333333333',
        '2026-04-18', '2026-04-18 10:04:00-04', 'Northside Owls', 'away', 'Northside Park, Field 1')
ON CONFLICT DO NOTHING;

-- Roster matching samples/roster.csv.
INSERT INTO players (id, team_id, first_name, last_name, jersey_number, bats, throws, birth_year)
VALUES
  ('a0000000-0000-0000-0000-000000000001', '22222222-2222-2222-2222-222222222222', 'Jake',   'Smith',     '7',  'R','R',2013),
  ('a0000000-0000-0000-0000-000000000002', '22222222-2222-2222-2222-222222222222', 'Marcus', 'Hernandez', '12', 'L','R',2013),
  ('a0000000-0000-0000-0000-000000000003', '22222222-2222-2222-2222-222222222222', 'Owen',   'Brooks',    '21', 'R','R',2014),
  ('a0000000-0000-0000-0000-000000000004', '22222222-2222-2222-2222-222222222222', 'Daniel', 'Okafor',    '3',  'R','R',2013),
  ('a0000000-0000-0000-0000-000000000005', '22222222-2222-2222-2222-222222222222', 'Liam',   'Nguyen',    '15', 'L','L',2013),
  ('a0000000-0000-0000-0000-000000000006', '22222222-2222-2222-2222-222222222222', 'Sofia',  'Alvarez',   '9',  'R','R',2014),
  ('a0000000-0000-0000-0000-000000000007', '22222222-2222-2222-2222-222222222222', 'Ravi',   'Patel',     '24', 'R','R',2013),
  ('a0000000-0000-0000-0000-000000000008', '22222222-2222-2222-2222-222222222222', 'Cole',   'Whitfield', '5',  'L','R',2014),
  ('a0000000-0000-0000-0000-000000000009', '22222222-2222-2222-2222-222222222222', 'Theo',   'Moreau',    '11', 'R','R',2013)
ON CONFLICT DO NOTHING;

INSERT INTO player_positions (player_id, position, is_primary) VALUES
  ('a0000000-0000-0000-0000-000000000001','SS',TRUE),
  ('a0000000-0000-0000-0000-000000000001','P',FALSE),
  ('a0000000-0000-0000-0000-000000000002','2B',TRUE),
  ('a0000000-0000-0000-0000-000000000003','CF',TRUE),
  ('a0000000-0000-0000-0000-000000000004','C',TRUE),
  ('a0000000-0000-0000-0000-000000000005','1B',TRUE),
  ('a0000000-0000-0000-0000-000000000005','P',FALSE),
  ('a0000000-0000-0000-0000-000000000006','3B',TRUE),
  ('a0000000-0000-0000-0000-000000000007','LF',TRUE),
  ('a0000000-0000-0000-0000-000000000008','RF',TRUE),
  ('a0000000-0000-0000-0000-000000000009','2B',TRUE)
ON CONFLICT DO NOTHING;

INSERT INTO season_rosters (season_id, player_id)
SELECT '33333333-3333-3333-3333-333333333333', id FROM players
 WHERE team_id = '22222222-2222-2222-2222-222222222222'
ON CONFLICT DO NOTHING;

-- Batting order for the sample game.
INSERT INTO lineup_entries (game_id, player_id, batting_order, starting_position)
VALUES
  ('55555555-5555-5555-5555-555555555555','a0000000-0000-0000-0000-000000000001',1,'SS'),
  ('55555555-5555-5555-5555-555555555555','a0000000-0000-0000-0000-000000000002',2,'2B'),
  ('55555555-5555-5555-5555-555555555555','a0000000-0000-0000-0000-000000000003',3,'CF'),
  ('55555555-5555-5555-5555-555555555555','a0000000-0000-0000-0000-000000000004',4,'C'),
  ('55555555-5555-5555-5555-555555555555','a0000000-0000-0000-0000-000000000005',5,'P'),
  ('55555555-5555-5555-5555-555555555555','a0000000-0000-0000-0000-000000000006',6,'3B'),
  ('55555555-5555-5555-5555-555555555555','a0000000-0000-0000-0000-000000000007',7,'LF'),
  ('55555555-5555-5555-5555-555555555555','a0000000-0000-0000-0000-000000000008',8,'RF'),
  ('55555555-5555-5555-5555-555555555555','a0000000-0000-0000-0000-000000000009',9,'EH')
ON CONFLICT DO NOTHING;

-- Guardians, one per player.
INSERT INTO guardians (id, full_name, email, phone) VALUES
  ('b0000000-0000-0000-0000-000000000001','Dana Smith','dana.smith@example.com','555-0101'),
  ('b0000000-0000-0000-0000-000000000002','Rosa Hernandez','rosa.h@example.com','555-0102'),
  ('b0000000-0000-0000-0000-000000000003','Tim Brooks','tim.brooks@example.com','555-0103'),
  ('b0000000-0000-0000-0000-000000000004','Ada Okafor','ada.okafor@example.com','555-0104'),
  ('b0000000-0000-0000-0000-000000000005','Mai Nguyen','mai.nguyen@example.com','555-0105'),
  ('b0000000-0000-0000-0000-000000000006','Pilar Alvarez','pilar.a@example.com','555-0106'),
  ('b0000000-0000-0000-0000-000000000007','Anil Patel','anil.patel@example.com','555-0107'),
  ('b0000000-0000-0000-0000-000000000008','Kim Whitfield','kim.w@example.com','555-0108'),
  ('b0000000-0000-0000-0000-000000000009','Celine Moreau','celine.m@example.com','555-0109')
ON CONFLICT DO NOTHING;

INSERT INTO player_guardians (player_id, guardian_id, relationship, is_primary_contact)
SELECT
  ('a0000000-0000-0000-0000-00000000000' || n)::uuid,
  ('b0000000-0000-0000-0000-00000000000' || n)::uuid,
  'parent', TRUE
FROM generate_series(1, 9) AS n
ON CONFLICT DO NOTHING;

-- Consent. Everyone except #8 has granted the full set, so the demo shows both
-- the working path and the blocked path.
INSERT INTO consents (player_id, guardian_id, type, granted, note)
SELECT
  ('a0000000-0000-0000-0000-00000000000' || n)::uuid,
  ('b0000000-0000-0000-0000-00000000000' || n)::uuid,
  t::consent_type,
  (n <> 8),
  'seeded demo consent'
FROM generate_series(1, 9) AS n
CROSS JOIN unnest(ARRAY[
  'media_capture','highlight_generation','family_sharing','team_sharing'
]) AS t;

-- External sharing is off for everyone by default, deliberately.
INSERT INTO consents (player_id, guardian_id, type, granted, note)
SELECT
  ('a0000000-0000-0000-0000-00000000000' || n)::uuid,
  ('b0000000-0000-0000-0000-00000000000' || n)::uuid,
  'external_sharing', FALSE, 'seeded demo consent'
FROM generate_series(1, 9) AS n;

COMMIT;
