import urllib
import pandas as pd
import numpy as np


class Transformation:

    def __init__(self, response):
        self.data = response
        self.dict_countries = {'AR': 'Argentina', 'BO': 'Bolivia', 'BR': 'Brazil', 'CL': 'Chile', 'CO': 'Colombia',
                               'EC': 'Ecuador', 'PY': 'Paraguay', 'PE': 'Peru', 'UY': 'Uruguay', 'VE': 'Venezuela',
                               'MX': 'Mexico'}

    # Countries Data Transformation
    def csv_continents(self):
        """
        Transforms the CSV with continents to fit the SQL table
        :return:
            df
        """
        self.data.loc[self.data['continent_name'] == 'North America', 'continent_code'] = 'NA'
        return self.data

    def csv_countries(self):
        """
        Transforms the CSV with countries to fit the SQL table
        :return:
            df
        """
        self.data.loc[self.data['continent_name'] == 'North America', 'continent_code'] = 'NA'
        self.data.loc[self.data['country_name'] == 'Namibia', 'country_code_2'] = 'NA'
        self.data['country_code_un'] = self.data['country_code_un'].astype(int)
        cols = ['country_code_2', 'country_code_3', 'country_code_un', 'country_name', 'country_flag', 'continent_code']
        return self.data[cols]

    # Leagues and Seasons Data Transformation
    def api_leagues_seasons(self):
        """
        Transforms the API response from the Leagues endpoint and creates the LKPs Leagues and Seasons
        :return:
            df_leagues: DF with leagues id and description ready to load to DW
            df_seasons: DF with each season of each leagues id and description ready to load to DW
        """
        # Leagues
        df_leagues = pd.json_normalize(self.data["response"], sep="_")
        df_leagues['league_id'] = df_leagues['league_id'].astype(int)
        df_leagues.loc[df_leagues['country_name'] == 'Namibia', 'country_code'] = 'NA'
        del df_leagues["seasons"]
        del df_leagues["country_flag"]

        cols_leagues = ['league_id', 'league_name', 'league_type', 'league_logo', 'country_code', 'country_name']

        # Seasons
        df_seasons = pd.DataFrame()
        for idx in range(len(self.data["response"])):
            seasons = pd.json_normalize(self.data["response"][idx]['seasons'], sep='_')
            seasons.loc[:, 'league_id'] = self.data["response"][idx]['league']['id']
            df_seasons = df_seasons.append(seasons)

        df_seasons.rename(columns={'year': 'season'}, inplace=True)
        df_seasons['league_id'] = df_seasons['league_id'].astype(int)
        cols_seasons = ['league_id', 'season', 'start', 'end', 'current', 'coverage_fixtures_events',
                        'coverage_fixtures_lineups', 'coverage_fixtures_statistics_fixtures',
                        'coverage_fixtures_statistics_players', 'coverage_standings', 'coverage_players',
                        'coverage_top_scorers', 'coverage_top_assists', 'coverage_top_cards',
                        'coverage_injuries', 'coverage_predictions', 'coverage_odds']

        return df_leagues[cols_leagues], df_seasons[cols_seasons]

    def api_venues(self, query_val):
        df_venues = pd.json_normalize(self.data["response"], sep="_")
        dict_countries_rev = {value: key for (key, value) in self.dict_countries.items()}
        df_venues['country_code_2'] = dict_countries_rev[query_val]
        cols_venues = ['id', 'name', 'address', 'city', 'country_code_2', 'country', 'capacity', 'surface', 'image']

        for col in ['name', 'address', 'city', 'country_code_2', 'country', 'capacity', 'surface', 'image']:
            if col not in df_venues.columns:
                df_venues[col] = None

        return df_venues[cols_venues]

    def api_teams(self, query_val):
        df_teams = pd.json_normalize(self.data["response"], sep="_")

        dict_countries_rev = {value: key for (key, value) in self.dict_countries.items()}
        if query_val is None:
            df_teams['country_code_2'] = df_teams['team_country'].map(dict_countries_rev)
        else:
            df_teams['country_code_2'] = dict_countries_rev[query_val]
        df_teams['team_id'] = df_teams['team_id'].astype(int)
        df_teams['team_founded'] = df_teams['team_founded'].fillna(9999).astype(int)
        df_teams['venue_id'] = df_teams['venue_id'].fillna(9999).astype(int)
        cols_teams = ['team_id', 'team_name', 'country_code_2', 'team_country', 'team_founded', 'team_national',
                      'team_logo', 'venue_id']

        for col in ['team_name', 'country_code_2', 'team_country', 'team_founded', 'team_national', 'team_logo', 'venue_id']:
            if col not in df_teams.columns:
                df_teams[col] = None


        return df_teams[cols_teams]

    def api_players(self, query_val):
        df_players = pd.DataFrame()
        for idx in range(len(self.data["response"])):
            df_player = pd.concat([pd.json_normalize(self.data["response"][idx]['player'], sep='_'),
                                   pd.json_normalize(self.data["response"][idx]['statistics'], sep='_')[
                                       'games_position'].rename('position')], axis=1)

            df_players = df_players.append(df_player)

    def api_matches(self):
        try:
            df_matches = pd.json_normalize(self.data["response"], sep="_")
            df_matches['fixture_id'] = df_matches['fixture_id'].astype(int)
            df_matches['teams_home_winner'] = np.select([df_matches['teams_home_winner'] == True,
                                                         df_matches['teams_home_winner'] == False,
                                                         df_matches['teams_home_winner'].isna()], [1, -1, 0], default=99)

            df_matches['teams_away_winner'] = np.select([df_matches['teams_away_winner'] == True,
                                                         df_matches['teams_away_winner'] == False,
                                                         df_matches['teams_away_winner'].isna()], [1, -1, 0], default=99)

            df_matches['goals_home'] = df_matches['goals_home'].fillna(-1)
            df_matches['goals_away'] = df_matches['goals_away'].fillna(-1)
            df_matches['fixture_venue_id'] = df_matches['fixture_venue_id'].fillna(-1)
            df_matches['score_halftime_home'] = df_matches['score_halftime_home'].fillna(-1)
            df_matches['score_halftime_away'] = df_matches['score_halftime_away'].fillna(-1)
            df_matches['score_extratime_home'] = df_matches['score_extratime_home'].fillna(-1)
            df_matches['score_extratime_away'] = df_matches['score_extratime_away'].fillna(-1)
            df_matches['score_penalty_home'] = df_matches['score_penalty_home'].fillna(-1)
            df_matches['score_penalty_away'] = df_matches['score_penalty_away'].fillna(-1)
            df_matches['fixture_timestamp'] = df_matches['fixture_timestamp'].fillna(-1)
            df_matches['fixture_periods_first'] = df_matches['fixture_periods_first'].fillna(-1)
            df_matches['fixture_periods_second'] = df_matches['fixture_periods_second'].fillna(-1)
            df_matches['fixture_status_elapsed'] = df_matches['fixture_status_elapsed'].fillna(-1)

            cols_to_keep = ['fixture_id', 'fixture_referee', 'fixture_timezone', 'fixture_date', 'fixture_timestamp',
                            'fixture_periods_first', 'fixture_periods_second', 'fixture_status_short',
                            'fixture_status_long', 'fixture_status_elapsed', 'fixture_venue_id', 'league_id',
                            'league_season', 'league_round', 'teams_home_id', 'teams_home_name', 'teams_home_winner',
                            'teams_away_id', 'teams_away_name', 'teams_away_winner', 'goals_home', 'goals_away',
                            'score_halftime_home', 'score_halftime_away', 'score_extratime_home', 'score_extratime_away',
                            'score_penalty_home', 'score_penalty_away']

            for col in ['fixture_referee', 'fixture_timezone', 'fixture_date', 'fixture_timestamp',
                            'fixture_periods_first', 'fixture_periods_second', 'fixture_status_short',
                            'fixture_status_long', 'fixture_status_elapsed', 'fixture_venue_id', 'league_id',
                            'league_season', 'league_round', 'teams_home_id', 'teams_home_name', 'teams_home_winner',
                            'teams_away_id', 'teams_away_name', 'teams_away_winner', 'goals_home', 'goals_away',
                            'score_halftime_home', 'score_halftime_away', 'score_extratime_home', 'score_extratime_away',
                            'score_penalty_home', 'score_penalty_away']:
                if col not in df_matches.columns:
                    df_matches[col] = None

            return df_matches[cols_to_keep]

        except Exception as error:
            print(f"Error procesando Matches: %s" % error)

    def api_matches_stats(self, fixture_id):
        try:
            # Home team statistics
            home_team = pd.json_normalize(self.data["response"][0]["team"], sep="_")
            home_team['fixture_id'] = fixture_id
            home_team['fl_home'] = True
            home_stats = pd.json_normalize(self.data["response"][0]["statistics"], sep="_").set_index(
                'type').transpose().reset_index(drop=True)
            df_home = pd.concat([home_team[['fixture_id', 'fl_home', 'id', 'name']], home_stats.fillna(0)], axis=1)

            # Away team statistics
            away_team = pd.json_normalize(self.data["response"][1]["team"], sep="_")
            away_team['fixture_id'] = fixture_id
            away_team['fl_home'] = False
            away_stats = pd.json_normalize(self.data["response"][1]["statistics"], sep="_").set_index(
                'type').transpose().reset_index(drop=True)
            df_away = pd.concat([away_team[['fixture_id', 'fl_home', 'id', 'name']], away_stats.fillna(0)], axis=1)

            # Match Statistics
            df_match_stats = pd.concat([df_home, df_away])
            df_match_stats.columns = [col.lower().replace(' ', '_') for col in df_match_stats.columns]

            df_match_stats['ball_possession'] = df_match_stats['ball_possession'].apply(
                    lambda x: float(str(x)[0:2]) / 100 if len(str(x)) > 2 else float(str(x)[0:1]) / 100)
            df_match_stats['passes_pct'] = df_match_stats['passes_%'].apply(
                    lambda x: float(str(x)[0:2]) / 100 if len(str(x)) > 2 else float(str(x)[0:1]) / 100)
            del df_match_stats['passes_%']

            cols_to_keep = ['fixture_id', 'id', 'name', 'fl_home', 'shots_on_goal', 'shots_off_goal',
                            'total_shots', 'blocked_shots', 'shots_insidebox', 'shots_outsidebox', 'fouls', 'corner_kicks',
                            'offsides', 'ball_possession', 'yellow_cards', 'red_cards', 'goalkeeper_saves', 'total_passes',
                            'passes_accurate', 'passes_pct']

            for col in ['name', 'fl_home', 'shots_on_goal', 'shots_off_goal',
                            'total_shots', 'blocked_shots', 'shots_insidebox', 'shots_outsidebox', 'fouls', 'corner_kicks',
                            'offsides', 'ball_possession', 'yellow_cards', 'red_cards', 'goalkeeper_saves', 'total_passes',
                            'passes_accurate', 'passes_pct']:
                if col not in df_match_stats.columns:
                    df_match_stats[col] = None

            return df_match_stats[cols_to_keep]

        except Exception as error:
            print(f"Error procesando Match Stats: %s" % error)

    def api_matches_events(self, fixture_id):
        try:
            df_match_events = pd.json_normalize(self.data["response"], sep="_").reset_index()
            df_match_events['fixture_id'] = fixture_id
            df_match_events['time_extra'] = df_match_events['time_extra'].fillna(-1)
            df_match_events['team_id'] = df_match_events['team_id'].fillna(-1)
            df_match_events['player_id'] = df_match_events['player_id'].fillna(-1)
            df_match_events['assist_id'] = df_match_events['assist_id'].fillna(-1)

            cols_to_keep = ['fixture_id', 'index', 'time_elapsed', 'time_extra', 'type', 'detail', 'comments', 'team_id',
                            'player_id', 'player_name', 'assist_id', 'assist_name']

            for col in ['time_elapsed', 'time_extra', 'type', 'detail', 'comments', 'team_id',
                            'player_id', 'player_name', 'assist_id', 'assist_name']:
                if col not in df_match_events.columns:
                    df_match_events[col] = None

            return df_match_events[cols_to_keep]

        except Exception as error:
            print(f"Error procesando Events: %s" % error)

    def api_matches_player_stats(self, fixture_id):
        try:
            ## Home
            df_players_home = pd.DataFrame()
            for idx in range(len(self.data["response"][0]['players'])):
                df_player = pd.concat([pd.DataFrame([fixture_id], columns=['fixture_id']),
                                       pd.json_normalize(self.data["response"][0]['team'], sep='_')['id'].rename(
                                           'team_id'),
                                       pd.json_normalize(self.data["response"][0]['players'][idx]['player'],
                                                         sep='_').rename(
                                               columns={'id': 'player_id', 'name': 'player_name', 'photo': 'player_photo'}),
                                       pd.json_normalize(self.data["response"][0]['players'][idx]['statistics'],
                                                         sep='_')], axis=1)

                df_players_home = df_players_home.append(df_player)

            ## Away
            df_players_away = pd.DataFrame()
            for idx in range(len(self.data["response"][1]['players'])):
                df_player = pd.concat([pd.DataFrame([fixture_id], columns=['fixture_id']),
                                       pd.json_normalize(self.data["response"][1]['team'], sep='_')['id'].rename('team_id'),
                                       pd.json_normalize(self.data["response"][1]['players'][idx]['player'], sep='_').rename(
                                               columns={'id': 'player_id', 'name': 'player_name', 'photo': 'player_photo'}),
                                       pd.json_normalize(self.data["response"][1]['players'][idx]['statistics'],
                                                         sep='_')], axis=1)

                df_players_away = df_players_away.append(df_player)

            ## Merge
            df_players_stats = pd.concat([df_players_home, df_players_away]).fillna(0).reset_index(drop=True)
            df_players_stats['passes_accuracy'] = df_players_stats['passes_accuracy'].apply(
                    lambda x: float(str(x)[0:2]) / 100 if len(str(x)) > 2 else float(str(x)[0:1]) / 100)
            df_players_stats['games_rating'] = df_players_stats['games_rating'].replace('–', '-1').astype(float)
            df_players = df_players_stats[['player_id', 'player_name', 'player_photo']].drop_duplicates().copy()
            df_players_stats.drop(columns=['player_photo'], inplace=True)

            return df_players, df_players_stats

        except Exception as error:
            print(f"Error procesando Player Stats: %s" % error)

    def api_matches_lineups(self, fixture_id):
        try:
            ## Teams
            df_lineup_teams = pd.json_normalize(self.data["response"], sep='_')
            df_lineup_teams['fixture_id'] = fixture_id
            cols_to_keep = ['fixture_id', 'team_id', 'team_colors', 'coach_id', 'formation']
            for col in ['team_colors', 'coach_id', 'formation']:
                if col not in df_lineup_teams.columns:
                    df_lineup_teams[col] = None

            df_lineup_teams = df_lineup_teams[cols_to_keep]

            ## Players
            # Home Team
            df_lineup_start_home = pd.json_normalize(self.data["response"][0]["startXI"], sep='_')
            df_lineup_start_home['start_xi'] = True
            df_lineup_subs_home = pd.json_normalize(self.data["response"][0]["substitutes"], sep='_')
            df_lineup_subs_home['start_xi'] = False
            df_lineup_home = pd.concat([df_lineup_start_home, df_lineup_subs_home])
            df_lineup_home['fixture_id'] = fixture_id
            df_lineup_home['team_id'] = self.data["response"][0]['team']['id']

            # Away Team
            df_lineup_start_away = pd.json_normalize(self.data["response"][1]["startXI"], sep='_')
            df_lineup_start_away['start_xi'] = True
            df_lineup_subs_away = pd.json_normalize(self.data["response"][1]["substitutes"], sep='_')
            df_lineup_subs_away['start_xi'] = False
            df_lineup_away = pd.concat([df_lineup_start_away, df_lineup_subs_away])
            df_lineup_away['fixture_id'] = fixture_id
            df_lineup_away['team_id'] = self.data["response"][1]['team']['id']

            # Match Lineup
            cols_to_keep = ['fixture_id', 'team_id', 'player_id', 'player_name', 'player_number', 'player_pos',
                            'player_grid', 'start_xi']

            for col in ['player_id', 'player_name', 'player_number', 'player_pos','player_grid', 'start_xi']:
                if col not in df_lineup_home.columns:
                    df_lineup_home[col] = None
                if col not in df_lineup_away.columns:
                    df_lineup_away[col] = None

            df_lineup_players = pd.concat([df_lineup_home[cols_to_keep], df_lineup_away[cols_to_keep]], ignore_index=True)

            return df_lineup_teams, df_lineup_players

        except Exception as error:
            print(f"Error procesando Lineups: %s" % error)

    def api_matches_predictions(self, fixture_id):
        try:
            df_pred = pd.concat([pd.DataFrame([fixture_id], columns=['fixture_id']),
                                 pd.json_normalize(self.data['response'][0]['predictions'], sep='_').fillna(0)], axis=1)

            df_pred['percent_home'] = df_pred['percent_home'].apply(
                    lambda x: float(x[0:2]) / 100 if len(x) > 2 else float(x[0:1]) / 100)
            df_pred['percent_draw'] = df_pred['percent_draw'].apply(
                    lambda x: float(x[0:2]) / 100 if len(x) > 2 else float(x[0:1]) / 100)
            df_pred['percent_away'] = df_pred['percent_away'].apply(
                    lambda x: float(x[0:2]) / 100 if len(x) > 2 else float(x[0:1]) / 100)

            df_pred['fixture_id'] = df_pred['fixture_id'].astype(int)
            df_pred['under_over'] = df_pred['under_over'].astype(str)
            df_pred['goals_home'] = df_pred['goals_home'].astype(str)
            df_pred['goals_away'] = df_pred['goals_away'].astype(str)
            df_pred['winner_name'] = df_pred['winner_name'].astype(str)
            df_pred['advice'] = df_pred['advice'].astype(str)
            df_pred['winner_comment'] = df_pred['winner_comment'].astype(str)

            return df_pred

        except Exception as error:
            print(f"Error procesando Predictions: %s" % error)

    def api_standings(self):
        try:
            df_standings = pd.json_normalize(self.data['response'][0]['league']['standings'][0], sep='_')
            df_standings['league_id'] = self.data['response'][0]['league']['id']
            df_standings['league_name'] = self.data['response'][0]['league']['name']
            df_standings['league_season'] = self.data['response'][0]['league']['season']
            df_standings['country_name'] = self.data['response'][0]['league']['country']

            cols = ['league_id', 'league_season', 'rank', 'team_id', 'team_name', 'points', 'goalsDiff', 'status', 'form',
                    'league_name', 'country_name', 'group', 'description', 'all_played', 'all_win', 'all_draw', 'all_lose',
                    'all_goals_for', 'all_goals_against', 'home_played', 'home_win', 'home_draw', 'home_lose',
                    'home_goals_for', 'home_goals_against', 'away_played', 'away_win', 'away_draw', 'away_lose',
                    'away_goals_for', 'away_goals_against', 'update']

            for col in ['all_played', 'all_win', 'all_draw', 'all_lose', 'all_goals_for', 'all_goals_against',
                        'home_played', 'home_win', 'home_draw', 'home_lose', 'home_goals_for', 'home_goals_against',
                        'away_played', 'away_win', 'away_draw', 'away_lose', 'away_goals_for', 'away_goals_against']:
                df_standings.loc[:, col].fillna(-1, inplace=True)

            return df_standings[cols]

        except Exception as error:
            print(f"Error procesando Standings: %s" % error)



