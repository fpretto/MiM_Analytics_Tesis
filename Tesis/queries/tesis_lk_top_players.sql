-- Top Scorers, Assisters and Goalkeepers
-- Top Scorers
DROP TABLE IF EXISTS fdm.tesis_lk_top_scorers_0;
CREATE TABLE fdm.tesis_lk_top_scorers_0 AS (
WITH 
rounds AS ( 
	SELECT DISTINCT fixtures.league_id, fixtures.league_season, fixtures.league_round, rounds.league_round_number
	FROM fdm.ft_api_matches as fixtures
	LEFT JOIN fdm.lk_csv_league_rounds AS rounds
		ON fixtures.league_id=rounds.league_id AND fixtures.league_season=rounds.league_season AND fixtures.league_round=rounds.league_round
	WHERE CAST(fixtures.league_id AS text)||CAST(fixtures.league_season AS text) IN (
		SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_lk_leagues)),
scorers_season AS (
	SELECT DISTINCT matches.league_id, matches.league_season, stats.player_id
	FROM fdm.ft_api_matches AS matches
	LEFT JOIN fdm.ft_api_matches_stats_players AS stats
	ON stats.fixture_id=matches.fixture_id
	WHERE goals_total > 0),
scorers_round AS (
	SELECT DISTINCT matches.league_id, matches.league_season, matches.league_round, stats.player_id, stats.goals_total
	FROM fdm.ft_api_matches AS matches
	LEFT JOIN fdm.ft_api_matches_stats_players AS stats
	ON stats.fixture_id=matches.fixture_id
	WHERE goals_total > 0)
SELECT
	rounds.league_id,
	rounds.league_season,
	rounds.league_round,
	rounds.league_round_number,
	scorers_season.player_id,
	COALESCE(scorers_round.goals_total, 0) AS goals_round,
	SUM(COALESCE(scorers_round.goals_total, 0)) OVER (PARTITION BY rounds.league_id, rounds.league_season, scorers_season.player_id
								 ORDER BY rounds.league_id, rounds.league_season, rounds.league_round_number) AS goals_season
FROM rounds 
LEFT JOIN scorers_season
ON rounds.league_id=scorers_season.league_id AND rounds.league_season=scorers_season.league_season
LEFT JOIN scorers_round
ON rounds.league_id=scorers_round.league_id AND rounds.league_season=scorers_round.league_season
	AND rounds.league_round=scorers_round.league_round AND scorers_season.player_id=scorers_round.player_id
ORDER BY rounds.league_id, rounds.league_season, rounds.league_round_number, goals_season DESC);

DROP TABLE IF EXISTS fdm.tesis_lk_top_scorers;
CREATE TABLE fdm.tesis_lk_top_scorers AS (
WITH lagged_goals AS(
SELECT *,
	LAG(goals_season, 1) OVER(PARTITION BY league_id, league_season, player_id ORDER BY league_id, league_season, league_round_number) AS goals_season_l1
FROM fdm.tesis_lk_top_scorers_0)
SELECT 
	*,
	CASE WHEN goals_season_l1=0 OR goals_season_l1 IS NULL THEN 0 
	ELSE DENSE_RANK() OVER(PARTITION BY league_id, league_season, league_round_number 
					  ORDER BY league_id, league_season, league_round_number, goals_season_l1 DESC) END AS scorer_rank_l1
FROM lagged_goals
ORDER BY league_id, league_season, league_round_number, goals_season_l1 DESC);

DROP TABLE IF EXISTS fdm.tesis_lk_top_scorers_0;

-- Top Assisters
DROP TABLE IF EXISTS fdm.tesis_lk_top_assisters_0;
CREATE TABLE fdm.tesis_lk_top_assisters_0 AS (
WITH 
rounds AS ( 
	SELECT DISTINCT fixtures.league_id, fixtures.league_season, fixtures.league_round, rounds.league_round_number
	FROM fdm.ft_api_matches as fixtures
	LEFT JOIN fdm.lk_csv_league_rounds AS rounds
		ON fixtures.league_id=rounds.league_id AND fixtures.league_season=rounds.league_season AND fixtures.league_round=rounds.league_round
	WHERE CAST(fixtures.league_id AS text)||CAST(fixtures.league_season AS text) IN (
		SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_lk_leagues)),
assisters_season AS (
	SELECT DISTINCT matches.league_id, matches.league_season, stats.player_id
	FROM fdm.ft_api_matches AS matches
	LEFT JOIN fdm.ft_api_matches_stats_players AS stats
	ON stats.fixture_id=matches.fixture_id
	WHERE goals_assists > 0),
assisters_round AS (
	SELECT DISTINCT matches.league_id, matches.league_season, matches.league_round, stats.player_id, stats.goals_assists
	FROM fdm.ft_api_matches AS matches
	LEFT JOIN fdm.ft_api_matches_stats_players AS stats
	ON stats.fixture_id=matches.fixture_id
	WHERE goals_assists > 0)
SELECT 
	rounds.league_id,
	rounds.league_season,
	rounds.league_round,
	rounds.league_round_number,
	assisters_season.player_id,
	COALESCE(assisters_round.goals_assists, 0) AS assists_round,
	SUM(COALESCE(assisters_round.goals_assists, 0)) OVER (PARTITION BY rounds.league_id, rounds.league_season, assisters_season.player_id
								 ORDER BY rounds.league_id, rounds.league_season, rounds.league_round_number) AS assists_season
FROM rounds 
LEFT JOIN assisters_season
ON rounds.league_id=assisters_season.league_id AND rounds.league_season=assisters_season.league_season
LEFT JOIN assisters_round
ON rounds.league_id=assisters_round.league_id AND rounds.league_season=assisters_round.league_season
	AND rounds.league_round=assisters_round.league_round AND assisters_season.player_id=assisters_round.player_id
ORDER BY rounds.league_id, rounds.league_season, rounds.league_round_number, assists_season DESC);

