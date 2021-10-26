DROP TABLE IF EXISTS fdm.lk_api_venues_tz;
CREATE TABLE fdm.lk_api_venues_tz AS (
SELECT 
	venues.*,
	CASE 
		WHEN venues.country_name='Argentina' THEN 'America/Buenos_Aires'
		WHEN venues.country_name='Colombia' THEN 'America/Bogota'
		WHEN venues.country_name='Venezuela' THEN 'America/Caracas'
		WHEN venues.country_name='Ecuador' THEN 'America/Quito'
		WHEN venues.country_name='Peru' THEN 'America/Lima'
		WHEN venues.country_name='Chile' THEN 'America/Santiago'
		WHEN venues.country_name='Uruguay' THEN 'America/Montevideo'
		WHEN venues.country_name='Paraguay' THEN 'America/Asuncion'
		WHEN venues.country_name='Bolivia' THEN 'America/La_Paz'
		WHEN venues.country_name='Brazil' THEN tz_br_mx.tz_pgsql
		WHEN venues.country_name='Mexico' THEN tz_br_mx.tz_pgsql
	ELSE 'Check' END AS pg_timezone
FROM fdm.lk_api_venues AS venues
LEFT JOIN fdm.lk_csv_timezones_br_mx AS tz_br_mx 
	ON venues.venue_id=tz_br_mx.venue_id
);
