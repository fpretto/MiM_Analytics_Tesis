-- Ligas a utilizar
CREATE TABLE fdm.tesis_ligas AS (
SELECT * FROM fdm.fp_leagues_completeness
WHERE league_type='League' AND stats_teams_pct>70 AND stats_players_pct>50 AND league_name!='Serie B'
)

select * from fdm.lk_csv_league_rounds
where league_id=13
order by league_id, season

-- select * from pg_timezone_names;
SELECT 
	fixture_id,
	referee,
	to_timestamp(date_tz, 'YYYY-MM-DD"T"HH24:MI:SS') AT time zone 'America/Buenos_Aires' AS date_timestamp,
	DATE(to_timestamp(date_tz, 'YYYY-MM-DD"T"HH24:MI:SS') AT time zone 'America/Buenos_Aires') AS date_match,
	LEFT(RIGHT(TEXT(to_timestamp(date_tz, 'YYYY-MM-DD"T"HH24:MI:SS') AT time zone 'America/Buenos_Aires'), 8), 5) AS time_match,
	venue_id,
	league_id,
	league_season,
	league_round,
	CAST(RIGHT(league_round, 2) AS INT) AS round,
	teams_home_id,
	teams_home_name,
	teams_home_winner,
	teams_away_id,
	teams_away_name,
	teams_away_winner,
	goals_home,
	goals_away,
	CASE 
		WHEN teams_home_winner=1 THEN 'Home'
		WHEN teams_home_winner=-1 THEN 'Away'
	ELSE 'Draw' END as target
	
FROM fdm.ft_api_matches
WHERE CAST(league_id AS text)||CAST(league_season AS text) IN (
	SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_ligas) 
ORDER BY league_round

-- Rounds per season (grado de avance)
SELECT
	matches.league_id,
	matches.league_season,
	MAX(rounds.league_round_number) AS total_rounds
	
FROM fdm.ft_api_matches AS matches
LEFT JOIN fdm.lk_csv_league_rounds AS rounds
	ON matches.league_id=rounds.league_id AND matches.league_season=rounds.league_season
WHERE CAST(matches.league_id AS text)||CAST(matches.league_season AS text) IN (
	SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_ligas) 
GROUP BY matches.league_id, matches.league_season
ORDER BY matches.league_id, matches.league_season

-- Teams Match Stats
CREATE TEMP TABLE match_stats AS
SELECT
	stats.*,
	CASE WHEN stats.fl_home=true THEN away.fouls ELSE home.fouls END AS fouls_opp,
	CASE WHEN stats.fl_home=true THEN away.yellow_cards ELSE home.yellow_cards END AS yellow_cards_opp,
	CASE WHEN stats.fl_home=true THEN away.red_cards ELSE home.red_cards END AS red_cards_opp,
	CASE WHEN stats.fl_home=true THEN away.total_shots ELSE home.total_shots END AS total_shots_opp,
	CASE WHEN stats.fl_home=true THEN away.shots_on_goal ELSE home.shots_on_goal END AS shots_on_goal_opp,
	CASE WHEN stats.fl_home=true THEN away.shots_off_goal ELSE home.shots_off_goal END AS shots_off_goal_opp,
	CASE WHEN stats.fl_home=true THEN away.shots_insidebox ELSE home.shots_insidebox END AS shots_insidebox_opp,
	CASE WHEN stats.fl_home=true THEN away.shots_outsidebox ELSE home.shots_outsidebox END AS shots_outsidebox_opp,
	CASE WHEN stats.fl_home=true THEN away.blocked_shots ELSE home.blocked_shots END AS blocked_shots_opp,
	CASE WHEN stats.fl_home=true THEN away.corner_kicks ELSE home.corner_kicks END AS corner_kicks_opp

FROM fdm.ft_api_matches_stats_teams AS stats
LEFT JOIN (SELECT * FROM fdm.ft_api_matches_stats_teams WHERE fl_home=true) AS home
ON stats.fixture_id=home.fixture_id
LEFT JOIN (SELECT * FROM fdm.ft_api_matches_stats_teams WHERE fl_home=false) AS away
ON stats.fixture_id=away.fixture_id

-- Player Match Stats (Avg Rating by Position)
SELECT 
	fixture_id, 
	team_id, 
	AVG(CASE WHEN player_position='G' THEN player_rating END) AS GK_rating,
	AVG(CASE WHEN player_position='D' THEN player_rating END) AS DF_rating,
	AVG(CASE WHEN player_position='M' THEN player_rating END) AS MF_rating,
	AVG(CASE WHEN player_position='F' THEN player_rating END) AS FW_rating

FROM fdm.ft_api_matches_stats_players AS stats
GROUP BY fixture_id, team_id

