-- Derived statistics used by the on-screen overlays and the intro cards.
-- Kept as views so a corrected play-by-play import instantly corrects every
-- overlay without a re-computation job.

BEGIN;

-- Per player, per game batting line.
CREATE VIEW player_game_batting AS
SELECT
  pp.player_id,
  p.game_id,
  COUNT(*) FILTER (WHERE p.play_type IN
    ('single','double','triple','home_run','strikeout','groundout','flyout','lineout','popout','fielders_choice','error_reached'))            AS at_bats,
  COUNT(*) FILTER (WHERE p.play_type IN ('single','double','triple','home_run'))  AS hits,
  COUNT(*) FILTER (WHERE p.play_type = 'double')                                  AS doubles,
  COUNT(*) FILTER (WHERE p.play_type = 'triple')                                  AS triples,
  COUNT(*) FILTER (WHERE p.play_type = 'home_run')                                AS home_runs,
  COUNT(*) FILTER (WHERE p.play_type = 'walk')                                    AS walks,
  COUNT(*) FILTER (WHERE p.play_type = 'strikeout')                               AS strikeouts,
  COALESCE(SUM(p.rbi), 0)                                                         AS rbi,
  COALESCE(SUM(p.runs_scored), 0)                                                 AS runs
FROM play_participants pp
JOIN plays p ON p.id = pp.play_id
WHERE pp.role = 'batter' AND pp.player_id IS NOT NULL
GROUP BY pp.player_id, p.game_id;

-- Per player, per game pitching line.
CREATE VIEW player_game_pitching AS
SELECT
  pp.player_id,
  p.game_id,
  COUNT(*) FILTER (WHERE p.play_type = 'strikeout')                          AS strikeouts,
  COUNT(*) FILTER (WHERE p.play_type = 'walk')                               AS walks_allowed,
  COUNT(*) FILTER (WHERE p.play_type IN ('single','double','triple','home_run')) AS hits_allowed,
  COUNT(DISTINCT p.inning)                                                   AS innings_touched,
  COUNT(*)                                                                   AS batters_faced
FROM play_participants pp
JOIN plays p ON p.id = pp.play_id
WHERE pp.role = 'pitcher' AND pp.player_id IS NOT NULL
GROUP BY pp.player_id, p.game_id;

-- Per player, per game fielding line.
CREATE VIEW player_game_fielding AS
SELECT
  pp.player_id,
  p.game_id,
  COUNT(*) FILTER (WHERE pp.role = 'fielder_putout') AS putouts,
  COUNT(*) FILTER (WHERE pp.role = 'fielder_assist') AS assists,
  COUNT(*) FILTER (WHERE pp.role = 'fielder_error')  AS errors
FROM play_participants pp
JOIN plays p ON p.id = pp.play_id
WHERE pp.player_id IS NOT NULL
  AND pp.role IN ('fielder_putout','fielder_assist','fielder_error')
GROUP BY pp.player_id, p.game_id;

-- Season rollup driving the intro card.
CREATE VIEW player_season_batting AS
SELECT
  b.player_id,
  g.season_id,
  SUM(b.at_bats)   AS at_bats,
  SUM(b.hits)      AS hits,
  SUM(b.home_runs) AS home_runs,
  SUM(b.rbi)       AS rbi,
  SUM(b.runs)      AS runs,
  CASE WHEN SUM(b.at_bats) > 0
       THEN ROUND(SUM(b.hits)::numeric / SUM(b.at_bats), 3)
       ELSE NULL END AS batting_average
FROM player_game_batting b
JOIN games g ON g.id = b.game_id
GROUP BY b.player_id, g.season_id;

-- Coach review queue, ordered so the most consequential uncertainty is first.
CREATE VIEW review_queue AS
SELECT
  c.id            AS clip_id,
  c.player_id,
  c.match_confidence,
  c.rank_score,
  c.category,
  pl.first_name || ' ' || pl.last_name AS player_name,
  g.id            AS game_id,
  g.played_on,
  g.opponent_name,
  p.description   AS play_description,
  p.inning,
  p.half
FROM clips c
JOIN players pl ON pl.id = c.player_id
LEFT JOIN plays p ON p.id = c.play_id
LEFT JOIN games g ON g.id = p.game_id
WHERE c.review_status = 'needs_review'
ORDER BY c.rank_score DESC, c.match_confidence ASC;

COMMIT;
