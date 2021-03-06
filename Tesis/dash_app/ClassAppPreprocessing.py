import pandas as pd
import numpy as np
import json
import joblib
import sys
from sqlalchemy import create_engine
PATH_PI = 'C:/Repo/MiM_Analytics_Tesis/Tesis/performance_index/'
sys.path.insert(0, PATH_PI)
from PI_Preprocessing import PI_Preprocessing
from PI_FactorAnalysis import PI_FactorAnalysis
import importlib

#importlib.reload(PI_Preprocessing)
#importlib.reload(PI_FactorAnalysis)

class ClassPreprocessing:

    def __init__(self, config_data):
        self.config_data = config_data
        self.master_path = config_data['DataSources']['master_path']
        self.AR_players = config_data['DataSources']['AR_players']
        self.AR_seasons = config_data['DataSources']['AR_seasons']
        self.AR_rating_correction = config_data['DataSources']['rating_correction']
        self.PerfIndexObj = config_data['DataSources']['PerfIndexObject']

    def load_AR(self, dataset, source):
        """
        Queries data from PostgreSQL and creates dataframes
        :param config_data: JSON file with connection parameters
        :return:
            AR_season_player: data and stats by player and season
            AR_player: data and stats by player (all seasons)
        """
        uri = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
                self.config_data['PostgreSQL']['username'],
                self.config_data['PostgreSQL']['password'],
                self.config_data['PostgreSQL']['host'],
                self.config_data['PostgreSQL']['port'],
                self.config_data['PostgreSQL']['database'])

        engine = create_engine(uri)
        conn = engine.raw_connection()

        if source == 'pg':
            if dataset == 'player_seasons':
                AR = pd.read_sql_query("SELECT * FROM fdm.dash_ft_abt_season_players_train;", conn)
            elif dataset == 'player_all_seasons':
                AR = pd.read_sql_query("SELECT * FROM fdm.dash_ft_abt_players_train;", conn)
        else:
            if dataset == 'player_seasons':
                AR = pd.read_csv(self.master_path+self.AR_seasons, encoding='utf-8', decimal='.', sep='|')
            elif dataset == 'player_all_seasons':
                AR = pd.read_csv(self.master_path+self.AR_players, encoding='utf-8', decimal='.', sep='|')

        return AR

    def score_performance_index(self, AR):
        """
        Calculates Performance Index by player
        :param AR: dataframe with players to score
        :return:
            df_scored: input dataframe with ana aditional column (Performance Index)
        """
        dict_perf_index = joblib.load(PATH_PI+self.PerfIndexObj)

        df_scored = PI_Preprocessing().filter_and_data_engineering(AR, rating_correction=None, correct_rating=False)
        df_scored = PI_FactorAnalysis().score_index(df_scored, dict_perf_index)

        return df_scored

    def feature_engineering(self, df, dataset):
        """
        Prepares dataset to be ready to use in Dash
        :param df: dataframe
        :param dataset: type of dataset: Season, Player
        :return:
            df: processed dataframe
        """
        df['Perf_Index_scaled'] = df['Perf_Index_scaled'].apply(lambda x: round(x*100))
        df['Perf_Index_scaled'] = np.where(df['Perf_Index_scaled'] > 100, 100, df['Perf_Index_scaled'])
        df['Perf_Index_scaled'] = np.where(df['player_preferred_position'] == 'D', df['Perf_Index_scaled']-15, df['Perf_Index_scaled'])
        df['wavg_player_rating'] = df['wavg_player_rating'].apply(lambda x: round(x, 2))
        df['player_preferred_position'] = df['player_preferred_position'].map(self.config_data['ColumnValues']["player_preferred_position"])

        if dataset == 'player_seasons':
            df['season'] = df['league_season'].astype(str) + '/' + df['league_season'].apply(lambda x: str(x+1)[2:4])
            df = df[df['season'] != '2021/22'].copy()

        return df[(~df['player_name'].isna()) & (~df['team_name'].isna())]

    def load_score_process_data(self, dataset, source, generate_dropdown=False):
        """
        Loads data from PostgreSQL, calculates Performance Index and format data
        :param
            dataset: type of dataset: Season, Player
            generate_dropdown: flag to generate players dropdown for Dash
        :return:
            df: dataframe ready for Dash
        """

        AR = self.load_AR(dataset=dataset, source=source)
        df = self.score_performance_index(AR)
        df = self.feature_engineering(df, dataset=dataset)

        if (dataset == 'player_seasons') & generate_dropdown:
            dict_options = {}

            for country in df['team_country'].unique():
                dict_options[country] = {}
                for season in df[(df['team_country'] == country)]['season'].unique():
                    dict_options[country][str(season)] = {}
                    for team in df[(df['team_country'] == country) & (df['season'] == season)]['team_name']:
                        dict_options[country][str(season)][team] = df[(df['team_country'] == country) &
                                                                      (df['season'] == season) &
                                                                      (df['team_name'] == team)]['player_name'].unique()

            joblib.dump(dict_options, self.master_path+'dropdown_options.pkl')

        return df


