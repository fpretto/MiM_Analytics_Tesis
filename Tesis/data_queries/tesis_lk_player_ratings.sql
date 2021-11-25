-- Player Match Stats (Avg Rating by Position for Starting XI)
DROP TABLE IF EXISTS fdm.tesis_lk_player_ratings;
CREATE TABLE fdm.tesis_lk_player_ratings AS (
WITH 
rating_hist AS (
	SELECT
		matches.league_id,
		matches.league_season,
		matches.league_round,
		rounds.league_round_number,
		stats.fixture_id, 
		stats.team_id,
		stats.player_id,
		stats.player_position,
		stats.player_rating,
		LAG(stats.player_rating, 1) OVER(PARTITION BY matches.league_id, matches.league_season, player_id 
										 ORDER BY matches.league_id, matches.league_season, rounds.league_round_number) AS player_rating_l1,
		LAG(stats.player_rating, 2) OVER(PARTITION BY matches.league_id, matches.league_season, player_id 
										 ORDER BY matches.league_id, matches.league_season, rounds.league_round_number) AS player_rating_l2,
		LAG(stats.player_rating, 3) OVER(PARTITION BY matches.league_id, matches.league_season, player_id 
										 ORDER BY matches.league_id, matches.league_season, rounds.league_round_number) AS player_rating_l3,
		LAG(stats.player_rating, 4) OVER(PARTITION BY matches.league_id, matches.league_season, player_id 
										 ORDER BY matches.league_id, matches.league_season, rounds.league_round_number) AS player_rating_l4,
		LAG(stats.player_rating, 5) OVER(PARTITION BY matches.league_id, matches.league_season, player_id 
										 ORDER BY matches.league_id, matches.league_season, rounds.league_round_number) AS player_rating_l5
	FROM fdm.ft_api_matches_stats_players AS stats
	LEFT JOIN fdm.ft_api_matches AS matches
		ON stats.fixture_id=matches.fixture_id
	LEFT JOIN fdm.lk_csv_league_rounds AS rounds
		ON matches.league_id=rounds.league_id AND matches.league_season=rounds.league_season 
			AND matches.league_round=rounds.league_round
	WHERE CAST(matches.league_id AS text)||CAST(matches.league_season AS text) IN (
			SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_lk_leagues)
	ORDER BY matches.league_id, matches.league_season, rounds.league_round_number, stats.player_id),
player_ratings AS (
	SELECT
		*,
		CASE WHEN player_rating_l1 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN player_rating_l2 IS NOT NULL THEN 1 ELSE 0 END + 
		CASE WHEN player_rating_l3 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN player_rating_l4 IS NOT NULL THEN 1 ELSE 0 END + 
		CASE WHEN player_rating_l5 IS NOT NULL THEN 1 ELSE 0 END AS player_rating_cnt

	FROM rating_hist),
start_xi_player_ratings AS (
	SELECT 
		player_ratings.*,
		CASE WHEN player_rating_cnt=0 THEN 0 
		ELSE (COALESCE(player_rating_l1, 0)+COALESCE(player_rating_l2, 0)+COALESCE(player_rating_l3, 0)+COALESCE(player_rating_l4, 0)+
			  COALESCE(player_rating_l5, 0))/player_rating_cnt END AS avg_player_rating_l5
	FROM player_ratings
	LEFT JOIN fdm.ft_api_matches_lineups_players AS lineup_players
		ON player_ratings.fixture_id=lineup_players.fixture_id AND player_ratings.team_id=lineup_players.team_id 
		AND player_ratings.player_id=lineup_players.player_id
	WHERE lineup_players.start_xi=true)
SELECT 
	start_xi_player_ratings.league_id,
	start_xi_player_ratings.league_season,
	start_xi_player_ratings.league_round,
	start_xi_player_ratings.league_round_number,
	start_xi_player_ratings.fixture_id, 
	start_xi_player_ratings.team_id, 
	AVG(CASE WHEN player_position='G' THEN NULLIF(avg_player_rating_l5, 0) END) AS GK_rating_l5,
	AVG(CASE WHEN player_position='D' THEN NULLIF(avg_player_rating_l5, 0) END) AS DF_rating_l5,
	AVG(CASE WHEN player_position='M' THEN NULLIF(avg_player_rating_l5, 0) END) AS MF_rating_l5,
	AVG(CASE WHEN player_position='F' THEN NULLIF(avg_player_rating_l5, 0) END) AS FW_rating_l5,
	AVG(NULLIF(avg_player_rating_l5, 0)) AS TEAM_rating_l5
	
FROM start_xi_player_ratings
GROUP BY league_id,	league_season, league_round, league_round_number, fixture_id, team_id
ORDER BY league_id, league_season, league_round_number, team_id, fixture_id);