-- =======================================================================================================
-- Author:    Fabricio Pretto
-- Create date:  23/11/2021
-- Description:  ABT creation of player performance by season
-- =======================================================================================================

-- Player Most Frequent Team by Season
DROP TABLE IF EXISTS fdm.dash_lk_player_team;
CREATE TABLE fdm.dash_lk_player_team AS (
WITH 
grouped_players_team AS(
	SELECT 
		player_id,
		league_season,
		stats_players.team_id,
		team_name,
		team_country,
		SUM(stats_players.player_minutes) as player_minutes

	FROM fdm.ft_api_matches_stats_players AS stats_players
	LEFT JOIN fdm.ft_api_matches AS matches
		ON stats_players.fixture_id=matches.fixture_id
	LEFT JOIN fdm.lk_api_leagues AS leagues
		ON matches.league_id=leagues.league_id
	LEFT JOIN fdm.lk_api_teams AS teams
		ON stats_players.team_id=teams.team_id
	GROUP BY player_id, league_season, stats_players.team_id, team_name, team_country
	ORDER BY player_id, league_season, player_minutes DESC
),
grouped_players_team2 AS(
SELECT
	*,
	ROW_NUMBER() OVER(PARTITION BY player_id, league_season) AS row_n
FROM grouped_players_team)
SELECT * FROM grouped_players_team2
WHERE row_n=1);

-- Player Most Frequent Number
DROP TABLE IF EXISTS fdm.dash_lk_player_number_all_seasons;
CREATE TABLE fdm.dash_lk_player_number_all_seasons AS (
WITH 
grouped_players_number AS(
	SELECT 
		player_id,
		league_season,
		player_number,
		SUM(stats_players.player_minutes) as player_minutes

	FROM fdm.ft_api_matches_stats_players AS stats_players
	LEFT JOIN fdm.ft_api_matches AS matches
		ON stats_players.fixture_id=matches.fixture_id
	GROUP BY player_id, league_season, player_number
	ORDER BY player_id, league_season, player_minutes DESC
),
grouped_players_number2 AS(
SELECT
	*,
	ROW_NUMBER() OVER(PARTITION BY player_id, league_season) AS row_n
FROM grouped_players_number)
SELECT * FROM grouped_players_number2
WHERE row_n=1);

-- Player Most Frequent Position
DROP TABLE IF EXISTS fdm.dash_lk_player_position_all_seasons;
CREATE TABLE fdm.dash_lk_player_position_all_seasons AS (
WITH
grouped_players_position AS(
	SELECT 
		player_id,
		league_season,
		player_position,
		SUM(stats_players.player_minutes) as player_minutes

	FROM fdm.ft_api_matches_stats_players AS stats_players
	LEFT JOIN fdm.ft_api_matches AS matches
		ON stats_players.fixture_id=matches.fixture_id
	GROUP BY player_id, league_season, player_position
	ORDER BY player_id, league_season, player_minutes DESC
),
grouped_players_position2 AS(
SELECT
	*,
	ROW_NUMBER() OVER(PARTITION BY player_id, league_season) AS row_n
FROM grouped_players_position)
SELECT * FROM grouped_players_position2
WHERE row_n=1);

-- Shots on Goal Opponent Team
DROP TABLE IF EXISTS fdm.dash_lk_team_opp_stats;
CREATE TABLE fdm.dash_lk_team_opp_stats AS (
SELECT 
	matches.fixture_id,
	matches.teams_home_id AS team_id,
	stats_teams_home.shots_on_goal AS shots_on_goal_opp
FROM fdm.ft_api_matches AS matches
LEFT JOIN fdm.ft_api_matches_stats_teams AS stats_teams_home
	ON matches.fixture_id=stats_teams_home.fixture_id AND matches.teams_away_id=stats_teams_home.teams_id
UNION ALL
SELECT 
	matches.fixture_id,
	matches.teams_away_id AS team_id,
	stats_teams_away.shots_on_goal AS shots_on_goal_opp
FROM fdm.ft_api_matches AS matches
LEFT JOIN fdm.ft_api_matches_stats_teams AS stats_teams_away
	ON matches.fixture_id=stats_teams_away.fixture_id AND matches.teams_home_id=stats_teams_away.teams_id);

