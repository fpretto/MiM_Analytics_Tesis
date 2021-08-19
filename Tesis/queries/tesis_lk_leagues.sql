-- Ligas a utilizar
DROP TABLE fdm.tesis_lk_leagues;
CREATE TABLE fdm.tesis_lk_leagues AS (
SELECT * FROM fdm.fp_leagues_completeness
WHERE league_type='League' AND stats_teams_pct>70 AND stats_players_pct>50 AND league_name!='Serie B'
)