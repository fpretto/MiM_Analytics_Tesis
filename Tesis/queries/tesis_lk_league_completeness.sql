/*
select * from fdm.lk_api_leagues l
left join fdm.lk_api_countries co
on l.country_code=co.country_code_2
where continent_code='SA'
order by country_code, league_id

-- Leagues and Seasons
select * from fdm.lk_api_leagues
where league_id=128

select * from fdm.lk_api_seasons
where league_id=722
order by league_id, season


SELECT * FROM fdm.fp_leagues_completeness
WHERE country_name='Mexico'
ORDER BY country_name, league_id, league_season
*/

-- Check all
DROP TABLE fdm.tesis_lk_leagues_completeness;
CREATE TABLE fdm.tesis_lk_leagues_completeness AS (
select 

	matches.country_name,
	matches.league_id, 
	matches.league_name, 
	matches.league_type, 
	matches.league_season,
	matches.matches,
	matches.teams,
	events.events,
	lineups_teams.lineups_teams,
	lineups_players.lineups_players,
	preds.predictions,
	stats_teams.stats_teams,
	stats_players.stats_players,
	stands.standings_teams,
	ROUND(events.events/CAST(matches.matches AS float)*100) AS events_pct,
	ROUND(lineups_teams.lineups_teams/CAST(matches.matches AS float)*100) AS lineup_teams_pct,
	ROUND(lineups_players.lineups_players/CAST(matches.matches AS float)*100) AS lineup_players_pct,
	ROUND(preds.predictions/CAST(matches.matches AS float)*100) AS predictions_pct,
	ROUND(stats_teams.stats_teams/CAST(matches.matches AS float)*100) AS stats_teams_pct,
	ROUND(stats_players.stats_players/CAST(matches.matches AS float)*100) AS stats_players_pct,
	ROUND(stands.standings_teams/CAST(matches.matches AS float)*100) AS standings_pct
	
from
-- Matches
(select country_name, fixtures.league_id, league_name, league_type, league_season, count(distinct fixture_id) as matches, count(distinct teams_home_id) as teams from fdm.ft_api_matches as fixtures
 left join fdm.lk_api_leagues as leagues
 on fixtures.league_id=leagues.league_id
 --where league_id=128
group by country_name, fixtures.league_id, league_name, league_type,league_season
order by fixtures.league_id, league_season) as matches
left join
-- Matches Events
(select fix.league_id, fix.league_season, count(distinct ev.fixture_id) as events
from fdm.ft_api_matches_events as ev
left join fdm.ft_api_matches as fix
on ev.fixture_id=fix.fixture_id
group by fix.league_id, fix.league_season) as events
on matches.league_id=events.league_id and matches.league_season=events.league_season
left join
-- Matches Lineups
(select fix.league_id, fix.league_season, count(distinct lin.fixture_id) as lineups_teams
from fdm.ft_api_matches_lineups_players as lin
left join fdm.ft_api_matches as fix
on lin.fixture_id=fix.fixture_id
group by fix.league_id, fix.league_season) as lineups_teams
on matches.league_id=lineups_teams.league_id and matches.league_season=lineups_teams.league_season
left join
(select fix.league_id, fix.league_season, count(distinct lin.fixture_id) as lineups_players
from fdm.ft_api_matches_lineups_teams as lin
left join fdm.ft_api_matches as fix
on lin.fixture_id=fix.fixture_id
group by fix.league_id, fix.league_season) as lineups_players
on matches.league_id=lineups_players.league_id and matches.league_season=lineups_players.league_season
left join
-- Predictions
(select fix.league_id, fix.league_season, count(distinct pred.fixture_id) as predictions
from fdm.ft_api_matches_predictions as pred
left join fdm.ft_api_matches as fix
on pred.fixture_id=fix.fixture_id
group by fix.league_id, fix.league_season) as preds
on matches.league_id=preds.league_id and matches.league_season=preds.league_season
left join
-- Stats Players
(select fix.league_id, fix.league_season, count(distinct stats.fixture_id) as stats_players
from fdm.ft_api_matches_stats_players as stats
left join fdm.ft_api_matches as fix
on stats.fixture_id=fix.fixture_id
group by fix.league_id, fix.league_season) as stats_players
on matches.league_id=stats_players.league_id and matches.league_season=stats_players.league_season
left join
-- Stats Teams
(select fix.league_id, fix.league_season, count(distinct stats.fixture_id) as stats_teams
from fdm.ft_api_matches_stats_teams as stats
left join fdm.ft_api_matches as fix
on stats.fixture_id=fix.fixture_id
group by fix.league_id, fix.league_season) as stats_teams
on matches.league_id=stats_teams.league_id and matches.league_season=stats_teams.league_season
left join
-- Standings
(select league_id, league_season, count(*) as standings_teams from fdm.ft_api_standings
where league_id=128
group by league_id, league_season) as stands
on matches.league_id=stands.league_id and matches.league_season=stands.league_season
	)