-- Top Scorers
WITH 
rounds AS ( 
	SELECT DISTINCT fixtures.league_id, fixtures.league_season, fixtures.league_round, rounds.league_round_number
	FROM fdm.ft_api_matches as fixtures
	LEFT JOIN fdm.lk_csv_league_rounds AS rounds
		ON fixtures.league_id=rounds.league_id AND fixtures.league_season=rounds.league_season AND fixtures.league_round=rounds.league_round
	WHERE CAST(fixtures.league_id AS text)||CAST(fixtures.league_season AS text) IN (
		SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_ligas)),
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
ORDER BY rounds.league_id, rounds.league_season, rounds.league_round_number, goals_season DESC

-- Top Assisters
WITH 
rounds AS ( 
	SELECT DISTINCT fixtures.league_id, fixtures.league_season, fixtures.league_round, rounds.league_round_number
	FROM fdm.ft_api_matches as fixtures
	LEFT JOIN fdm.lk_csv_league_rounds AS rounds
		ON fixtures.league_id=rounds.league_id AND fixtures.league_season=rounds.league_season AND fixtures.league_round=rounds.league_round
	WHERE CAST(fixtures.league_id AS text)||CAST(fixtures.league_season AS text) IN (
		SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_ligas)),
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
ORDER BY rounds.league_id, rounds.league_season, rounds.league_round_number, assists_season DESC

-- Top Goals Saved (by GK)
WITH 
rounds AS ( 
	SELECT DISTINCT fixtures.league_id, fixtures.league_season, fixtures.league_round, rounds.league_round_number
	FROM fdm.ft_api_matches as fixtures
	LEFT JOIN fdm.lk_csv_league_rounds AS rounds
		ON fixtures.league_id=rounds.league_id AND fixtures.league_season=rounds.league_season AND fixtures.league_round=rounds.league_round
	WHERE CAST(fixtures.league_id AS text)||CAST(fixtures.league_season AS text) IN (
		SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_ligas)),
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
ORDER BY rounds.league_id, rounds.league_season, rounds.league_round_number, saves_season DESC

-- Standings by Round
WITH 
rounds AS(
	SELECT DISTINCT fixtures.league_id, fixtures.league_season, fixtures.league_round, rounds.league_round_number,
		teams_home_id AS team_id FROM fdm.ft_api_matches AS fixtures
		LEFT JOIN fdm.lk_csv_league_rounds AS rounds
			ON fixtures.league_id=rounds.league_id AND fixtures.league_season=rounds.league_season 
				AND fixtures.league_round=rounds.league_round
	UNION
	SELECT DISTINCT fixtures.league_id, fixtures.league_season, fixtures.league_round, rounds.league_round_number,
		teams_away_id AS team_id FROM fdm.ft_api_matches AS fixtures
		LEFT JOIN fdm.lk_csv_league_rounds AS rounds
			ON fixtures.league_id=rounds.league_id AND fixtures.league_season=rounds.league_season 
				AND fixtures.league_round=rounds.league_round),
results AS(
	SELECT
	rounds.league_id, 
	rounds.league_season, 
	rounds.league_round, 
	rounds.league_round_number,
	rounds.team_id, 
	COALESCE(matches_home.teams_home_name, matches_away.teams_away_name) AS team_name,
	CASE 
		WHEN matches_home.teams_home_name IS NOT NULL AND matches_home.teams_home_winner=-1 THEN 0
		WHEN matches_home.teams_home_name IS NOT NULL AND matches_home.teams_home_winner=0 THEN 1
		WHEN matches_home.teams_home_name IS NOT NULL AND matches_home.teams_home_winner=1 THEN 3
		WHEN matches_away.teams_away_name IS NOT NULL AND matches_away.teams_away_winner=-1 THEN 0
		WHEN matches_away.teams_away_name IS NOT NULL AND matches_away.teams_away_winner=0 THEN 1
		WHEN matches_away.teams_away_name IS NOT NULL AND matches_away.teams_away_winner=1 THEN 3
	ELSE -1 END AS points_round,
	CASE WHEN matches_home.teams_home_name IS NOT NULL THEN matches_home.goals_home
		ELSE matches_away.goals_away END AS goals_for_round,
	CASE WHEN matches_home.teams_home_name IS NOT NULL THEN matches_home.goals_away
		ELSE matches_away.goals_home END AS goals_against_round,
	CASE 
		WHEN matches_home.teams_home_name IS NOT NULL THEN matches_home.goals_home-matches_home.goals_away
	ELSE matches_away.goals_away-matches_away.goals_home END AS goals_diff_round							 
		
	FROM rounds
	LEFT JOIN fdm.ft_api_matches AS matches_home
		ON rounds.league_id=matches_home.league_id AND rounds.league_season=matches_home.league_season 
		AND rounds.league_round=matches_home.league_round AND rounds.team_id=matches_home.teams_home_id
	LEFT JOIN fdm.ft_api_matches AS matches_away
		ON rounds.league_id=matches_away.league_id AND rounds.league_season=matches_away.league_season 
		AND rounds.league_round=matches_away.league_round AND rounds.team_id=matches_away.teams_away_id
	WHERE CAST(rounds.league_id AS text)||CAST(rounds.league_season AS text) IN (
			SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_ligas)),
