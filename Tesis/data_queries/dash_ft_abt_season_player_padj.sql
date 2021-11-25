-- Player Majoritarian Team by Season
DROP TABLE IF EXISTS fdm.dash_lk_player_team;
CREATE TABLE fdm.dash_lk_player_team AS (
WITH 
grouped_players_team AS(
	SELECT 
		player_id,
		league_season,
		team_id,
		SUM(stats_players.player_minutes) as player_minutes

	FROM fdm.ft_api_matches_stats_players AS stats_players
	LEFT JOIN fdm.ft_api_matches AS matches
		ON stats_players.fixture_id=matches.fixture_id
	LEFT JOIN fdm.lk_api_leagues AS leagues
		ON matches.league_id=leagues.league_id
	GROUP BY player_id, league_season, team_id
	ORDER BY player_id, league_season, player_minutes DESC
),
grouped_players_team2 AS(
SELECT
	*,
	ROW_NUMBER() OVER(PARTITION BY player_id, league_season) AS row_n
FROM grouped_players_team)
SELECT * FROM grouped_players_team2
WHERE row_n=1);

-- Player Preferred Number
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

-- Player Preferred Position
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

-- ABT
DROP TABLE IF EXISTS fdm.dash_ft_abt_season_players_train_padj;
CREATE TABLE fdm.dash_ft_abt_season_players_train_padj AS (
SELECT
	matches.league_season,
	stats_players.player_id,
	player_names.player_name,
	player_positions.player_position AS player_preferred_position,
	player_numbers.player_number AS player_preferred_number,
	player_team.team_id,
	(AVG(standings.standings_points)-AVG(standings.standings_min_pts_season))/(AVG(standings.standings_max_pts_season)-AVG(standings.standings_min_pts_season)) AS avg_team_position,
	CASE WHEN AVG(standings.standings_avg_points)=0 THEN 0 ELSE AVG(standings.standings_stddev_points)/AVG(standings.standings_avg_points) END AS avg_league_cov,
	SUM(stats_players.player_minutes) AS player_minutes,
	SUM(player_rating*stats_players.player_minutes)/NULLIF(SUM(CASE WHEN player_rating<=0 THEN 0 ELSE stats_players.player_minutes END), 0) wavg_player_rating,
	SUM(stats_players.offsides) AS offsides,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.offsides ELSE stats_players.offsides*0.5/stats_teams.ball_possession END) AS offsides_padj,
	SUM(stats_players.shots_total) AS shots_total,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.shots_total ELSE stats_players.shots_total*0.5/stats_teams.ball_possession END) AS shots_total_padj,
	SUM(stats_players.shots_on) AS shots_on_goal,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.shots_on ELSE stats_players.shots_on*0.5/stats_teams.ball_possession END) AS shots_on_goal_padj,
	SUM(stats_players.goals_total) AS goals_total,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.goals_total ELSE stats_players.goals_total*0.5/stats_teams.ball_possession END) AS goals_total_padj,
	SUM(stats_players.goals_conceded) AS goals_conceded,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.goals_conceded ELSE stats_players.goals_conceded*0.5/stats_teams.ball_possession END) AS goals_conceded_padj,
	SUM(stats_players.goals_assists) AS goals_assists,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.goals_assists ELSE stats_players.goals_assists*0.5/stats_teams.ball_possession END) AS goals_assists_padj,
	SUM(stats_players.goals_saves) AS goals_saves,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.goals_saves ELSE stats_players.goals_saves*0.5/stats_teams.ball_possession END) AS goals_saves_padj,
	SUM(stats_players.passes_total) AS passes_total,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.passes_total ELSE stats_players.passes_total*0.5/stats_teams.ball_possession END) AS passes_total_padj,
	SUM(stats_players.passes_key) AS passes_key,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.passes_key ELSE stats_players.passes_key*0.5/stats_teams.ball_possession END) AS passes_key_padj,
	SUM(stats_players.passes_total*passes_accuracy) AS passes_completed,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.passes_total*passes_accuracy ELSE stats_players.passes_total*passes_accuracy*0.5/stats_teams.ball_possession END) AS passes_completed_padj,
	SUM(stats_players.tackles_total) AS tackles_total,
	SUM(stats_players.tackles_blocks) AS tackles_blocks,
	SUM(stats_players.tackles_interceptions) AS tackles_interceptions,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.tackles_total ELSE stats_players.tackles_total*0.5/stats_teams.ball_possession END) AS tackles_total_padj,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.tackles_blocks ELSE stats_players.tackles_blocks*0.5/stats_teams.ball_possession END) AS tackles_blocks_padj,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.tackles_interceptions ELSE stats_players.tackles_interceptions*0.5/stats_teams.ball_possession END) AS tackles_interceptions_padj,
	SUM(stats_players.duels_total) AS duels_total,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.duels_total ELSE stats_players.duels_total*0.5/stats_teams.ball_possession END) AS duels_total_padj,
	SUM(stats_players.duels_won) AS duels_won,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.duels_won ELSE stats_players.duels_won*0.5/stats_teams.ball_possession END) AS duels_won_padj,
	SUM(stats_players.dribbles_attemps) AS dribbles_attemps,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.dribbles_attemps ELSE stats_players.dribbles_attemps*0.5/stats_teams.ball_possession END) AS dribbles_attemps_padj,
	SUM(stats_players.dribbles_success) AS dribbles_success,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.dribbles_success ELSE stats_players.dribbles_success*0.5/stats_teams.ball_possession END) AS dribbles_success_padj,
	SUM(stats_players.dribbles_past) AS dribbles_past,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.dribbles_past ELSE stats_players.dribbles_past*0.5/stats_teams.ball_possession END) AS dribbles_past_padj,
	SUM(stats_players.fouls_drawn) AS fouls_drawn,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.fouls_drawn ELSE stats_players.fouls_drawn*0.5/stats_teams.ball_possession END) AS fouls_drawn_padj,
	SUM(stats_players.fouls_committed) AS fouls_committed,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.fouls_committed ELSE stats_players.fouls_committed*0.5/stats_teams.ball_possession END) AS fouls_committed_padj,
	SUM(stats_players.cards_yellow) AS cards_yellow,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.cards_yellow ELSE stats_players.cards_yellow*0.5/stats_teams.ball_possession END) AS cards_yellow_padj,
	SUM(stats_players.cards_red) AS cards_red,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.cards_red ELSE stats_players.cards_red*0.5/stats_teams.ball_possession END) AS cards_red_padj,
	SUM(stats_players.penalty_won) AS penalty_won,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.penalty_won ELSE stats_players.penalty_won*0.5/stats_teams.ball_possession END) AS penalty_won_padj,
	SUM(stats_players.penalty_committed) AS penalty_committed,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.penalty_committed ELSE stats_players.penalty_committed*0.5/stats_teams.ball_possession END) AS penalty_committed_padj,
	SUM(stats_players.penalty_scored) AS penalty_scored,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.penalty_scored ELSE stats_players.penalty_scored*0.5/stats_teams.ball_possession END) AS penalty_scored_padj,
	SUM(stats_players.penalty_missed) AS penalty_missed,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.penalty_missed ELSE stats_players.penalty_missed*0.5/stats_teams.ball_possession END) AS penalty_missed_padj,
	SUM(penalty_saved) AS penalty_saved,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.penalty_saved ELSE stats_players.penalty_saved*0.5/stats_teams.ball_possession END) AS penalty_saved_padj
	
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
GROUP BY matches.league_season, stats_players.player_id, player_names.player_name, player_positions.player_position, 
	player_numbers.player_number, player_team.team_id
);