DROP TABLE IF EXISTS fdm.tesis_lk_top_assisters;
CREATE TABLE fdm.tesis_lk_top_assisters AS (
WITH lagged_assists AS(
SELECT *,
	LAG(assists_season, 1) OVER(PARTITION BY league_id, league_season, player_id ORDER BY league_id, league_season, league_round_number) AS assists_season_l1
FROM fdm.tesis_lk_top_assisters_0)
SELECT 
	*,
	CASE WHEN assists_season_l1=0 OR assists_season_l1 IS NULL THEN 0 
	ELSE DENSE_RANK() OVER(PARTITION BY league_id, league_season, league_round_number 
					  ORDER BY league_id, league_season, league_round_number, assists_season_l1 DESC) END AS assister_rank_l1
FROM lagged_assists
ORDER BY league_id, league_season, league_round_number, assists_season_l1 DESC);

DROP TABLE IF EXISTS fdm.tesis_lk_top_assisters_0;

-- Top Goals Saved (by GK)
DROP TABLE IF EXISTS fdm.tesis_lk_top_savers_0;
CREATE TABLE fdm.tesis_lk_top_savers_0 AS (
WITH 
rounds AS ( 
	SELECT DISTINCT fixtures.league_id, fixtures.league_season, fixtures.league_round, rounds.league_round_number
	FROM fdm.ft_api_matches as fixtures
	LEFT JOIN fdm.lk_csv_league_rounds AS rounds
		ON fixtures.league_id=rounds.league_id AND fixtures.league_season=rounds.league_season AND fixtures.league_round=rounds.league_round
	WHERE CAST(fixtures.league_id AS text)||CAST(fixtures.league_season AS text) IN (
		SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_lk_leagues)),
savers_season AS (
	SELECT DISTINCT matches.league_id, matches.league_season, stats.player_id
	FROM fdm.ft_api_matches AS matches
	LEFT JOIN fdm.ft_api_matches_stats_players AS stats
	ON stats.fixture_id=matches.fixture_id
	WHERE goals_saves > 0 AND stats.player_position='G'),
savers_round AS (
	SELECT DISTINCT matches.league_id, matches.league_season, matches.league_round, stats.player_id, stats.goals_saves
	FROM fdm.ft_api_matches AS matches
	LEFT JOIN fdm.ft_api_matches_stats_players AS stats
	ON stats.fixture_id=matches.fixture_id
	WHERE goals_saves > 0 AND stats.player_position='G')
SELECT
	rounds.league_id,
	rounds.league_season,
	rounds.league_round,
	rounds.league_round_number,
	savers_season.player_id,
	COALESCE(savers_round.goals_saves, 0) AS saves_round,
	SUM(COALESCE(savers_round.goals_saves, 0)) OVER (PARTITION BY rounds.league_id, rounds.league_season, savers_season.player_id
								 ORDER BY rounds.league_id, rounds.league_season, rounds.league_round_number) AS saves_season
FROM rounds 
LEFT JOIN savers_season
ON rounds.league_id=savers_season.league_id AND rounds.league_season=savers_season.league_season
LEFT JOIN savers_round
ON rounds.league_id=savers_round.league_id AND rounds.league_season=savers_round.league_season
	AND rounds.league_round=savers_round.league_round AND savers_season.player_id=savers_round.player_id
ORDER BY rounds.league_id, rounds.league_season, rounds.league_round_number, saves_season DESC);

DROP TABLE IF EXISTS fdm.tesis_lk_top_savers;
CREATE TABLE fdm.tesis_lk_top_savers AS (
WITH lagged_saves AS(
SELECT *,
	LAG(saves_season, 1) OVER(PARTITION BY league_id, league_season, player_id ORDER BY league_id, league_season, league_round_number) AS saves_season_l1
FROM fdm.tesis_lk_top_savers_0)
SELECT 
	*,
	CASE WHEN saves_season_l1=0 OR saves_season_l1 IS NULL THEN 0 
	ELSE DENSE_RANK() OVER(PARTITION BY league_id, league_season, league_round_number 
					  ORDER BY league_id, league_season, league_round_number, saves_season_l1 DESC) END AS saver_rank_l1
FROM lagged_saves
ORDER BY league_id, league_season, league_round_number, saves_season_l1 DESC);

DROP TABLE IF EXISTS fdm.tesis_lk_top_savers_0;