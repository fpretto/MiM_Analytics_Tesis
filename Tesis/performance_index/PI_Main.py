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
import numpy as np
import json
import sys
sys.path.insert(0, PATH_REPO)
import PI_Preprocessing
import PI_FactorAnalysis
import importlib

importlib.reload(PI_Preprocessing)
importlib.reload(PI_FactorAnalysis)

dict_cols = {"player_cols": ['player_id', 'player_name', 'player_preferred_position', 'player_preferred_number', 'player_minutes'],

             "fw_cols": ['np_goals_p90', 'shots_p90', 'shooting_accuracy', 'goal_conversion_np', 'passing_accuracy',
                         'assists_p90', 'key_passes_p90', 'dribbles_p90', 'dribbles_success_ratio', 'total_tackles_p90'],

             "mf_cols": ['wavg_player_rating', 'passes_p90', 'passing_accuracy', 'key_passes_p90', 'scoring_contribution',
                         'dribbles_success_ratio', 'fouls_drawn_p90', 'fouls_committed_p90', 'dribbles_past_p90',
                         'total_tackles_p90', 'tackles_p90', 'interceptions_p90'],

             "df_cols": ['wavg_player_rating', 'passes_p90', 'passing_accuracy', 'key_passes_p90', 'fouls_drawn_p90',
                         'fouls_committed_p90', 'dribbles_past_p90', 'duels_p90', 'duels_success_ratio', 'tackles_p90',
                         'blocks_p90', 'interceptions_p90'],

             "gk_cols": ['wavg_player_rating', 'saves_p90', 'goals_conceded_p90', 'passes_p90', 'passing_accuracy',
                         'fouls_drawn_p90', 'fouls_committed_p90', 'duels_p90', 'duels_success_ratio', 'tackles_p90',
                         'interceptions_p90', 'penalty_committed_p90']
             }

# Load files
f = open(PATH_REPO+"ConfigFile.json", "r")
inputs = json.loads(f.read())

AR = pd.read_csv(inputs['data_sources']['master_path']+inputs['data_sources']['AR'], encoding='utf-8', decimal='.', sep='|')
rating_correction = pd.read_csv(inputs['data_sources']['master_path']+inputs['data_sources']['rating_correction'], encoding='utf-8', decimal='.', sep='|')

# Preprocessing
df = PI_Preprocessing.filter_and_data_engineering(AR, rating_correction)
df_gk, df_df, df_mf, df_fw = PI_Preprocessing.normalize_by_position(df, dict_cols, scaler='Robust') # [Robust, Standard, MinMax]

# Create Index
dict_weights = {}
df_fw, dict_weights = PI_FactorAnalysis.create_index(df_fw, dict_cols['fw_cols'], dict_weights, position='F', factors=4,
                                                     factors_method='principal', factors_rotation='varimax')

dict_weights
df_fw.sort_values('Perf_Index_scaled', ascending=False)