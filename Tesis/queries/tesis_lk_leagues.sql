-- Ligas a utilizar (Modelo ML)
DROP TABLE IF EXISTS fdm.tesis_lk_leagues;
CREATE TABLE fdm.tesis_lk_leagues AS (
SELECT * FROM fdm.tesis_lk_leagues_completeness
WHERE league_type='League' AND stats_teams_pct>70 AND stats_players_pct>50 AND league_name!='Serie B'
);


-- Ligas a utilizar (Soccerment)
DROP TABLE IF EXISTS fdm.dash_lk_leagues;
CREATE TABLE fdm.dash_lk_leagues AS (
SELECT A.* FROM fdm.tesis_lk_leagues_completeness AS A
LEFT JOIN fdm.lk_api_countries AS B
	ON A.country_name=B.country_name
WHERE A.league_type='League' AND stats_players_pct>70 AND league_name!='Serie B' --AND B.continent_code IN ('NA', 'SA')
);