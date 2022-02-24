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
PATH_REPO = 'C:/Repo/MiM_Analytics_Tesis/Tesis/'

import pandas as pd
import json
import sys
import joblib
sys.path.insert(0, PATH_REPO)
import PI_Preprocessing
import PI_FactorAnalysis
import importlib
from sqlalchemy import create_engine

importlib.reload(PI_Preprocessing)
importlib.reload(PI_FactorAnalysis)

# Load files
f = open(PATH_REPO+"performance_index/perfindex_config.json", "r")
inputs = json.loads(f.read())

AR_score = pd.read_csv(PATH_REPO+'AR_scoring_20220210.csv', encoding='utf-8', decimal='.', sep='|')
dict_perf_index = joblib.load(PATH_REPO+'performance_index/20220210_PerformanceIndexObject.pkl')

# Preprocessing
df = PI_Preprocessing.filter_and_data_engineering(AR_score, rating_correction=None, correct_rating=False)

# Scoring
df_indexes = PI_FactorAnalysis.score_index(df, dict_perf_index)

df_indexes.to_csv('C:/Repo/MiM_Analytics_Tesis/Tesis/DASH_PlayersScored_20220210.csv', sep='|', decimal='.')