-- Inital ABT
DROP TABLE IF EXISTS fdm.tesis_abt_0;
CREATE TABLE fdm.tesis_abt_0 AS (
SELECT 
-- Match Info
	matches.country_name,
	matches.country_code,
	matches.league_id,
	matches.league_name,
	matches.league_type,
	matches.league_season,
	matches.league_round,
	matches.league_round_number,
	matches.league_round_number/CAST(rounds.total_rounds AS float) AS league_progress,
	rounds.total_rounds,
	rounds.total_teams,
	matches.fixture_id,
	matches.referee,
	matches.date_tz,
	matches.date_match,
	To_Char(matches.date_match, 'Day') AS date_dow,
	matches.time_match,
	CASE 
		WHEN CAST(LEFT(matches.time_match, 2) AS INT)<13 THEN 'Morning'
		WHEN CAST(LEFT(matches.time_match, 2) AS INT)<18 THEN 'Afternoon'
	ELSE 'Evening' END AS date_day,
	matches.venue_id,
	matches.teams_home_id,
	matches.teams_home_name,
	matches.teams_away_id,
	matches.teams_away_name,
	matches.target,
-- Standings
	standing_motivation.rank_last,
	standing_motivation.rank_points_last,
	standing_motivation.rank_points_leader,
	standing_motivation.rank_points_top5,
	home_standing.rank_l1 AS home_rank,
	home_standing.points_season_l1 AS home_rank_points,
	home_standing.goals_diff_season_l1 AS home_rank_goals_diff,
	away_standing.rank_l1 AS away_rank,
	away_standing.points_season_l1 AS away_rank_points,
	away_standing.goals_diff_season_l1 AS away_rank_goals_diff,
-- Formation
	home_lineup.formation as home_formation,
	away_lineup.formation as away_formation,
-- Form
	home_form.form AS home_form,
	home_form.points_won_pct_l5 AS home_points_won_l5,
	home_form.form AS home_ha_form,
	home_form.ha_form AS home_ha_points_won_l5,
	away_form.ha_points_won_pct_l5 AS away_form,
	away_form.points_won_pct_l5 AS away_points_won_l5,
	away_form.ha_form AS away_ha_form,
	away_form.ha_points_won_pct_l5 AS away_ha_points_won_l5,
-- Player Ratings
	home_ratings.gk_rating_l5 AS home_gk_rating_l5,
	home_ratings.df_rating_l5 AS home_df_rating_l5,
	home_ratings.mf_rating_l5 AS home_mf_rating_l5,
	home_ratings.fw_rating_l5 AS home_fw_rating_l5,
	home_ratings.team_rating_l5 AS home_team_rating_l5,
	away_ratings.gk_rating_l5 AS away_gk_rating_l5,
	away_ratings.df_rating_l5 AS away_df_rating_l5,
	away_ratings.mf_rating_l5 AS away_mf_rating_l5,
	away_ratings.fw_rating_l5 AS away_fw_rating_l5,
	away_ratings.team_rating_l5 AS away_team_rating_l5,
-- Match History (Home)
	home_stats.matches_hist_cnt AS home_matches_cnt,
	away_stats.matches_hist_cnt AS away_matches_cnt,
	home_stats.shots_on_goal_l5 AS home_shots_on_goal_l5,
	home_stats.shots_off_goal_l5 AS home_shots_off_goal_l5,
	home_stats.total_shots_l5 AS home_total_shots_l5,
	home_stats.blocked_shots_l5 AS home_blocked_shots_l5,
	home_stats.shots_insidebox_l5 AS home_shots_insidebox_l5,
	home_stats.shots_outsidebox_l5 AS home_shots_outsidebox_l5,
	home_stats.fouls_l5 AS home_fouls_l5,
	home_stats.corner_kicks_l5 AS home_corner_kicks_l5,
	home_stats.offsides_l5 AS home_offsides_l5,
	home_stats.ball_possesion_l5 AS home_ball_possesion_l5,
	home_stats.yellow_cards_l5 AS home_yellow_cards_l5,
	home_stats.red_cards_l5 AS home_red_cards_l5,
	home_stats.goalkeeper_saves_l5 AS home_gk_saves_l5,
	home_stats.total_passes_l5 AS home_total_passes_l5,
	home_stats.passes_accurate_l5 AS home_passes_acc_l5,
	home_stats.passes_pct_l5 AS home_passes_pct_l5,
	home_stats.fouls_opp_l5 AS home_fouls_opp_l5,
	home_stats.yellow_cards_opp_l5 AS home_yellow_cards_opp_l5,
	home_stats.red_cards_opp_l5 AS home_red_cards_opp_l5,
	home_stats.total_shots_opp_l5 AS home_total_shots_opp_l5,
	home_stats.shots_on_goal_opp_l5 AS home_shots_on_goal_opp_l5,
	home_stats.shots_off_goal_opp_l5 AS home_shots_off_goal_opp_l5,
	home_stats.shots_insidebox_opp_l5 AS home_shots_outsidebox_opp_l5,
	home_stats.blocked_shots_opp_l5 AS home_blocked_shots_opp_l5,
	home_stats.corner_kicks_opp_l5 AS home_corner_kicks_opp_l5,
-- Match History (Away)
	away_stats.shots_on_goal_l5 AS away_shots_on_goal_l5,
	away_stats.shots_off_goal_l5 AS away_shots_off_goal_l5,
	away_stats.total_shots_l5 AS away_total_shots_l5,
	away_stats.blocked_shots_l5 AS away_blocked_shots_l5,
	away_stats.shots_insidebox_l5 AS away_shots_insidebox_l5,
	away_stats.shots_outsidebox_l5 AS away_shots_outsidebox_l5,
	away_stats.fouls_l5 AS away_fouls_l5,
	away_stats.corner_kicks_l5 AS away_corner_kicks_l5,
	away_stats.offsides_l5 AS away_offsides_l5,
	away_stats.ball_possesion_l5 AS away_ball_possesion_l5,
	away_stats.yellow_cards_l5 AS away_yellow_cards_l5,
	away_stats.red_cards_l5 AS away_red_cards_l5,
	away_stats.goalkeeper_saves_l5 AS away_gk_saves_l5,
	away_stats.total_passes_l5 AS away_total_passes_l5,
	away_stats.passes_accurate_l5 AS away_passes_acc_l5,
	away_stats.passes_pct_l5 AS away_passes_pct_l5,
	away_stats.fouls_opp_l5 AS away_fouls_opp_l5,
	away_stats.yellow_cards_opp_l5 AS away_yellow_cards_opp_l5,
	away_stats.red_cards_opp_l5 AS away_red_cards_opp_l5,
	away_stats.total_shots_opp_l5 AS away_total_shots_opp_l5,
	away_stats.shots_on_goal_opp_l5 AS away_shots_on_goal_opp_l5,
	away_stats.shots_off_goal_opp_l5 AS away_shots_off_goal_opp_l5,
	away_stats.shots_insidebox_opp_l5 AS away_shots_outsidebox_opp_l5,
	away_stats.blocked_shots_opp_l5 AS away_blocked_shots_opp_l5,
	away_stats.corner_kicks_opp_l5 AS away_corner_kicks_opp_l5
		 


FROM fdm.tesis_ft_matches AS matches
-- Rounds
LEFT JOIN fdm.tesis_lk_rounds_season AS rounds
	ON matches.league_id=rounds.league_id AND matches.league_season=rounds.league_season
-- Match Team Stats
LEFT JOIN (SELECT * FROM fdm.tesis_lk_match_stats WHERE fl_home=true) AS home_stats
	ON matches.fixture_id=home_stats.fixture_id
LEFT JOIN (SELECT * FROM fdm.tesis_lk_match_stats WHERE fl_home=false) AS away_stats
	ON matches.fixture_id=away_stats.fixture_id
-- Form
LEFT JOIN (SELECT * FROM fdm.tesis_lk_past_performance WHERE home_away='Home') AS home_form
	ON matches.fixture_id=home_form.fixture_id
LEFT JOIN (SELECT * FROM fdm.tesis_lk_past_performance WHERE home_away='Away') AS away_form
	ON matches.fixture_id=away_form.fixture_id
-- Ratings
LEFT JOIN fdm.tesis_lk_player_ratings AS home_ratings
	ON matches.fixture_id=home_ratings.fixture_id AND matches.teams_home_id=home_ratings.team_id
LEFT JOIN fdm.tesis_lk_player_ratings AS away_ratings
	ON matches.fixture_id=away_ratings.fixture_id AND matches.teams_away_id=away_ratings.team_id
-- Standings 
LEFT JOIN fdm.tesis_lk_standings_rounds AS home_standing
	ON matches.league_id=home_standing.league_id AND matches.league_season=home_standing.league_season 
	AND matches.league_round=home_standing.league_round AND matches.teams_home_id=home_standing.team_id
LEFT JOIN fdm.tesis_lk_standings_rounds AS away_standing
	ON matches.league_id=away_standing.league_id AND matches.league_season=away_standing.league_season 
	AND matches.league_round=away_standing.league_round AND matches.teams_away_id=away_standing.team_id
LEFT JOIN fdm.tesis_lk_standings_motivation AS standing_motivation
	ON matches.league_id=standing_motivation.league_id AND matches.league_season=standing_motivation.league_season 
	AND matches.league_round=standing_motivation.league_round
-- Formation
LEFT JOIN fdm.ft_api_matches_lineups_teams AS home_lineup
	ON matches.fixture_id=home_lineup.fixture_id AND matches.teams_home_id=home_lineup.team_id
LEFT JOIN fdm.ft_api_matches_lineups_teams AS away_lineup
	ON matches.fixture_id=away_lineup.fixture_id AND matches.teams_away_id=away_lineup.team_id);
	
