-- Base table (matches)
-- select * from pg_timezone_names;
DROP TABLE IF EXISTS fdm.tesis_ft_matches;
CREATE TABLE fdm.tesis_ft_matches AS (
SELECT 
	rounds.country_name,
	rounds.country_code,
	countries.continent_code,
	continents.continent_name,
	matches.league_id,
	rounds.league_name,
	rounds.league_type,
	matches.league_season,
	matches.league_round,
	rounds.league_round_number,
	matches.fixture_id,
	fixture_referee,
	fixture_date,
	CASE WHEN (rounds.country_code='BR' OR rounds.country_code='MX') AND (matches.fixture_venue_id>0 AND tzs_venue.pg_timezone IS NOT NULL) 
		THEN to_timestamp(fixture_date, 'YYYY-MM-DD"T"HH24:MI:SS') AT time zone tzs_venue.pg_timezone 
		ELSE to_timestamp(fixture_date, 'YYYY-MM-DD"T"HH24:MI:SS') AT time zone tzs_country.pg_timezone	END AS date_timestamp,
	CASE WHEN (rounds.country_code='BR' OR rounds.country_code='MX') AND (matches.fixture_venue_id>0 AND tzs_venue.pg_timezone IS NOT NULL) 
		THEN DATE(to_timestamp(fixture_date, 'YYYY-MM-DD"T"HH24:MI:SS') AT time zone tzs_venue.pg_timezone )
		ELSE DATE(to_timestamp(fixture_date, 'YYYY-MM-DD"T"HH24:MI:SS') AT time zone tzs_country.pg_timezone) END AS date_match,
	CASE WHEN (rounds.country_code='BR' OR rounds.country_code='MX') AND (matches.fixture_venue_id>0 AND tzs_venue.pg_timezone IS NOT NULL) 
		THEN LEFT(RIGHT(TEXT(to_timestamp(fixture_date, 'YYYY-MM-DD"T"HH24:MI:SS') AT time zone tzs_venue.pg_timezone), 8), 5) 
		ELSE LEFT(RIGHT(TEXT(to_timestamp(fixture_date, 'YYYY-MM-DD"T"HH24:MI:SS') AT time zone tzs_country.pg_timezone), 8), 5) END AS time_match,
	matches.fixture_venue_id,
	teams_home_id,
	teams_home_name,
	teams_away_id,
	teams_away_name,
	CASE 
		WHEN teams_home_winner=1 THEN 'Home'
		WHEN teams_home_winner=-1 THEN 'Away'
	ELSE 'Draw' END as target

FROM fdm.ft_api_matches AS matches
LEFT JOIN fdm.lk_api_venues_tz as tzs_venue
	ON matches.fixture_venue_id=tzs_venue.venue_id
LEFT JOIN fdm.lk_csv_league_rounds AS rounds
	ON matches.league_id=rounds.league_id AND matches.league_season=rounds.league_season AND matches.league_round=rounds.league_round
LEFT JOIN fdm.lk_api_countries AS countries
	ON rounds.country_code=countries.country_code_2
LEFT JOIN fdm.lk_api_continents AS continents
	ON countries.continent_code=continents.continent_code
LEFT JOIN (SELECT DISTINCT country_code_2, pg_timezone FROM fdm.lk_api_venues_tz 
			 WHERE pg_timezone NOT IN ('Mexico/BajaSur', 'Mexico/BajaNorte', 'Brazil/Acre', 'Brazil/West')) as tzs_country
	ON rounds.country_code=tzs_country.country_code_2
WHERE CAST(matches.league_id AS text)||CAST(matches.league_season AS text) IN (
	SELECT CAST(league_id AS text)||CAST(league_season AS text) FROM fdm.tesis_lk_leagues) 
ORDER BY country_name, league_id, league_season, league_round_number
)