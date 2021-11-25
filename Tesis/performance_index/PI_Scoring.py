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
from sqlalchemy import create_engine

importlib.reload(PI_Preprocessing)
importlib.reload(PI_FactorAnalysis)

# Load files
f = open(PATH_REPO+"perfindex_config.json", "r")
inputs = json.loads(f.read())

uri = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
        inputs['PostgreSQL']['username'], inputs['PostgreSQL']['password'], inputs['PostgreSQL']['host'],
        inputs['PostgreSQL']['port'], inputs['PostgreSQL']['database'])

engine = create_engine(uri)
conn = engine.raw_connection()
cursor = conn.cursor()

AR_score = pd.read_sql_query("SELECT * FROM fdm.dash_ft_abt_season_player;", conn)
dict_perf_index = joblib.load(PATH_REPO+'20211118_PerformanceIndexObject.pkl')

# Preprocessing
df = PI_Preprocessing.filter_and_data_engineering(AR_score, rating_correction=None, correct_rating=False)

# Scoring
df_indexes = PI_FactorAnalysis.score_index(df, dict_perf_index)

df_indexes.to_csv('C:/Repo/MiM_Analytics_Tesis/Tesis/DASH_PlayersScored_20211118.csv', sep='|', decimal='.')