tabla_posiciones AS(
	SELECT *,
	CASE WHEN points_round = 3 THEN 1 ELSE 0 END game_won,
	CASE WHEN points_round = 1 THEN 1 ELSE 0 END game_draw,
	CASE WHEN points_round = 0 THEN 1 ELSE 0 END game_lose,
	SUM(points_round) OVER (PARTITION BY league_id, league_season, team_id
								 ORDER BY league_id, league_season, league_round_number) AS points_season,
	SUM(CASE WHEN points_round = 3 THEN 1 ELSE 0 END) OVER (PARTITION BY league_id, league_season, team_id
								 ORDER BY league_id, league_season, league_round_number) AS games_won_season,
	SUM(CASE WHEN points_round = 1 THEN 1 ELSE 0 END) OVER (PARTITION BY league_id, league_season, team_id
								 ORDER BY league_id, league_season, league_round_number) AS games_draw_season,
	SUM(CASE WHEN points_round = 0 THEN 1 ELSE 0 END) OVER (PARTITION BY league_id, league_season, team_id
								 ORDER BY league_id, league_season, league_round_number) AS games_lose_season,
	SUM(goals_for_round) OVER (PARTITION BY league_id, league_season, team_id
								 ORDER BY league_id, league_season, league_round_number) AS goals_for_season,
	SUM(goals_against_round) OVER (PARTITION BY league_id, league_season, team_id
								 ORDER BY league_id, league_season, league_round_number) AS goals_against_season,							
	SUM(goals_diff_round) OVER (PARTITION BY league_id, league_season, team_id
								 ORDER BY league_id, league_season, league_round_number) AS goals_diff_season
	FROM results)
SELECT 
	*,
	DENSE_RANK() OVER (PARTITION BY league_id, league_season, league_round_number
					 ORDER BY league_id, league_season, league_round_number, points_season DESC) AS rank
FROM tabla_posiciones
ORDER BY league_id, league_season, league_round_number, points_season DESC, goals_diff_season DESC

-- Form (Performance ultimos partidos - general, local, visitante)
WITH match_history AS(
SELECT --Home
	fixtures.league_id, fixtures.league_season, fixtures.league_round, league_round_number,
	teams_home_id AS team_id,
	teams_home_name AS team_name,
	teams_home_winner AS match_result,
	'Home' AS home_away
FROM fdm.ft_api_matches AS fixtures
LEFT JOIN fdm.lk_csv_league_rounds AS rounds
	ON fixtures.league_id=rounds.league_id AND fixtures.league_season=rounds.league_season 
		AND fixtures.league_round=rounds.league_round
WHERE CAST(rounds.league_id AS text)||CAST(rounds.league_season AS text) IN (
			SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_ligas)
UNION
SELECT --Away
	fixtures.league_id, fixtures.league_season, fixtures.league_round, league_round_number, 
	teams_away_id AS team_id,
	teams_away_name AS team_name,
	teams_away_winner AS match_result,
	'Away' AS home_away
FROM fdm.ft_api_matches AS fixtures
LEFT JOIN fdm.lk_csv_league_rounds AS rounds
	ON fixtures.league_id=rounds.league_id AND fixtures.league_season=rounds.league_season 
		AND fixtures.league_round=rounds.league_round
WHERE CAST(rounds.league_id AS text)||CAST(rounds.league_season AS text) IN (
			SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_ligas)
ORDER BY league_id, league_season, league_round_number)
SELECT 
	*,	
	LAG(match_result, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS match_result_1,
	LAG(match_result, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS match_result_2,
	LAG(match_result, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS match_result_3,
	LAG(match_result, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS match_result_4,
	LAG(match_result, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS match_result_5,
	
	LAG(match_result, 1) OVER(PARTITION BY team_id, home_away ORDER BY league_id, league_season, league_round_number) AS match_result_ha_1,
	LAG(match_result, 2) OVER(PARTITION BY team_id, home_away ORDER BY league_id, league_season, league_round_number) AS match_result_ha_2,
	LAG(match_result, 3) OVER(PARTITION BY team_id, home_away ORDER BY league_id, league_season, league_round_number) AS match_result_ha_3,
	LAG(match_result, 4) OVER(PARTITION BY team_id, home_away ORDER BY league_id, league_season, league_round_number) AS match_result_ha_4,
	LAG(match_result, 5) OVER(PARTITION BY team_id, home_away ORDER BY league_id, league_season, league_round_number) AS match_result_ha_5
	
FROM match_history

-- Cargar el csv con league_rounds (terminar de hacer el etl)