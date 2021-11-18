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
	ORDER BY player_id, player_minutes DESC
),
grouped_players_number2 AS(
SELECT
	*,
	ROW_NUMBER() OVER(PARTITION BY player_id) AS row_n
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
	ORDER BY player_id, player_minutes DESC
),
grouped_players_position2 AS(
SELECT
	*,
	ROW_NUMBER() OVER(PARTITION BY player_id) AS row_n
FROM grouped_players_position)
SELECT * FROM grouped_players_position2
WHERE row_n=1);

-- ABT
DROP TABLE IF EXISTS fdm.dash_ft_abt_season_players_train;
CREATE TABLE fdm.dash_ft_abt_season_players_train AS (
SELECT
	matches.league_season,
	stats_players.player_id,
	player_names.player_name,
	player_positions.player_position AS player_preferred_position,
	player_numbers.player_number AS player_preferred_number,
	SUM(stats_players.player_minutes) AS player_minutes,
	SUM(player_rating*stats_players.player_minutes)/NULLIF(SUM(CASE WHEN player_rating<=0 THEN 0 ELSE stats_players.player_minutes END), 0) wavg_player_rating,
	SUM(stats_players.offsides) AS offsides,
	SUM(stats_players.shots_total) AS shots_total,
	SUM(stats_players.shots_on) AS shots_on_goal,
	SUM(stats_players.goals_total) AS goals_total,
	SUM(stats_players.goals_conceded) AS goals_conceded,
	SUM(stats_players.goals_assists) AS goals_assists,
	SUM(stats_players.goals_saves) AS goals_saves,
	SUM(stats_players.passes_total) AS passes_total,
	SUM(stats_players.passes_key) AS passes_key,
	SUM(stats_players.passes_total*passes_accuracy) AS passes_completed,
	SUM(stats_players.tackles_total) AS tackles_total,
	SUM(stats_players.tackles_blocks) AS tackles_blocks,
	SUM(stats_players.tackles_interceptions) AS tackles_interceptions,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.tackles_total ELSE stats_players.tackles_total*0.5/stats_teams.ball_possession END) AS tackles_total_padj,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.tackles_blocks ELSE stats_players.tackles_blocks*0.5/stats_teams.ball_possession END) AS tackles_blocks_padj,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.tackles_interceptions ELSE stats_players.tackles_interceptions*0.5/stats_teams.ball_possession END) AS tackles_interceptions_padj,
	SUM(stats_players.duels_total) AS duels_total,
	SUM(stats_players.duels_won) AS duels_won,
	SUM(stats_players.dribbles_attemps) AS dribbles_attemps,
	SUM(stats_players.dribbles_success) AS dribbles_success,
	SUM(stats_players.dribbles_past) AS dribbles_past,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.dribbles_past ELSE stats_players.dribbles_past*0.5/stats_teams.ball_possession END) AS dribbles_past_padj,
	SUM(stats_players.fouls_drawn) AS fouls_drawn,
	SUM(stats_players.fouls_committed) AS fouls_committed,
	SUM(CASE WHEN stats_teams.ball_possession=0 THEN stats_players.fouls_committed ELSE stats_players.fouls_committed*0.5/stats_teams.ball_possession END) AS fouls_committed_padj,
	SUM(stats_players.cards_yellow) AS cards_yellow,
	SUM(stats_players.cards_red) AS cards_red,
	SUM(stats_players.penalty_won) AS penalty_won,
	SUM(stats_players.penalty_committed) AS penalty_committed,
	SUM(stats_players.penalty_scored) AS penalty_scored,
	SUM(stats_players.penalty_missed) AS penalty_missed,
	SUM(penalty_saved) AS penalty_saved
	
FROM fdm.ft_api_matches_stats_players AS stats_players
LEFT JOIN fdm.ft_api_matches AS matches
	ON stats_players.fixture_id=matches.fixture_id
LEFT JOIN fdm.fp_lk_player_names as player_names
	ON stats_players.player_id=player_names.player_id
LEFT JOIN fdm.dash_lk_player_position_all_seasons AS player_positions
	ON stats_players.player_id=player_positions.player_id AND matches.league_season=player_positions.league_season
LEFT JOIN fdm.dash_lk_player_number_all_seasons AS player_numbers
	ON stats_players.player_id=player_numbers.player_id AND matches.league_season=player_numbers.league_season
LEFT JOIN fdm.ft_api_matches_stats_teams AS stats_teams
	ON stats_players.fixture_id=stats_teams.fixture_id AND stats_players.team_id=stats_teams.teams_id
GROUP BY matches.league_season, stats_players.player_id, player_names.player_name, player_positions.player_position, player_numbers.player_number
);