---- Top Players
-- Scorers
DROP TABLE IF EXISTS home_max_scorers;
CREATE TEMPORARY TABLE home_max_scorers AS(
SELECT 
	matches.league_id,
	matches.league_season,
	matches.league_round,
	matches.league_round_number,
	matches.teams_home_id,
	MIN(NULLIF(scorer_rank_l1, 0)) AS max_scorer
	
FROM fdm.tesis_ft_matches AS matches
LEFT JOIN fdm.ft_api_matches_lineups_players AS lineup_players
	ON matches.fixture_id=lineup_players.fixture_id AND matches.teams_home_id=lineup_players.team_id
LEFT JOIN fdm.tesis_lk_top_scorers AS scorers
	ON matches.league_id=scorers.league_id AND matches.league_season=scorers.league_season AND matches.league_round=scorers.league_round
	AND lineup_players.player_id=scorers.player_id
WHERE lineup_players.start_xi=true
GROUP BY matches.league_id,	matches.league_season, matches.league_round, matches.league_round_number, matches.teams_home_id
ORDER BY matches.league_id,	matches.league_season, matches.league_round_number, max_scorer);

DROP TABLE IF EXISTS away_max_scorers;
CREATE TEMPORARY TABLE away_max_scorers AS(
SELECT 
	matches.league_id,
	matches.league_season,
	matches.league_round,
	matches.league_round_number,
	matches.teams_away_id,
	MIN(NULLIF(scorer_rank_l1, 0)) AS max_scorer
	
FROM fdm.tesis_ft_matches AS matches
LEFT JOIN fdm.ft_api_matches_lineups_players AS lineup_players
	ON matches.fixture_id=lineup_players.fixture_id AND matches.teams_away_id=lineup_players.team_id
LEFT JOIN fdm.tesis_lk_top_scorers AS scorers
	ON matches.league_id=scorers.league_id AND matches.league_season=scorers.league_season AND matches.league_round=scorers.league_round
	AND lineup_players.player_id=scorers.player_id
WHERE lineup_players.start_xi=true
GROUP BY matches.league_id,	matches.league_season, matches.league_round, matches.league_round_number, matches.teams_away_id
ORDER BY matches.league_id,	matches.league_season, matches.league_round_number, max_scorer);

