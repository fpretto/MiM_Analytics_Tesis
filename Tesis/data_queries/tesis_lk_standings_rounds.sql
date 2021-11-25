-- Standings by Round
DROP TABLE IF EXISTS fdm.tesis_lk_standings_rounds_0;
CREATE TABLE fdm.tesis_lk_standings_rounds_0 AS (
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
			SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_lk_leagues)),
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
ORDER BY league_id, league_season, league_round_number, points_season DESC, goals_diff_season DESC);

DROP TABLE IF EXISTS fdm.tesis_lk_standings_rounds;
CREATE TABLE fdm.tesis_lk_standings_rounds AS (
SELECT
	*,
	COALESCE(LAG(rank, 1) OVER(PARTITION BY league_id, league_season, team_id 
					  ORDER BY league_id, league_season, league_round_number), 0) AS rank_l1,
	COALESCE(LAG(points_season, 1) OVER(PARTITION BY league_id, league_season, team_id 
							   ORDER BY league_id, league_season, league_round_number), 0) AS points_season_l1,
	COALESCE(LAG(goals_diff_season, 1) OVER(PARTITION BY league_id, league_season, team_id 
								   ORDER BY league_id, league_season, league_round_number), 0) AS goals_diff_season_l1
	
FROM fdm.tesis_lk_standings_rounds_0);

DROP TABLE IF EXISTS fdm.tesis_lk_standings_rounds_0;

DROP TABLE IF EXISTS fdm.tesis_lk_standings_motivation;
CREATE TABLE fdm.tesis_lk_standings_motivation AS (
SELECT 
	standings.league_id,
	standings.league_season,
	standings.league_round,
	standings.league_round_number,
	MAX(standings.rank_l1) AS rank_last,
	MIN(standings.points_season_l1) AS rank_points_last,
	MAX(standings.points_season_l1) AS rank_points_leader,
	CAST(AVG(CASE WHEN standings.rank_l1=5 THEN standings.points_season_l1 ELSE NULL END) AS INT) AS rank_points_top5
	
FROM fdm.tesis_lk_standings_rounds AS standings
GROUP BY league_id, league_season, league_round, league_round_number
ORDER BY league_id, league_season, league_round_number);
