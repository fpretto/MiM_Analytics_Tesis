-- Player Match Stats (Avg Rating by Position)
DROP TABLE IF EXISTS fdm.tesis_lk_player_ratings_0;
CREATE TABLE fdm.tesis_lk_player_ratings_0 AS(
WITH player_ratings_round AS (
SELECT
	matches.league_id,
	matches.league_season,
	matches.league_round,
	rounds.league_round_number,
	stats.fixture_id, 
	stats.team_id, 
	AVG(CASE WHEN player_position='G' THEN player_rating END) AS GK_rating,
	AVG(CASE WHEN player_position='D' THEN player_rating END) AS DF_rating,
	AVG(CASE WHEN player_position='M' THEN player_rating END) AS MF_rating,
	AVG(CASE WHEN player_position='F' THEN player_rating END) AS FW_rating

FROM fdm.ft_api_matches_stats_players AS stats
LEFT JOIN fdm.ft_api_matches AS matches
	ON stats.fixture_id=matches.fixture_id
LEFT JOIN fdm.lk_csv_league_rounds AS rounds
	ON matches.league_id=rounds.league_id AND matches.league_season=rounds.league_season 
		AND matches.league_round=rounds.league_round
WHERE CAST(matches.league_id AS text)||CAST(matches.league_season AS text) IN (
		SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_lk_leagues)
GROUP BY matches.league_id, matches.league_season,	matches.league_round, rounds.league_round_number,
		stats.fixture_id, stats.team_id
ORDER BY matches.league_id, matches.league_season, rounds.league_round_number)
SELECT
	*,
	LAG(GK_rating, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS GK_rating_1,
	LAG(GK_rating, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS GK_rating_2,
	LAG(GK_rating, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS GK_rating_3,
	LAG(GK_rating, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS GK_rating_4,
	LAG(GK_rating, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS GK_rating_5,
	
	LAG(DF_rating, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS DF_rating_1,
	LAG(DF_rating, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS DF_rating_2,
	LAG(DF_rating, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS DF_rating_3,
	LAG(DF_rating, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS DF_rating_4,
	LAG(DF_rating, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS DF_rating_5,
	
	LAG(MF_rating, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS MF_rating_1,
	LAG(MF_rating, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS MF_rating_2,
	LAG(MF_rating, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS MF_rating_3,
	LAG(MF_rating, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS MF_rating_4,
	LAG(MF_rating, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS MF_rating_5,
	
	LAG(FW_rating, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS FW_rating_1,
	LAG(FW_rating, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS FW_rating_2,
	LAG(FW_rating, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS FW_rating_3,
	LAG(FW_rating, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS FW_rating_4,
	LAG(FW_rating, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS FW_rating_5
	
FROM player_ratings_round);
		
-- Tabla Final
DROP TABLE IF EXISTS fdm.tesis_lk_player_ratings;
CREATE TABLE fdm.tesis_lk_player_ratings AS(
WITH player_ratings AS (
SELECT *,
	CASE WHEN GK_rating_1 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN GK_rating_2 IS NOT NULL THEN 1 ELSE 0 END + 
    CASE WHEN GK_rating_3 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN GK_rating_4 IS NOT NULL THEN 1 ELSE 0 END + 
	CASE WHEN GK_rating_5 IS NOT NULL THEN 1 ELSE 0 END AS gk_rating_cnt,
	
	CASE WHEN DF_rating_1 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN DF_rating_2 IS NOT NULL THEN 1 ELSE 0 END + 
    CASE WHEN DF_rating_3 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN DF_rating_4 IS NOT NULL THEN 1 ELSE 0 END + 
	CASE WHEN DF_rating_5 IS NOT NULL THEN 1 ELSE 0 END AS df_rating_cnt,
	
	CASE WHEN MF_rating_1 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN MF_rating_2 IS NOT NULL THEN 1 ELSE 0 END + 
    CASE WHEN MF_rating_3 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN MF_rating_4 IS NOT NULL THEN 1 ELSE 0 END + 
	CASE WHEN MF_rating_5 IS NOT NULL THEN 1 ELSE 0 END AS mf_rating_cnt,
	
	CASE WHEN FW_rating_1 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN FW_rating_2 IS NOT NULL THEN 1 ELSE 0 END + 
    CASE WHEN FW_rating_3 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN FW_rating_4 IS NOT NULL THEN 1 ELSE 0 END + 
	CASE WHEN FW_rating_5 IS NOT NULL THEN 1 ELSE 0 END AS fw_rating_cnt
FROM fdm.tesis_lk_player_ratings_0)
SELECT 
	league_id,
	league_season,
	league_round,
	league_round_number,
	fixture_id,
	team_id,
	gk_rating_cnt,
	df_rating_cnt,
	mf_rating_cnt,
	fw_rating_cnt,	
	CASE WHEN gk_rating_cnt=0 THEN 0 ELSE (COALESCE(GK_rating_1, 0)+COALESCE(GK_rating_2, 0)+COALESCE(GK_rating_3, 0)+COALESCE(GK_rating_4, 0)+COALESCE(GK_rating_5, 0))/gk_rating_cnt END AS gk_rating_l5,
	CASE WHEN df_rating_cnt=0 THEN 0 ELSE (COALESCE(DF_rating_1, 0)+COALESCE(DF_rating_2, 0)+COALESCE(DF_rating_3, 0)+COALESCE(DF_rating_4, 0)+COALESCE(DF_rating_5, 0))/df_rating_cnt END AS df_rating_l5,
	CASE WHEN mf_rating_cnt=0 THEN 0 ELSE (COALESCE(MF_rating_1, 0)+COALESCE(MF_rating_2, 0)+COALESCE(MF_rating_3, 0)+COALESCE(MF_rating_4, 0)+COALESCE(MF_rating_5, 0))/mf_rating_cnt END AS mf_rating_l5,
	CASE WHEN fw_rating_cnt=0 THEN 0 ELSE (COALESCE(FW_rating_1, 0)+COALESCE(FW_rating_2, 0)+COALESCE(FW_rating_3, 0)+COALESCE(FW_rating_4, 0)+COALESCE(FW_rating_5, 0))/fw_rating_cnt END AS fw_rating_l5
FROM player_ratings);

DROP TABLE IF EXISTS fdm.tesis_lk_player_ratings_0;