-- Assisters
DROP TABLE IF EXISTS home_max_assisters;
CREATE TEMPORARY TABLE home_max_assisters AS(
SELECT 
	matches.league_id,
	matches.league_season,
	matches.league_round,
	matches.league_round_number,
	matches.teams_home_id,
	MIN(NULLIF(assister_rank_l1, 0)) AS max_assister
	
FROM fdm.tesis_ft_matches AS matches
LEFT JOIN fdm.ft_api_matches_lineups_players AS lineup_players
	ON matches.fixture_id=lineup_players.fixture_id AND matches.teams_home_id=lineup_players.team_id
LEFT JOIN fdm.tesis_lk_top_assisters AS assisters
	ON matches.league_id=assisters.league_id AND matches.league_season=assisters.league_season AND matches.league_round=assisters.league_round
	AND lineup_players.player_id=assisters.player_id
WHERE lineup_players.start_xi=true
GROUP BY matches.league_id,	matches.league_season, matches.league_round, matches.league_round_number, matches.teams_home_id
ORDER BY matches.league_id,	matches.league_season, matches.league_round_number, max_assister);

DROP TABLE IF EXISTS away_max_assisters;
CREATE TEMPORARY TABLE away_max_assisters AS(
SELECT 
	matches.league_id,
	matches.league_season,
	matches.league_round,
	matches.league_round_number,
	matches.teams_away_id,
	MIN(NULLIF(assister_rank_l1, 0)) AS max_assister
	
FROM fdm.tesis_ft_matches AS matches
LEFT JOIN fdm.ft_api_matches_lineups_players AS lineup_players
	ON matches.fixture_id=lineup_players.fixture_id AND matches.teams_away_id=lineup_players.team_id
LEFT JOIN fdm.tesis_lk_top_assisters AS assisters
	ON matches.league_id=assisters.league_id AND matches.league_season=assisters.league_season AND matches.league_round=assisters.league_round
	AND lineup_players.player_id=assisters.player_id
WHERE lineup_players.start_xi=true
GROUP BY matches.league_id,	matches.league_season, matches.league_round, matches.league_round_number, matches.teams_away_id
ORDER BY matches.league_id,	matches.league_season, matches.league_round_number, max_assister);

