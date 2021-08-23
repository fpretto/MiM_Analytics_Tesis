-- Rounds per season (grado de avance)
DROP TABLE IF EXISTS fdm.tesis_lk_rounds_season;
CREATE TABLE fdm.tesis_lk_rounds_season AS (
SELECT
	matches.league_id,
	matches.league_season,
	MAX(rounds.league_round_number) AS total_rounds,
	COUNT(DISTINCT teams_home_id) AS total_teams
	
FROM fdm.ft_api_matches AS matches
LEFT JOIN fdm.lk_csv_league_rounds AS rounds
	ON matches.league_id=rounds.league_id AND matches.league_season=rounds.league_season
WHERE CAST(matches.league_id AS text)||CAST(matches.league_season AS text) IN (
	SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_lk_leagues) 
GROUP BY matches.league_id, matches.league_season
ORDER BY matches.league_id, matches.league_season)