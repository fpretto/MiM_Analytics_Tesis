from Extract import Extract
from Transformation import Transformation
from Load_PostgreSQL import PostgreSQL
import json
import pandas as pd
import distutils.util

#etl_data = json.load(open('data/data_config.json'))
#extractObj = Extract(etl_data)
#pgEngine = PostgreSQL(etl_data)

class ETL_Engine:
    def __init__(self, etl_data):
        self.etl_data = etl_data
        self.extractObj = Extract(self.etl_data)
        self.pgEngine = PostgreSQL(self.etl_data)

        for endpoint in self.etl_data['ETL']['api'].keys():
            if bool(distutils.util.strtobool(self.etl_data['ETL']['api'][endpoint]['process'])):
                print(endpoint, self.etl_data['ETL']['api'][endpoint])

                # getattr function takes in function name of class and calls it.
                func_name = 'etl_' + endpoint
                getattr(self, func_name)()

        for file in self.etl_data['ETL']['csv'].keys():
            if bool(distutils.util.strtobool(self.etl_data['ETL']['csv'][file]['process'])):
                print(file)

                # getattr function takes in function name of class and calls it.
                func_name = 'etl_' + file
                getattr(self, func_name)()


    # Continents
    def etl_continents(self):
        csv_continents = self.extractObj.getCSVData(csv_name='continents', separator=',')
        df_continents = Transformation(response=csv_continents).csv_continents()
        self.pgEngine.load_batch(df=df_continents, table_name='lk_api_continents')

    # Countries
    def etl_countries(self):
        csv_countries = self.extractObj.getCSVData(csv_name='countries', separator=',')
        df_countries = Transformation(response=csv_countries).csv_countries()
        self.pgEngine.load_batch(df=df_countries, table_name='lk_api_countries')

    # Leagues and Seasons
    def etl_leagues(self):
        api_response = self.extractObj.getAPIFootballData(endpoint='leagues')
        df_leagues, df_seasons = Transformation(response=api_response).api_leagues_seasons()
        self.pgEngine.load_batch(df=df_leagues, table_name='lk_api_leagues')
        self.pgEngine.load_batch(df=df_seasons, table_name='lk_api_seasons')

    # League Rounds
    def etl_league_rounds(self):
        csv_rounds = self.extractObj.getCSVData(csv_name='league_rounds', separator=';')
        self.pgEngine.load_batch(df=csv_rounds, table_name='lk_csv_league_rounds')

    # Timezones Brazil
    def etl_timezones_br_mx(self):
        csv_tz = self.extractObj.getCSVData(csv_name='timezones_br_mx', separator=';')
        self.pgEngine.load_batch(df=csv_tz, table_name='lk_csv_timezones_br_mx')

    # Venues
    def etl_venues(self):
        for query_param in self.etl_data['ETL']['api']['venues']['params'].keys():
            for query_val in self.etl_data['ETL']['api']['venues']['params'][query_param]:
                query = f'?{query_param}={str(query_val)}'
                print(f'Procesando Venues de {str(query_val)}')
                api_response = self.extractObj.getAPIFootballData(endpoint='venues', query=query)
                df_venues = Transformation(response=api_response).api_venues(query_val)
                self.pgEngine.load_batch(df=df_venues, table_name='lk_api_venues')

    # Teams
    def etl_teams(self):
        if len(self.etl_data['ETL']['api']['teams']['params']['country']) > 0:

            for country in self.etl_data['ETL']['api']['teams']['params']['country']:
                query = f'?country={str(country)}'
                print(f'Procesando Teams de {str(country)}')
                try:
                    api_response = self.extractObj.getAPIFootballData(endpoint='teams', query=query)
                    df_teams = Transformation(response=api_response).api_teams(country)
                    self.pgEngine.load_batch(df=df_teams, table_name='lk_api_teams')
                except Exception as error:
                    print(f"Error procesando Teams de {str(country)}: %s" % error)
        else:
            for league_id in self.etl_data['ETL']['api']['teams']['params']['league']:
                for season in self.etl_data['ETL']['api']['teams']['params']['season']:
                    query = f'?league={str(league_id)}&season={str(season)}'
                    print(f'Procesando Teams de la Temporada {str(season)} de la Liga {str(league_id)}')
                    try:
                        api_response = self.extractObj.getAPIFootballData(endpoint='teams', query=query)
                        df_teams = Transformation(response=api_response).api_teams(query_val=None)
                        self.pgEngine.load_batch(df=df_teams, table_name='lk_api_teams')
                    except Exception as error:
                        print(f"Error procesando Teams de la Temporada {str(season)} de la Liga {str(league_id)}': %s" % error)

    def etl_matches(self):
        for league_id in self.etl_data['ETL']['api']['matches']['params']['league']:
            for season in self.etl_data['ETL']['api']['matches']['params']['season']:
                query = f'?league={str(league_id)}&season={str(season)}'
                print(f'Procesando Temporada {str(season)} de la Liga {str(league_id)}')
                try:
                    api_response = self.extractObj.getAPIFootballData(endpoint='fixture', query=query)
                    df_matches = Transformation(response=api_response).api_matches()
                    self.pgEngine.load_batch(df=df_matches, table_name='ft_api_matches')
                except Exception as error:
                    print(f"Error procesando Temporada {str(season)} de la Liga {str(league_id)}: %s" % error)

    def etl_matches_events(self):
        if len(self.etl_data['ETL']['api']['matches_events']['params']['fixture_id']) > 0:
            for fixture in self.etl_data['ETL']['api']['matches_events']['params']['fixture_id']:
                query = f'?fixture={fixture}'
                print(f'Procesando partido {str(fixture)}')

                try:
                    # Extract
                    api_response_stats = self.extractObj.getAPIFootballData(endpoint='match_stats', query=query)
                    api_response_events = self.extractObj.getAPIFootballData(endpoint='match_events', query=query)
                    api_response_player_stats = self.extractObj.getAPIFootballData(endpoint='match_player_stats', query=query)
                    api_response_lineups = self.extractObj.getAPIFootballData(endpoint='match_lineups', query=query)

                    # Transform
                    df_match_stats = Transformation(response=api_response_stats).api_matches_stats(fixture)
                    df_match_events = Transformation(response=api_response_events).api_matches_events(fixture)
                    df_players, df_players_stats = Transformation(
                        response=api_response_player_stats).api_matches_player_stats(fixture)
                    df_lineup_teams, df_lineup_players = Transformation(response=api_response_lineups).api_matches_lineups(
                        fixture)

                    # Load
                    self.pgEngine.load_batch(df=df_match_stats, table_name='ft_api_matches_stats_teams')
                    self.pgEngine.load_batch(df=df_match_events, table_name='ft_api_matches_events')
                    self.pgEngine.load_batch(df=df_players, table_name='lk_api_players')
                    self.pgEngine.load_batch(df=df_players_stats, table_name='ft_api_matches_stats_players')
                    self.pgEngine.load_batch(df=df_lineup_teams, table_name='ft_api_matches_lineups_teams')
                    self.pgEngine.load_batch(df=df_lineup_players, table_name='ft_api_matches_lineups_players')

                except Exception as error:
                    print(f"Error procesando partido {str(fixture)}: %s" % error)
        else:
            for league_id in self.etl_data['ETL']['api']['matches_events']['params']['league']:
                for season in self.etl_data['ETL']['api']['matches_events']['params']['season']:
                    query = f'?league={str(league_id)}&season={str(season)}'
                    print(f'Procesando Partidos de Temporada {str(season)} de la Liga {str(league_id)}')
                    # Get matches of the league and season
                    api_response = self.extractObj.getAPIFootballData(endpoint='fixture', query=query)
                    df_matches = Transformation(response=api_response).api_matches()

                    # Filter matches already in DW
                    ft_api_matches = pd.read_sql_query("SELECT fixture_id FROM fdm.ft_api_matches_stats_players",
                                                       self.pgEngine.conn)
                    df_process = df_matches[~df_matches['fixture_id'].isin(ft_api_matches['fixture_id'])]

                    print(f'Hay {len(df_process)} partidos para procesar')

                    if len(df_process) > 0:
                        for fixture in df_process['fixture_id'].unique():
                            print(f'Partido: {str(fixture)}')
                            try:
                                query = f'?fixture={fixture}'
                                # Extract
                                print('Extract')
                                api_response_stats = self.extractObj.getAPIFootballData(endpoint='match_stats',
                                                                                        query=query)
                                api_response_events = self\
                                    .extractObj.getAPIFootballData(endpoint='match_events',
                                                                                         query=query)
                                api_response_player_stats = self.extractObj.getAPIFootballData(endpoint='match_player_stats',
                                                                                               query=query)
                                api_response_lineups = self.extractObj.getAPIFootballData(endpoint='match_lineups',
                                                                                          query=query)

                                # Transform
                                print('Transform')
                                print('match_stats')
                                df_match_stats = Transformation(response=api_response_stats).api_matches_stats(fixture)
                                print('match_events')
                                df_match_events = Transformation(response=api_response_events).api_matches_events(fixture)
                                print('lineups')
                                df_lineup_teams, df_lineup_players = Transformation(
                                        response=api_response_lineups).api_matches_lineups(fixture)
                                print('player_stats')
                                if api_response_player_stats['results'] > 0:
                                    df_players, df_players_stats = Transformation(
                                        response=api_response_player_stats).api_matches_player_stats(fixture)
                                else:
                                    print('Estadistica de jugador no disponible')

                                # Load
                                print('Load')
                                self.pgEngine.load_batch(df=df_match_stats, table_name='ft_api_matches_stats_teams')
                                self.pgEngine.load_batch(df=df_match_events, table_name='ft_api_matches_events')
                                if api_response_player_stats['results'] > 0:
                                    self.pgEngine.load_batch(df=df_players, table_name='lk_api_players')
                                    self.pgEngine.load_batch(df=df_players_stats, table_name='ft_api_matches_stats_players')
                                self.pgEngine.load_batch(df=df_lineup_teams, table_name='ft_api_matches_lineups_teams')
                                self.pgEngine.load_batch(df=df_lineup_players, table_name='ft_api_matches_lineups_players')

                            except Exception as error:
                                print(f"Error procesando partido {str(fixture)} de la Temporada {str(season)} de la "
                                      f"Liga {str(league_id)}: %s" % error)

    def etl_predictions(self):
        for league_id in self.etl_data['ETL']['api']['predictions']['params']['league']:
            for season in self.etl_data['ETL']['api']['predictions']['params']['season']:
                query = f'?league={str(league_id)}&season={str(season)}'
                print(f'Procesando Predicciones de Temporada {str(season)} de la Liga {str(league_id)}')
                try:
                    # Get matches of the league and season
                    api_response = self.extractObj.getAPIFootballData(endpoint='fixture', query=query)
                    df_matches = Transformation(response=api_response).api_matches()

                    # Filter matches already in DW
                    query_check = "SELECT fixture_id FROM fdm.ft_api_matches_predictions"
                    ft_api_matches_pred = pd.read_sql_query(query_check, self.pgEngine.conn)
                    df_process = df_matches[~df_matches['fixture_id'].isin(ft_api_matches_pred['fixture_id'])]

                    print(f'Hay {len(df_process)} partidos para procesar')

                    if len(df_process) > 0:
                        for fixture in df_process['fixture_id'].unique():
                            print(f'Partido: {str(fixture)}')
                            try:
                                query = f'?fixture={fixture}'
                                api_response = self.extractObj.getAPIFootballData(endpoint='predictions', query=query)
                                df_predictions = Transformation(response=api_response).api_matches_predictions(fixture)
                                self.pgEngine.load_batch(df=df_predictions, table_name='ft_api_matches_predictions')

                            except Exception as error:
                                print(f"Error procesando partido {str(fixture)} de la Temporada {str(season)} de la "
                                      f"Liga {str(league_id)}: %s" % error)
                except Exception as error:
                    print(f"Error procesando partidos de la Temporada {str(season)} de la "
                          f"Liga {str(league_id)}: %s" % error)

    def etl_standings(self):
        for league_id in self.etl_data['ETL']['api']['standings']['params']['league']:
            for season in self.etl_data['ETL']['api']['standings']['params']['season']:
                query = f'?league={str(league_id)}&season={str(season)}'
                print(f'Procesando Standings de Temporada {str(season)} de la Liga {str(league_id)}')

                # Replace standings if season is current
                query_check = f"SELECT * FROM fdm.lk_api_seasons WHERE league_id={league_id} AND season={season} " \
                              f"ORDER BY date_start DESC"
                lk_api_seasons = pd.read_sql_query(query_check, self.pgEngine.conn)

                if lk_api_seasons.loc[0, 'current']:
                    query_delete = f"DELETE " \
                        f"" \
                        f"FROM fdm.ft_api_standings WHERE league_id={league_id} AND league_season={season} "
                    self.pgEngine.cursor.execute(query_delete)
                    self.pgEngine.conn.commit()

                # Add standings
                try:
                    api_response = self.extractObj.getAPIFootballData(endpoint='standings', query=query)
                    df_standings = Transformation(response=api_response).api_standings()
                    
                    self.pgEngine.load_batch(df=df_standings, table_name='ft_api_standings')

                except Exception as error:
                    print(f"Error procesando standings de la Temporada {str(season)} de la "
                          f"Liga {str(league_id)}: %s" % error)

    def etl_transfers(self):
        for league_id in self.etl_data['ETL']['api']['transfers']['params']['league']:
            print(f'Procesando Transfers de la Liga {str(league_id)}')

            # Retrieve all teams of the league
            query_check = f"SELECT DISTINCT teams_home_id FROM fdm.ft_api_matches WHERE league_id={league_id}"
            lk_api_teams = pd.read_sql_query(query_check, self.pgEngine.conn)

            # Add transfers
            for team_id in lk_api_teams['teams_home_id'].unique():
                query = f'?team={str(team_id)}'
                try:
                    api_response = self.extractObj.getAPIFootballData(endpoint='transfers', query=query)
                    df_transfers = Transformation(response=api_response).api_transfers()
                    self.pgEngine.load_batch(df=df_transfers, table_name='lk_api_transfers')

                except Exception as error:
                    print(f"Error procesando transfers del equipo {str(team_id)} de la "
                          f"Liga {str(league_id)}: %s" % error)

    def etl_trophies(self):
        for league_id in self.etl_data['ETL']['api']['trophies']['params']['league']:
            print(f'Procesando Transfers de la Liga {str(league_id)}')

            # Retrieve all teams of the league
            query_check = f"SELECT DISTINCT player_id FROM fdm.ft_api_matches_stats_players AS stats_players " \
                          f"LEFT JOIN fdm.ft_api_matches AS matches " \
                          f"ON stats_players.fixture_id=matches.fixture_id " \
                          f"WHERE matches.league_id={league_id}"

            lk_api_players = pd.read_sql_query(query_check, self.pgEngine.conn)

            # Add standings
            for player_id in lk_api_players['player_id'].unique():
                query = f'?player={str(player_id)}'
                try:
                    api_response = self.extractObj.getAPIFootballData(endpoint='trophies', query=query)
                    if len(api_response['response']) > 0:
                        df_trophies = Transformation(response=api_response).api_trophies(player_id)
                        self.pgEngine.load_batch(df=df_trophies, table_name='lk_api_trophies')

                except Exception as error:
                    print(f"Error procesando trophies del jugador {str(player_id)} de la "
                          f"Liga {str(league_id)}: %s" % error)

if __name__ == '__main__':

    etl_data = json.load(open('data_config.json'))
    ETL_Engine(etl_data)