-- Savers
DROP TABLE IF EXISTS home_max_savers;
CREATE TEMPORARY TABLE home_max_savers AS(
SELECT 
	matches.league_id,
	matches.league_season,
	matches.league_round,
	matches.league_round_number,
	matches.teams_home_id,
	MIN(NULLIF(saver_rank_l1, 0)) AS max_saver
	
FROM fdm.tesis_ft_matches AS matches
LEFT JOIN fdm.ft_api_matches_lineups_players AS lineup_players
	ON matches.fixture_id=lineup_players.fixture_id AND matches.teams_home_id=lineup_players.team_id
LEFT JOIN fdm.tesis_lk_top_savers AS savers
	ON matches.league_id=savers.league_id AND matches.league_season=savers.league_season AND matches.league_round=savers.league_round
	AND lineup_players.player_id=savers.player_id
WHERE lineup_players.start_xi=true
GROUP BY matches.league_id,	matches.league_season, matches.league_round, matches.league_round_number, matches.teams_home_id
ORDER BY matches.league_id,	matches.league_season, matches.league_round_number, max_saver);

DROP TABLE IF EXISTS away_max_savers;
CREATE TEMPORARY TABLE away_max_savers AS(
SELECT 
	matches.league_id,
	matches.league_season,
	matches.league_round,
	matches.league_round_number,
	matches.teams_away_id,
	MIN(NULLIF(saver_rank_l1, 0)) AS max_saver
	
FROM fdm.tesis_ft_matches AS matches
LEFT JOIN fdm.ft_api_matches_lineups_players AS lineup_players
	ON matches.fixture_id=lineup_players.fixture_id AND matches.teams_away_id=lineup_players.team_id
LEFT JOIN fdm.tesis_lk_top_savers AS savers
	ON matches.league_id=savers.league_id AND matches.league_season=savers.league_season AND matches.league_round=savers.league_round
	AND lineup_players.player_id=savers.player_id
WHERE lineup_players.start_xi=true
GROUP BY matches.league_id,	matches.league_season, matches.league_round, matches.league_round_number, matches.teams_away_id
ORDER BY matches.league_id,	matches.league_season, matches.league_round_number, max_saver);

