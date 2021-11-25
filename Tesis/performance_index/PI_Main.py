#####################################################################################################################
#
#
# Purpose: Proceso encargado de división de train/test y filtrado de valores para ILT
# Creator: Pablo Beltramone
#
#   Inputs:
#       Analitical record:
#
#   Outputs:
#       DF train Test
#
#  Notes: NA
#######################################################################################################################

#PATH_REPO = 'C:/Users/E0662122/Repo/MiM_Analytics_Tesis/Tesis/performance_index/'
PATH_REPO = 'C:/Repo/MiM_Analytics_Tesis/Tesis/performance_index/'

import pandas as pd
import json
import sys
import joblib
sys.path.insert(0, PATH_REPO)
import PI_Preprocessing
import PI_FactorAnalysis
import importlib

importlib.reload(PI_Preprocessing)
importlib.reload(PI_FactorAnalysis)

dict_cols = {"player_cols": ['player_id', 'player_name', 'player_preferred_position', 'player_preferred_number', 'player_minutes'],

             "F": ['np_goals_p90', 'shots_p90', 'shooting_accuracy', 'goal_conversion_np', 'passing_accuracy',
                   'assists_p90', 'key_passes_p90', 'dribbles_p90', 'dribbles_success_ratio', 'total_tackles_p90',
                   'avg_team_position', 'avg_league_cov'],

             "M": ['wavg_player_rating', 'passes_p90', 'passing_accuracy', 'key_passes_p90', 'scoring_contribution',
                   'dribbles_success_ratio', 'fouls_drawn_p90', 'fouls_committed_p90', 'dribbles_past_p90',
                   'total_tackles_p90', 'tackles_p90', 'interceptions_p90', 'avg_team_position', 'avg_league_cov'],

             "D": ['wavg_player_rating', 'passes_p90', 'passing_accuracy', 'key_passes_p90', 'fouls_drawn_p90',
                   'fouls_committed_p90', 'dribbles_past_p90', 'duels_p90', 'duels_success_ratio', 'tackles_p90',
                   'blocks_p90', 'interceptions_p90', 'avg_team_position', 'avg_league_cov'],

             "G": ['wavg_player_rating', 'saves_p90', 'goals_conceded_p90', 'passes_p90', 'passing_accuracy',
                   'fouls_drawn_p90', 'fouls_committed_p90', 'duels_p90', 'duels_success_ratio', 'tackles_p90',
                   'interceptions_p90', 'penalty_committed_p90', 'avg_team_position', 'avg_league_cov']
             }

## Load files
f = open(PATH_REPO+"perfindex_config.json", "r")
inputs = json.loads(f.read())

AR = pd.read_csv(inputs['data_sources']['master_path']+inputs['data_sources']['AR'], encoding='utf-8', decimal='.', sep='|')
rating_correction = pd.read_csv(inputs['data_sources']['master_path']+inputs['data_sources']['rating_correction'], encoding='utf-8', decimal='.', sep='|')

## Preprocessing
df = PI_Preprocessing.filter_and_data_engineering(AR, rating_correction, correct_rating=True)
df_gk, df_df, df_mf, df_fw, dict_scalers = PI_Preprocessing.normalize_by_position(df, dict_cols, scaler='Robust') # [Robust, Standard, MinMax]

## Create Index
dict_weights = {}
# Forwards
df_fw, dict_weights = PI_FactorAnalysis.create_index(df_fw, dict_cols['F'], dict_weights, position='F', factors=4,
                                                     factors_method='principal', factors_rotation='varimax')
# Midfielders
df_mf, dict_weights = PI_FactorAnalysis.create_index(df_mf, dict_cols['M'], dict_weights, position='M', factors=4,
                                                     factors_method='principal', factors_rotation='varimax')
# Defenders
df_df, dict_weights = PI_FactorAnalysis.create_index(df_df, dict_cols['D'], dict_weights, position='D', factors=4,
                                                     factors_method='principal', factors_rotation='varimax')
# Goalkeepers
df_gk, dict_weights = PI_FactorAnalysis.create_index(df_gk, dict_cols['G'], dict_weights, position='G', factors=5,
                                                     factors_method='principal', factors_rotation='varimax')

## Export
dict_perf_index = {'cols': dict_cols, 'scalers': dict_scalers, 'index_weights': dict_weights}
joblib.dump(dict_perf_index, PATH_REPO+'20211118_PerformanceIndexObject.pkl')
