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

PATH_REPO = 'C:/Users/E0662122/Repo/MiM_Analytics_Tesis/Tesis/performance_index/'

import pandas as pd
import numpy as np
import json
import sys
sys.path.insert(0, PATH_REPO)
import PI_Preprocessing
import importlib

importlib.reload(PI_Preprocessing)

# Load files
f = open(PATH_REPO+"ConfigFile.json", "r")
inputs = json.loads(f.read())

AR = pd.read_csv(inputs['data_sources']['master_path']+inputs['data_sources']['AR'], encoding='utf-8', decimal='.', sep='|')
rating_correction = pd.read_csv(inputs['data_sources']['master_path']+inputs['data_sources']['rating_correction'], encoding='utf-8', decimal='.', sep='|')

df = PI_Preprocessing.filter_and_data_engineering(AR, rating_correction)

df_gk, df_df, df_mf, df_fw = PI_Preprocessing.normalize_by_position(df, scaler='Robust') # [Robust, Standard, MinMax]
