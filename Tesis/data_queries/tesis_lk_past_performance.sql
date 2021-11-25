-- Form (Performance ultimos partidos - general, local, visitante)
DROP TABLE IF EXISTS fdm.tesis_lk_past_performance_0;
CREATE TABLE fdm.tesis_lk_past_performance_0 AS (
WITH match_history AS(
SELECT --Home
	fixtures.league_id, fixtures.league_season, fixtures.league_round, league_round_number, fixtures.fixture_id,
	teams_home_id AS team_id,
	teams_home_name AS team_name,
	CASE 
		WHEN teams_home_winner=-1 THEN 'L'
		WHEN teams_home_winner=0 THEN 'D'
		WHEN teams_home_winner=1 THEN 'W' 
	END AS match_result,
	CASE 
		WHEN teams_home_winner=-1 THEN 0
		WHEN teams_home_winner=0 THEN 1
		WHEN teams_home_winner=1 THEN 3 
	END AS match_points,
	'Home' AS home_away
FROM fdm.ft_api_matches AS fixtures
LEFT JOIN fdm.lk_csv_league_rounds AS rounds
	ON fixtures.league_id=rounds.league_id AND fixtures.league_season=rounds.league_season 
	AND fixtures.league_round=rounds.league_round
WHERE CAST(fixtures.league_id AS text)||CAST(fixtures.league_season AS text) IN (
			SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_lk_leagues)
UNION
SELECT --Away
	fixtures.league_id, fixtures.league_season, fixtures.league_round, league_round_number, fixtures.fixture_id,
	teams_away_id AS team_id,
	teams_away_name AS team_name,
	CASE 
		WHEN teams_away_winner=-1 THEN 'L'
		WHEN teams_away_winner=0 THEN 'D'
		WHEN teams_away_winner=1 THEN 'W' 
	END AS match_result,
	CASE 
		WHEN teams_away_winner=-1 THEN 0
		WHEN teams_away_winner=0 THEN 1
		WHEN teams_away_winner=1 THEN 3 
	END AS match_points,
	'Away' AS home_away
FROM fdm.ft_api_matches AS fixtures
LEFT JOIN fdm.lk_csv_league_rounds AS rounds
	ON fixtures.league_id=rounds.league_id AND fixtures.league_season=rounds.league_season 
		AND fixtures.league_round=rounds.league_round
WHERE CAST(fixtures.league_id AS text)||CAST(fixtures.league_season AS text) IN (
			SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_lk_leagues)
ORDER BY league_id, league_season, league_round_number)
SELECT 
	*,	
	LAG(match_points, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS match_points_1,
	LAG(match_points, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS match_points_2,
	LAG(match_points, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS match_points_3,
	LAG(match_points, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS match_points_4,
	LAG(match_points, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS match_points_5,
	
	LAG(match_points, 1) OVER(PARTITION BY team_id, home_away ORDER BY league_id, league_season, league_round_number) AS match_points_ha_1,
	LAG(match_points, 2) OVER(PARTITION BY team_id, home_away ORDER BY league_id, league_season, league_round_number) AS match_points_ha_2,
	LAG(match_points, 3) OVER(PARTITION BY team_id, home_away ORDER BY league_id, league_season, league_round_number) AS match_points_ha_3,
	LAG(match_points, 4) OVER(PARTITION BY team_id, home_away ORDER BY league_id, league_season, league_round_number) AS match_points_ha_4,
	LAG(match_points, 5) OVER(PARTITION BY team_id, home_away ORDER BY league_id, league_season, league_round_number) AS match_points_ha_5,
	
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
	
FROM match_history);

DROP TABLE IF EXISTS fdm.tesis_lk_past_performance;
CREATE TABLE fdm.tesis_lk_past_performance AS (
WITH form AS (
SELECT *,
	CASE WHEN match_points_1 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN match_points_2 IS NOT NULL THEN 1 ELSE 0 END + 
    CASE WHEN match_points_3 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN match_points_4 IS NOT NULL THEN 1 ELSE 0 END + 
	CASE WHEN match_points_5 IS NOT NULL THEN 1 ELSE 0 END AS matches_hist_cnt,
	
	CASE WHEN match_points_ha_1 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN match_points_ha_2 IS NOT NULL THEN 1 ELSE 0 END + 
    CASE WHEN match_points_ha_3 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN match_points_ha_4 IS NOT NULL THEN 1 ELSE 0 END + 
	CASE WHEN match_points_ha_5 IS NOT NULL THEN 1 ELSE 0 END AS matches_hist_ha_cnt
FROM fdm.tesis_lk_past_performance_0
ORDER BY league_id, league_season, team_id, league_round_number)
SELECT
	league_id,
	league_season,
	league_round,
	league_round_number,
	fixture_id,
	team_id,
	team_name,
	home_away,
	match_result,
	match_points,
	matches_hist_cnt,
	matches_hist_ha_cnt,
	CONCAT(match_result_1, match_result_2, match_result_3, match_result_4, match_result_5) AS form,
	CASE WHEN matches_hist_cnt=0 THEN -1 ELSE (COALESCE(match_points_1, 0)+COALESCE(match_points_2, 0)+COALESCE(match_points_3, 0)+COALESCE(match_points_4, 0)+COALESCE(match_points_5, 0))/(CAST(matches_hist_cnt AS float)*3) END AS points_won_pct_l5,
	CONCAT(match_result_ha_1, match_result_ha_2, match_result_ha_3, match_result_ha_4, match_result_ha_5) AS ha_form,
	CASE WHEN matches_hist_ha_cnt=0 THEN -1 ELSE (COALESCE(match_points_ha_1, 0)+COALESCE(match_points_ha_2, 0)+COALESCE(match_points_ha_3, 0)+COALESCE(match_points_ha_4, 0)+COALESCE(match_points_ha_5, 0))/(CAST(matches_hist_ha_cnt AS float)*3) END AS ha_points_won_pct_l5
	
FROM form);

DROP TABLE IF EXISTS fdm.tesis_lk_past_performance_0;
	
	
	
	
	
	
	