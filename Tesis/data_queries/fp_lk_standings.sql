DROP TABLE IF EXISTS fdm.fp_lk_standings;
CREATE TABLE fdm.fp_lk_standings AS (
WITH standings_home_away AS (
	SELECT 
		league_id, 
		league_season, 
		teams_home_id AS team_id, 
		SUM(CASE 
			WHEN teams_home_winner = 1 THEN 3
			WHEN teams_home_winner = 1 THEN 3
			ELSE 0 END) AS standings_points

	FROM fdm.ft_api_matches
	GROUP BY league_id,	league_season, teams_home_id
UNION ALL
	SELECT 
		league_id, 
		league_season, 
		teams_away_id AS team_id, 
		SUM(CASE 
			WHEN teams_away_winner = 1 THEN 3
			WHEN teams_away_winner = 1 THEN 3
			ELSE 0 END) AS standings_points

	FROM fdm.ft_api_matches
	GROUP BY league_id,	league_season, teams_away_id
)
SELECT 
	league_id, 
	league_season, 
	team_id,
	SUM(standings_points) AS standings_points,
	MIN(SUM(standings_points)) OVER(PARTITION BY league_id, league_season) AS standings_min_pts_season,
	MAX(SUM(standings_points)) OVER(PARTITION BY league_id, league_season) AS standings_max_pts_season,
	STDDEV(SUM(standings_points)) OVER(PARTITION BY league_id, league_season) AS standings_stddev_points,
	AVG(SUM(standings_points)) OVER(PARTITION BY league_id, league_season) AS standings_avg_points
	
FROM standings_home_away
GROUP BY league_id,	league_season, team_id
ORDER BY league_id,	league_season
);