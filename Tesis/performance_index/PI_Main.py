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

import pandas as pd
import numpy as np
import json
import PI_Preprocessing

# Load files
f = open("ConfigFile.json", "r")
inputs = json.loads(f.read())

AR = pd.read_csv(inputs['master_path']+inputs['AR'], encoding='utf-8', decimal='.', sep='|')
rating_correction = pd.read_csv(inputs['master_path']+inputs['rating_correction'], encoding='utf-8', decimal='.', sep='|')

