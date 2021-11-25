-- Unaccent player names
DROP TABLE IF EXISTS fdm.fp_lk_player_names;
CREATE TABLE fdm.fp_lk_player_names AS(
SELECT DISTINCT player_id, fdm.unaccent(player_name) AS player_name FROM fdm.ft_api_matches_stats_players
WHERE player_id>0
ORDER BY player_id
);

-- Unify player names
UPDATE fdm.fp_lk_player_names AS players
SET player_name = lkp.player_name
FROM
    (VALUES
        (41190, 'Carlos da Silva Junior'),
        (39583, 'Marco Aldair Rodriguez Iraola'),
        (278497, 'Bruno Marques'),
	 	(6631, 'Nicolas Reniero'),
	 	(35604, 'Roger Martinez'),
	 	(9971, 'Antony Santos'),
	 	(9976, 'Pablo Felipe'),
	 	(6387, 'Cristian Agustin Fontana'),
	 	(70841, 'Blas Armoa Nunez'),
	 	(13490, 'Michael Nike Gomez'),
	 	(9726, 'Renato Kayser'),
	 	(6356, 'Lisandro Cabrera'),
	 	(10432, 'Junior Santos'),
	 	(35991, 'Daniel Villalba'),
	 	(35988, 'Ake Arnaud Loba'),
	 	(5257, 'Juan Sanchez Sotelo'),
	 	(39794, 'Flavio Leonardo Gomez'),
	 	(10399, 'Jonathan Alvez'),
	 	(59541, 'Guillermo Murillo'),
	 	(39805, 'Emanuel Herrera'),
	 	(9324, 'Hector Ariel Bustamante'),
	 	(75913, 'Agustin Ramirez'),
	 	(6011, 'Rafael Santos Borre'),
	 	(13529, 'William Palacios'),
	 	(39402, 'Sebastian La Torre'),
	 	(39831, 'Jean Deza'),
	 	(13662, 'Juan David Perez'),
	 	(46856, 'Saul Berjon'),
	 	(39404, 'Cristian Lasso'),
	 	(41450, 'Cristian Arango'),
	 	(5983, 'Mauro Zarate'),
	 	(39472, 'Jorginho Sernaque'),
	 	(47579, 'Ezequiel Avila'),
	 	(36312, 'Francisco Da Costa'),
	 	(13793, 'Carmelo Valencia'),
	 	(11621, 'Lucas Guiliano Passerini'),
	 	(11778, 'Jason Flores Abrigo'),
	 	(6448, 'Brian Mansilla'),
	 	(10367, 'Vinicius Lopez'),
	 	(2435, 'Luiz Da Silva'),
	 	(11838, 'Matias Campos Lopez'),
	 	(64173, 'Valentin Viola'),
	 	(5710, 'Nicolas Contin'),
	 	(44645, 'Jhon Freddy Pajoy'),
	 	(13558, 'David Cortes Armero'),
	 	(80190, 'Victor Rangel'),
	 	(36521, 'Jose Luis Mendez'),
	 	(39830, 'Sergio Almiron'),
	 	(95652, 'Ronal Huaccha'),
	 	(10147, 'Vitinho'),
	 	(271784, 'Davi Araujo'),
	 	(106612, 'Saulo Mineiro'),
	 	(10174, 'Gabriel Barbosa'),
	 	(6189, 'Norberto Briasco Balekian'),
	 	(16362, 'Luis Daniel Gonzalez'),
	 	(6127, 'Pablo Maximiliano Cuadra'),
	 	(6040, 'Juan Cruz Kaprof')
	 	
    ) AS lkp (player_id, player_name)
WHERE players.player_id = lkp.player_id;

-- Delete duplicate rows
DELETE FROM fdm.fp_lk_player_names AS A USING (
  SELECT MIN(ctid) AS ctid, player_id
	FROM fdm.fp_lk_player_names 
	GROUP BY player_id HAVING COUNT(*) > 1
  ) AS B
WHERE A.player_id = B.player_id AND A.ctid <> B.ctid;
