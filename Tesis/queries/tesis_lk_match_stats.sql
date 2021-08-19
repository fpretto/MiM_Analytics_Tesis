-- Teams Match Stats
DROP TABLE IF EXISTS fdm.tesis_lk_match_stats_0;
CREATE TABLE fdm.tesis_lk_match_stats_0 AS (
WITH match_stats AS (
SELECT
	matches.league_id,
	matches.league_season,
	matches.league_round,
	rounds.league_round_number,
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
LEFT JOIN fdm.ft_api_matches AS matches
	ON stats.fixture_id=matches.fixture_id
LEFT JOIN fdm.lk_csv_league_rounds AS rounds
	ON matches.league_id=rounds.league_id AND matches.league_season=rounds.league_season 
	AND matches.league_round=rounds.league_round
WHERE CAST(matches.league_id AS text)||CAST(matches.league_season AS text) IN (
			SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_lk_leagues)
ORDER BY matches.league_id, matches.league_season, rounds.league_round_number)
SELECT
	*,
	LAG(shots_on_goal, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_on_goal_1,
	LAG(shots_on_goal, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_on_goal_2,
	LAG(shots_on_goal, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_on_goal_3,
	LAG(shots_on_goal, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_on_goal_4,
	LAG(shots_on_goal, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_on_goal_5,

	LAG(shots_off_goal, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_off_goal_1,
	LAG(shots_off_goal, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_off_goal_2,
	LAG(shots_off_goal, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_off_goal_3,
	LAG(shots_off_goal, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_off_goal_4,
	LAG(shots_off_goal, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_off_goal_5,

	LAG(total_shots, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_shots_1,
	LAG(total_shots, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_shots_2,
	LAG(total_shots, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_shots_3,
	LAG(total_shots, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_shots_4,
	LAG(total_shots, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_shots_5,

	LAG(blocked_shots, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS blocked_shots_1,
	LAG(blocked_shots, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS blocked_shots_2,
	LAG(blocked_shots, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS blocked_shots_3,
	LAG(blocked_shots, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS blocked_shots_4,
	LAG(blocked_shots, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS blocked_shots_5,
	
	LAG(shots_insidebox, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_insidebox_1,
	LAG(shots_insidebox, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_insidebox_2,
	LAG(shots_insidebox, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_insidebox_3,
	LAG(shots_insidebox, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_insidebox_4,
	LAG(shots_insidebox, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_insidebox_5,
	
	LAG(shots_outsidebox, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_outsidebox_1,
	LAG(shots_outsidebox, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_outsidebox_2,
	LAG(shots_outsidebox, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_outsidebox_3,
	LAG(shots_outsidebox, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_outsidebox_4,
	LAG(shots_outsidebox, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_outsidebox_5,
	
	LAG(fouls, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS fouls_1,
	LAG(fouls, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS fouls_2,
	LAG(fouls, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS fouls_3,
	LAG(fouls, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS fouls_4,
	LAG(fouls, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS fouls_5,
	
	LAG(corner_kicks, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS corner_kicks_1,
	LAG(corner_kicks, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS corner_kicks_2,
	LAG(corner_kicks, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS corner_kicks_3,
	LAG(corner_kicks, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS corner_kicks_4,
	LAG(corner_kicks, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS corner_kicks_5,
	
	LAG(offsides, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS offsides_1,
	LAG(offsides, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS offsides_2,
	LAG(offsides, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS offsides_3,
	LAG(offsides, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS offsides_4,
	LAG(offsides, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS offsides_5,
	
	LAG(ball_possesion, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS ball_possesion_1,
	LAG(ball_possesion, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS ball_possesion_2,
	LAG(ball_possesion, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS ball_possesion_3,
	LAG(ball_possesion, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS ball_possesion_4,
	LAG(ball_possesion, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS ball_possesion_5,
	
	LAG(yellow_cards, 1) OVER(PARTITION BY league_season, team_id ORDER BY league_id, league_season, league_round_number) AS yellow_cards_1,
	LAG(yellow_cards, 2) OVER(PARTITION BY league_season, team_id ORDER BY league_id, league_season, league_round_number) AS yellow_cards_2,
	LAG(yellow_cards, 3) OVER(PARTITION BY league_season, team_id ORDER BY league_id, league_season, league_round_number) AS yellow_cards_3,
	LAG(yellow_cards, 4) OVER(PARTITION BY league_season, team_id ORDER BY league_id, league_season, league_round_number) AS yellow_cards_4,
	LAG(yellow_cards, 5) OVER(PARTITION BY league_season, team_id ORDER BY league_id, league_season, league_round_number) AS yellow_cards_5,
	
	LAG(red_cards, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS red_cards_1,
	LAG(red_cards, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS red_cards_2,
	LAG(red_cards, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS red_cards_3,
	LAG(red_cards, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS red_cards_4,
	LAG(red_cards, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS red_cards_5,
	
	LAG(goalkeeper_saves, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS goalkeeper_saves_1,
	LAG(goalkeeper_saves, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS goalkeeper_saves_2,
	LAG(goalkeeper_saves, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS goalkeeper_saves_3,
	LAG(goalkeeper_saves, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS goalkeeper_saves_4,
	LAG(goalkeeper_saves, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS goalkeeper_saves_5,

	LAG(total_passes, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_passes_1,
	LAG(total_passes, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_passes_2,
	LAG(total_passes, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_passes_3,
	LAG(total_passes, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_passes_4,
	LAG(total_passes, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_passes_5,

	LAG(passes_accurate, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS passes_accurate_1,
	LAG(passes_accurate, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS passes_accurate_2,
	LAG(passes_accurate, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS passes_accurate_3,
	LAG(passes_accurate, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS passes_accurate_4,
	LAG(passes_accurate, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS passes_accurate_5,

	LAG(passes_pct, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS passes_pct_1,
	LAG(passes_pct, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS passes_pct_2,
	LAG(passes_pct, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS passes_pct_3,
	LAG(passes_pct, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS passes_pct_4,
	LAG(passes_pct, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS passes_pct_5,

	LAG(fouls_opp, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS fouls_opp_1,
	LAG(fouls_opp, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS fouls_opp_2,
	LAG(fouls_opp, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS fouls_opp_3,
	LAG(fouls_opp, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS fouls_opp_4,
	LAG(fouls_opp, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS fouls_opp_5,

	LAG(yellow_cards_opp, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS yellow_cards_opp_1,
	LAG(yellow_cards_opp, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS yellow_cards_opp_2,
	LAG(yellow_cards_opp, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS yellow_cards_opp_3,
	LAG(yellow_cards_opp, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS yellow_cards_opp_4,
	LAG(yellow_cards_opp, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS yellow_cards_opp_5,

	LAG(red_cards_opp, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS red_cards_opp_1,
	LAG(red_cards_opp, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS red_cards_opp_2,
	LAG(red_cards_opp, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS red_cards_opp_3,
	LAG(red_cards_opp, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS red_cards_opp_4,
	LAG(red_cards_opp, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS red_cards_opp_5,

	LAG(total_shots_opp, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_shots_opp_1,
	LAG(total_shots_opp, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_shots_opp_2,
	LAG(total_shots_opp, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_shots_opp_3,
	LAG(total_shots_opp, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_shots_opp_4,
	LAG(total_shots_opp, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS total_shots_opp_5,

	LAG(shots_on_goal_opp, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_on_goal_opp_1,
	LAG(shots_on_goal_opp, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_on_goal_opp_2,
	LAG(shots_on_goal_opp, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_on_goal_opp_3,
	LAG(shots_on_goal_opp, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_on_goal_opp_4,
	LAG(shots_on_goal_opp, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_on_goal_opp_5,
	
	LAG(shots_off_goal_opp, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_off_goal_opp_1,
	LAG(shots_off_goal_opp, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_off_goal_opp_2,
	LAG(shots_off_goal_opp, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_off_goal_opp_3,
	LAG(shots_off_goal_opp, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_off_goal_opp_4,
	LAG(shots_off_goal_opp, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_off_goal_opp_5,
	
	LAG(shots_insidebox_opp, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_insidebox_opp_1,
	LAG(shots_insidebox_opp, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_insidebox_opp_2,
	LAG(shots_insidebox_opp, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_insidebox_opp_3,
	LAG(shots_insidebox_opp, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_insidebox_opp_4,
	LAG(shots_insidebox_opp, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_insidebox_opp_5,
	
	LAG(shots_outsidebox_opp, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_outsidebox_opp_1,
	LAG(shots_outsidebox_opp, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_outsidebox_opp_2,
	LAG(shots_outsidebox_opp, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_outsidebox_opp_3,
	LAG(shots_outsidebox_opp, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_outsidebox_opp_4,
	LAG(shots_outsidebox_opp, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS shots_outsidebox_opp_5,
	
	LAG(blocked_shots_opp, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS blocked_shots_opp_1,
	LAG(blocked_shots_opp, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS blocked_shots_opp_2,
	LAG(blocked_shots_opp, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS blocked_shots_opp_3,
	LAG(blocked_shots_opp, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS blocked_shots_opp_4,
	LAG(blocked_shots_opp, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS blocked_shots_opp_5,
	
	LAG(corner_kicks_opp, 1) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS corner_kicks_opp_1,
	LAG(corner_kicks_opp, 2) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS corner_kicks_opp_2,
	LAG(corner_kicks_opp, 3) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS corner_kicks_opp_3,
	LAG(corner_kicks_opp, 4) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS corner_kicks_opp_4,
	LAG(corner_kicks_opp, 5) OVER(PARTITION BY team_id ORDER BY league_id, league_season, league_round_number) AS corner_kicks_opp_5

FROM match_stats);

-- Final table
DROP TABLE IF EXISTS fdm.tesis_lk_match_stats;
CREATE TABLE fdm.tesis_lk_match_stats AS (
WITH match_hist AS (
SELECT *,
	CASE WHEN total_shots_1 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN total_shots_2 IS NOT NULL THEN 1 ELSE 0 END + 
    CASE WHEN total_shots_3 IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN total_shots_4 IS NOT NULL THEN 1 ELSE 0 END + 
	CASE WHEN total_shots_5 IS NOT NULL THEN 1 ELSE 0 END AS matches_hist_cnt
FROM fdm.tesis_lk_match_stats_0)
SELECT 
	league_id,
	league_season,
	league_round,
	league_round_number,
	fixture_id,
	team_id,
	team_name,
	fl_home,
	matches_hist_cnt,
	COALESCE(shots_on_goal_1, 0)+COALESCE(shots_on_goal_2, 0)+COALESCE(shots_on_goal_3, 0)+COALESCE(shots_on_goal_4, 0)+COALESCE(shots_on_goal_5, 0) AS shots_on_goal_l5,
	COALESCE(shots_off_goal_1, 0)+COALESCE(shots_off_goal_2, 0)+COALESCE(shots_off_goal_3, 0)+COALESCE(shots_off_goal_4, 0)+COALESCE(shots_off_goal_5, 0) AS shots_off_goal_l5,
	COALESCE(total_shots_1, 0)+COALESCE(total_shots_2, 0)+COALESCE(total_shots_3, 0)+COALESCE(total_shots_4, 0)+COALESCE(total_shots_5, 0) AS total_shots_l5,
	COALESCE(blocked_shots_1, 0)+COALESCE(blocked_shots_2, 0)+COALESCE(blocked_shots_3, 0)+COALESCE(blocked_shots_4, 0)+COALESCE(blocked_shots_5, 0) AS blocked_shots_l5,
	COALESCE(shots_insidebox_1, 0)+COALESCE(shots_insidebox_2, 0)+COALESCE(shots_insidebox_3, 0)+COALESCE(shots_insidebox_4, 0)+COALESCE(shots_insidebox_5, 0) AS shots_insidebox_l5,
	COALESCE(shots_outsidebox_1, 0)+COALESCE(shots_outsidebox_2, 0)+COALESCE(shots_outsidebox_3, 0)+COALESCE(shots_outsidebox_4, 0)+COALESCE(shots_outsidebox_5, 0) AS shots_outsidebox_l5,
	COALESCE(fouls_1, 0)+COALESCE(fouls_2, 0)+COALESCE(fouls_3, 0)+COALESCE(fouls_4, 0)+COALESCE(fouls_5, 0) AS fouls_l5,
	COALESCE(corner_kicks_1, 0)+COALESCE(corner_kicks_2, 0)+COALESCE(corner_kicks_3, 0)+COALESCE(corner_kicks_4, 0)+COALESCE(corner_kicks_5, 0) AS corner_kicks_l5,
	COALESCE(offsides_1, 0)+COALESCE(offsides_2, 0)+COALESCE(offsides_3, 0)+COALESCE(offsides_4, 0)+COALESCE(offsides_5, 0) AS offsides_l5,
	CASE WHEN matches_hist_cnt=0 THEN 0 ELSE (COALESCE(ball_possesion_1, 0)+COALESCE(ball_possesion_2, 0)+COALESCE(ball_possesion_3, 0)+COALESCE(ball_possesion_4, 0)+COALESCE(ball_possesion_5, 0))/matches_hist_cnt END AS ball_possesion_l5,
	COALESCE(yellow_cards_1, 0)+COALESCE(yellow_cards_2, 0)+COALESCE(yellow_cards_3, 0)+COALESCE(yellow_cards_4, 0)+COALESCE(yellow_cards_5, 0) AS yellow_cards_l5,
	COALESCE(red_cards_1, 0)+COALESCE(red_cards_2, 0)+COALESCE(red_cards_3, 0)+COALESCE(red_cards_4, 0)+COALESCE(red_cards_5, 0) AS red_cards_l5,
	COALESCE(goalkeeper_saves_1, 0)+COALESCE(goalkeeper_saves_2, 0)+COALESCE(goalkeeper_saves_3, 0)+COALESCE(goalkeeper_saves_4, 0)+COALESCE(goalkeeper_saves_5, 0) AS goalkeeper_saves_l5,
	COALESCE(total_passes_1, 0)+COALESCE(total_passes_2, 0)+COALESCE(total_passes_3, 0)+COALESCE(total_passes_4, 0)+COALESCE(total_passes_5, 0) AS total_passes_l5,
	COALESCE(passes_accurate_1, 0)+COALESCE(passes_accurate_2, 0)+COALESCE(passes_accurate_3, 0)+COALESCE(passes_accurate_4, 0)+COALESCE(passes_accurate_5, 0) AS passes_accurate_l5,
	CASE WHEN matches_hist_cnt=0 THEN 0 ELSE (COALESCE(passes_pct_1, 0)+COALESCE(passes_pct_2, 0)+COALESCE(passes_pct_3, 0)+COALESCE(passes_pct_4, 0)+COALESCE(passes_pct_5, 0))/matches_hist_cnt END AS passes_pct_l5,
	COALESCE(fouls_opp_1, 0)+COALESCE(fouls_opp_2, 0)+COALESCE(fouls_opp_3, 0)+COALESCE(fouls_opp_4, 0)+COALESCE(fouls_opp_5, 0) AS fouls_opp_l5,
	COALESCE(yellow_cards_opp_1, 0)+COALESCE(yellow_cards_opp_2, 0)+COALESCE(yellow_cards_opp_3, 0)+COALESCE(yellow_cards_opp_4, 0)+COALESCE(yellow_cards_opp_5, 0) AS yellow_cards_opp_l5,
	COALESCE(red_cards_opp_1, 0)+COALESCE(red_cards_opp_2, 0)+COALESCE(red_cards_opp_3, 0)+COALESCE(red_cards_opp_4, 0)+COALESCE(red_cards_opp_5, 0) AS red_cards_opp_l5,
	COALESCE(total_shots_opp_1, 0)+COALESCE(total_shots_opp_2, 0)+COALESCE(total_shots_opp_3, 0)+COALESCE(total_shots_opp_4, 0)+COALESCE(total_shots_opp_5, 0) AS total_shots_opp_l5,
	COALESCE(shots_on_goal_opp_1, 0)+COALESCE(shots_on_goal_opp_2, 0)+COALESCE(shots_on_goal_opp_3, 0)+COALESCE(shots_on_goal_opp_4, 0)+COALESCE(shots_on_goal_opp_5, 0) AS shots_on_goal_opp_l5,
	COALESCE(shots_off_goal_opp_1, 0)+COALESCE(shots_off_goal_opp_2, 0)+COALESCE(shots_off_goal_opp_3, 0)+COALESCE(shots_off_goal_opp_4, 0)+COALESCE(shots_off_goal_opp_5, 0) AS shots_off_goal_opp_l5,
	COALESCE(shots_insidebox_opp_1, 0)+COALESCE(shots_insidebox_opp_2, 0)+COALESCE(shots_insidebox_opp_3, 0)+COALESCE(shots_insidebox_opp_4, 0)+COALESCE(shots_insidebox_opp_5, 0) AS shots_insidebox_opp_l5,
	COALESCE(shots_outsidebox_opp_1, 0)+COALESCE(shots_outsidebox_opp_2, 0)+COALESCE(shots_outsidebox_opp_3, 0)+COALESCE(shots_outsidebox_opp_4, 0)+COALESCE(shots_outsidebox_opp_5, 0) AS shots_outsidebox_opp_l5,
	COALESCE(blocked_shots_opp_1, 0)+COALESCE(blocked_shots_opp_2, 0)+COALESCE(blocked_shots_opp_3, 0)+COALESCE(blocked_shots_opp_4, 0)+COALESCE(blocked_shots_opp_5, 0) AS blocked_shots_opp_l5,
	COALESCE(corner_kicks_opp_1, 0)+COALESCE(corner_kicks_opp_2, 0)+COALESCE(corner_kicks_opp_3, 0)+COALESCE(corner_kicks_opp_4, 0)+COALESCE(corner_kicks_opp_5, 0) AS corner_kicks_opp_l5

FROM match_hist);
	
DROP TABLE IF EXISTS fdm.tesis_lk_match_stats_0;