-- Final ABT
DROP TABLE IF EXISTS fdm.tesis_abt;
CREATE TABLE fdm.tesis_abt AS (
SELECT
	abt.*,
-- Top Players	
	COALESCE(home_max_scorers.max_scorer, 0) AS home_max_scorer,
	COALESCE(away_max_scorers.max_scorer, 0) AS away_max_scorer,
	COALESCE(home_max_assisters.max_assister, 0) AS home_max_assister,
	COALESCE(away_max_assisters.max_assister, 0) AS away_max_assister,
	COALESCE(home_max_savers.max_saver, 0) AS home_max_saver,
	COALESCE(away_max_savers.max_saver, 0) AS away_max_saver,
-- Motivation
	CASE WHEN (league_progress>0.6 AND rank_points_top5-home_rank<=(total_rounds-abt.league_round_number)*3) THEN 1 ELSE 0 END AS home_motivation_cup,
	CASE WHEN (league_progress>0.6 AND rank_points_leader-home_rank<=(total_rounds-abt.league_round_number)*3) THEN 1 ELSE 0 END AS home_motivation_leader,
	CASE WHEN (league_progress>0.6 AND home_rank > rank_last/2 AND home_rank-rank_points_last<=(total_rounds-abt.league_round_number)*3) THEN 1 ELSE 0 END AS home_motivation_stay,
	
	CASE WHEN (league_progress>0.6 AND rank_points_top5-away_rank<=(total_rounds-abt.league_round_number)*3) THEN 1 ELSE 0 END AS away_motivation_cup,
	CASE WHEN (league_progress>0.6 AND rank_points_leader-away_rank<=(total_rounds-abt.league_round_number)*3) THEN 1 ELSE 0 END AS away_motivation_leader,
	CASE WHEN (league_progress>0.6 AND away_rank > rank_last/2 AND away_rank-rank_points_last<=(total_rounds-abt.league_round_number)*3) THEN 1 ELSE 0 END AS away_motivation_stay
	
FROM fdm.tesis_abt_0 AS abt
-- Scorers
LEFT JOIN home_max_scorers
	ON abt.league_id=home_max_scorers.league_id AND abt.league_season=home_max_scorers.league_season AND abt.league_round=home_max_scorers.league_round
	AND abt.teams_home_id=home_max_scorers.teams_home_id
LEFT JOIN away_max_scorers
	ON abt.league_id=away_max_scorers.league_id AND abt.league_season=away_max_scorers.league_season AND abt.league_round=away_max_scorers.league_round
	AND abt.teams_away_id=away_max_scorers.teams_away_id
-- Assisters
LEFT JOIN home_max_assisters
	ON abt.league_id=home_max_assisters.league_id AND abt.league_season=home_max_assisters.league_season AND abt.league_round=home_max_assisters.league_round
	AND abt.teams_home_id=home_max_assisters.teams_home_id
LEFT JOIN away_max_assisters
	ON abt.league_id=away_max_assisters.league_id AND abt.league_season=away_max_assisters.league_season AND abt.league_round=away_max_assisters.league_round
	AND abt.teams_away_id=away_max_assisters.teams_away_id
-- Savers
LEFT JOIN home_max_savers
	ON abt.league_id=home_max_savers.league_id AND abt.league_season=home_max_savers.league_season AND abt.league_round=home_max_savers.league_round
	AND abt.teams_home_id=home_max_savers.teams_home_id
LEFT JOIN away_max_savers
	ON abt.league_id=away_max_savers.league_id AND abt.league_season=away_max_savers.league_season AND abt.league_round=away_max_savers.league_round
	AND abt.teams_away_id=away_max_savers.teams_away_id);

DROP TABLE IF EXISTS fdm.tesis_abt_0;

