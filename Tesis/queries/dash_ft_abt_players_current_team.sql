-- Player Preferred Team
DROP TABLE IF EXISTS fdm.dash_lk_player_team;
CREATE TABLE fdm.dash_lk_player_team AS (
WITH 
grouped_players_team AS(
	SELECT 
		player_id,
		team_id,
		SUM(stats_players.player_minutes) as player_minutes

	FROM fdm.ft_api_matches_stats_players AS stats_players
	LEFT JOIN fdm.ft_api_matches AS matches
		ON stats_players.fixture_id=matches.fixture_id
	LEFT JOIN fdm.lk_api_leagues AS leagues
		ON matches.league_id=leagues.league_id
	WHERE matches.league_season=2021
	GROUP BY player_id, team_id
	ORDER BY player_id, player_minutes DESC
),
grouped_players_team2 AS(
SELECT
	*,
	ROW_NUMBER() OVER(PARTITION BY player_id) AS row_n
FROM grouped_players_team)
SELECT * FROM grouped_players_team2
WHERE row_n=1);

-- Player Preferred Number
DROP TABLE IF EXISTS fdm.dash_lk_player_number;
CREATE TABLE fdm.dash_lk_player_number AS (
WITH 
grouped_players_number AS(
	SELECT 
		player_id,
		team_id,
		player_number,
		SUM(stats_players.player_minutes) as player_minutes

	FROM fdm.ft_api_matches_stats_players AS stats_players
	LEFT JOIN fdm.ft_api_matches AS matches
		ON stats_players.fixture_id=matches.fixture_id
	LEFT JOIN fdm.lk_api_leagues AS leagues
		ON matches.league_id=leagues.league_id
	WHERE matches.league_season=2021
	GROUP BY player_id, team_id, player_number
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
DROP TABLE IF EXISTS fdm.dash_lk_player_position;
CREATE TABLE fdm.dash_lk_player_position AS (
WITH
grouped_players_position AS(
	SELECT 
		player_id,
		team_id,
		player_position,
		SUM(stats_players.player_minutes) as player_minutes

	FROM fdm.ft_api_matches_stats_players AS stats_players
	LEFT JOIN fdm.ft_api_matches AS matches
		ON stats_players.fixture_id=matches.fixture_id
	LEFT JOIN fdm.lk_api_leagues AS leagues
		ON matches.league_id=leagues.league_id
	WHERE matches.league_season=2021
	GROUP BY player_id, team_id, player_position
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
DROP TABLE IF EXISTS fdm.dash_ft_abt_player_current_team;
CREATE TABLE fdm.dash_ft_abt_player_current_team AS (
SELECT
	teams.team_country_code,
	teams.team_country,
	matches.league_id,
	leagues.league_name,
	leagues.league_type,
	matches.league_season,
	stats_players.player_id,
	player_names.player_name,
	player_positions.player_position AS player_preferred_position,
	player_numbers.player_number AS player_preferred_number,
	player_team.team_id,
	teams.team_name,
	SUM(stats_players.player_minutes) AS player_minutes,
	SUM(player_rating*stats_players.player_minutes)/NULLIF(SUM(CASE WHEN player_rating<1 THEN 0 ELSE stats_players.player_minutes END), 0) wavg_player_rating,
	SUM(stats_players.goals_total) AS goals_total,
	SUM(stats_players.goals_assists) AS goals_assists,
	SUM(stats_players.goals_saves) AS goals_saves	

FROM fdm.ft_api_matches_stats_players AS stats_players
INNER JOIN fdm.dash_lk_player_team AS player_team
	ON stats_players.player_id=player_team.player_id AND  stats_players.team_id=player_team.team_id
LEFT JOIN fdm.fp_lk_player_names as player_names
	ON stats_players.player_id=player_names.player_id
LEFT JOIN fdm.ft_api_matches AS matches
	ON stats_players.fixture_id=matches.fixture_id
LEFT JOIN fdm.dash_lk_player_position AS player_positions
	ON stats_players.player_id=player_positions.player_id AND player_team.team_id=player_positions.team_id
LEFT JOIN fdm.dash_lk_player_number AS player_numbers
	ON stats_players.player_id=player_numbers.player_id AND player_team.team_id=player_numbers.team_id
LEFT JOIN fdm.lk_api_teams AS teams
	ON player_team.team_id=teams.team_id
LEFT JOIN fdm.lk_api_leagues AS leagues
	ON matches.league_id=leagues.league_id
INNER JOIN fdm.dash_lk_leagues AS dash_leagues
	ON matches.league_id=dash_leagues.league_id AND matches.league_season=dash_leagues.league_season
WHERE matches.league_season=2021
GROUP BY teams.team_country_code, teams.team_country, matches.league_id, leagues.league_name, leagues.league_type, matches.league_season, 
		stats_players.player_id, player_names.player_name, player_positions.player_position, player_numbers.player_number,
		player_team.team_id, teams.team_name	
);

/*
SELECT count(*) FROM fdm.ft_api_matches_stats_teams
where ball_possesion <= 0

SELECT players.*,
	tackles_total,
	CASE WHEN teams.ball_possesion=0 THEN tackles_total ELSE tackles_total*0.5/teams.ball_possesion END AS tackles_total_padj,
	tackles_blocks,
	CASE WHEN teams.ball_possesion=0 THEN tackles_blocks ELSE tackles_blocks*0.5/teams.ball_possesion END AS tackles_blocks_padj,
	tackles_interceptions,
	CASE WHEN teams.ball_possesion=0 THEN tackles_interceptions ELSE tackles_interceptions*0.5/teams.ball_possesion END AS tackles_interceptions_padj,
	teams.ball_possesion FROM fdm.ft_api_matches_stats_players AS players
LEFT JOIN fdm.ft_api_matches_stats_teams AS teams
	ON players.fixture_id=teams.fixture_id AND players.team_id=teams.team_id
*/