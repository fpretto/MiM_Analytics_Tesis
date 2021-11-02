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

# Load files
f = open(PATH_REPO+"ConfigFile.json", "r")
inputs = json.loads(f.read())

AR_score = pd.read_csv(inputs['data_sources']['master_path']+inputs['data_sources']['AR_score'],
                       encoding='utf-8', decimal='.', sep='|')
dict_perf_index = joblib.load(PATH_REPO+'PerformanceIndexObject.pkl')

# Preprocessing
df = PI_Preprocessing.filter_and_data_engineering(AR_score, rating_correction=None, correct_rating=False)

# Scoring
df_indexes = PI_FactorAnalysis.score_index(df, dict_perf_index)

df_indexes.to_csv('C:/Repo/MiM_Analytics_Tesis/Tesis/DASH_PlayersScored_20211101.csv', sep='|', decimal='.')