-- ABT
DROP TABLE IF EXISTS fdm.dash_ft_abt_season_players_train;
CREATE TABLE fdm.dash_ft_abt_season_players_train AS (
SELECT
	matches.league_season,
	stats_players.player_id,
	player_names.player_name,
	player_positions.player_position AS player_preferred_position,
	player_numbers.player_number AS player_preferred_number,
	player_team.team_id,
	player_team.team_name,
	player_team.team_country,
	(AVG(standings.standings_points)-AVG(standings.standings_min_pts_season))/(AVG(standings.standings_max_pts_season)-AVG(standings.standings_min_pts_season)) AS avg_team_position,
	CASE WHEN AVG(standings.standings_avg_points)=0 THEN 0 ELSE AVG(standings.standings_stddev_points)/AVG(standings.standings_avg_points) END AS avg_league_cov,
	SUM(stats_players.player_minutes) AS player_minutes,
	SUM(player_rating*stats_players.player_minutes)/NULLIF(SUM(CASE WHEN player_rating<=0 THEN 0 ELSE stats_players.player_minutes END), 0) wavg_player_rating,
	SUM(stats_players.offsides) AS offsides,
	SUM(stats_players.shots_total) AS shots_total,
	SUM(stats_players.shots_on) AS shots_on_goal,
	SUM(stats_players.goals_total) AS goals_total,
	--SUM(stats_players.goals_conceded) AS goals_conceded,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.goals_conceded ELSE stats_players.goals_conceded*0.5/(1-stats_teams.ball_possession) END) AS goals_conceded_padj,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN opp_stats.shots_on_goal_opp ELSE opp_stats.shots_on_goal_opp*0.5/(1-stats_teams.ball_possession) END) AS shots_on_goal_opp_padj,
	SUM(stats_players.goals_assists) AS goals_assists,
	--SUM(stats_players.goals_saves) AS goals_saves,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.goals_saves ELSE stats_players.goals_saves*0.5/(1-stats_teams.ball_possession) END) AS goals_saves_padj,
	SUM(stats_players.passes_total) AS passes_total,
	SUM(stats_players.passes_key) AS passes_key,
	SUM(stats_players.passes_total*passes_accuracy) AS passes_completed,
	--SUM(stats_players.tackles_total) AS tackles_total,
	--SUM(stats_players.tackles_blocks) AS tackles_blocks,
	--SUM(stats_players.tackles_interceptions) AS tackles_interceptions,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.tackles_total ELSE stats_players.tackles_total*0.5/(1-stats_teams.ball_possession) END) AS tackles_total_padj,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.tackles_blocks ELSE stats_players.tackles_blocks*0.5/(1-stats_teams.ball_possession) END) AS tackles_blocks_padj,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.tackles_interceptions ELSE stats_players.tackles_interceptions*0.5/(1-stats_teams.ball_possession) END) AS tackles_interceptions_padj,
	--SUM(stats_players.duels_total) AS duels_total,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.duels_total ELSE stats_players.duels_total*0.5/(1-stats_teams.ball_possession) END) AS duels_total_padj,
	--SUM(stats_players.duels_won) AS duels_won,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.duels_won ELSE stats_players.duels_won*0.5/(1-stats_teams.ball_possession) END) AS duels_won_padj,
	SUM(stats_players.dribbles_attemps) AS dribbles_attemps,
	SUM(stats_players.dribbles_success) AS dribbles_success,
	--SUM(stats_players.dribbles_past) AS dribbles_past,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.dribbles_past ELSE stats_players.dribbles_past*0.5/(1-stats_teams.ball_possession) END) AS dribbles_past_padj,
	SUM(stats_players.fouls_drawn) AS fouls_drawn,
	--SUM(stats_players.fouls_committed) AS fouls_committed,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.fouls_committed ELSE stats_players.fouls_committed*0.5/(1-stats_teams.ball_possession) END) AS fouls_committed_padj,
	SUM(stats_players.cards_yellow) AS cards_yellow,
	SUM(stats_players.cards_red) AS cards_red,
	SUM(stats_players.penalty_won) AS penalty_won,
	--SUM(stats_players.penalty_committed) AS penalty_committed,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.penalty_committed ELSE stats_players.penalty_committed*0.5/(1-stats_teams.ball_possession) END) AS penalty_committed_padj,
	SUM(stats_players.penalty_scored) AS penalty_scored,
	SUM(stats_players.penalty_missed) AS penalty_missed,
	SUM(penalty_saved) AS penalty_saved
	
FROM fdm.ft_api_matches_stats_players AS stats_players
LEFT JOIN fdm.ft_api_matches AS matches
	ON stats_players.fixture_id=matches.fixture_id
LEFT JOIN fdm.fp_lk_player_names as player_names
	ON stats_players.player_id=player_names.player_id
LEFT JOIN fdm.dash_lk_player_team AS player_team
	ON stats_players.player_id=player_team.player_id AND matches.league_season=player_team.league_season
LEFT JOIN fdm.dash_lk_player_position_all_seasons AS player_positions
	ON stats_players.player_id=player_positions.player_id AND matches.league_season=player_positions.league_season
LEFT JOIN fdm.dash_lk_player_number_all_seasons AS player_numbers
	ON stats_players.player_id=player_numbers.player_id AND matches.league_season=player_numbers.league_season
LEFT JOIN fdm.ft_api_matches_stats_teams AS stats_teams
	ON stats_players.fixture_id=stats_teams.fixture_id AND stats_players.team_id=stats_teams.teams_id
LEFT JOIN fdm.fp_lk_standings AS standings
	ON player_team.team_id=standings.team_id AND player_team.league_season=standings.league_season
LEFT JOIN fdm.dash_lk_team_opp_stats AS opp_stats
	ON stats_players.fixture_id=opp_stats.fixture_id AND stats_players.team_id=opp_stats.team_id
GROUP BY matches.league_season, stats_players.player_id, player_names.player_name, player_positions.player_position, 
	player_numbers.player_number, player_team.team_id, player_team.team_name, player_team.team_country
);

DROP TABLE fdm.dash_lk_player_team;
DROP TABLE fdm.dash_lk_player_number_all_seasons;
DROP TABLE fdm.dash_lk_player_position_all_seasons;
DROP TABLE fdm.dash_lk_team_opp_stats;

SELECT * FROM fdm.dash_ft_abt_season_players_train 
WHERE player_preferred_position='G' LIMIT 100
