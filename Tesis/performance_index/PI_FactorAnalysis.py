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

PATH_REPO = 'C:/Repo/MiM_Analytics_Tesis/Tesis/performance_index/'

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from factor_analyzer import FactorAnalyzer
import pingouin as pg

def get_factors(x, factors, method='principal', rotation='varimax', thresh_c_alpha=0.5):
    fa = FactorAnalyzer(factors, method=method, rotation=rotation)
    fa.fit(x)
    # Get loadings
    loads = fa.loadings_
    # Get Variance
    var = pd.DataFrame(fa.get_factor_variance(), index=['Variance', 'Proportional Variance (%)', 'Cummulative (%)'],
                       columns=['Factor {}'.format(fact+1) for fact in range(factors)])
    # Get Communalities
    communalities = pd.DataFrame(fa.get_communalities(), columns=['Communalities'], index=x.columns)
    # Calculate Normalized Squared Factor Loadings
    variances = fa.get_factor_variance()[0]
    sq_norm_variances = (loads**2)/variances
    variances_pct = [variances[i]/sum(variances) for i in range(len(variances))]
    # Consolidate
    df_variances_pct = pd.DataFrame(variances_pct, index=['Factor {}'.format(fact+1) for fact in range(factors)],
                                    columns=['Expl.Var/Tot (%)']).transpose()
    df_sq_factors = pd.DataFrame(sq_norm_variances, index=x.columns, columns=['Sq Norm Factor {}'.format(fact+1) for
                                                                              fact in range(factors)])
    df_factors = pd.DataFrame(loads, index=x.columns, columns=['Factor {}'.format(fact+1) for fact in range(factors)])
    df_weights = pd.DataFrame(np.sum(sq_norm_variances*variances_pct, axis=1), index=x.columns, columns=['PC_Weight'])
    df_factors_var = pd.concat([pd.concat([df_factors, var, df_variances_pct]),
                                communalities, df_sq_factors, df_weights], axis=1)

    # Calculate Cronbach's coefficient alpha
    df_c_alpha = get_cronbach_alpha(x, df_factors_var, factors, threshold=thresh_c_alpha)

    return df_factors_var, df_c_alpha

def get_cronbach_alpha(df, df_factors, factors, threshold=0.5):
    list_c_alpha = []
    for factor in range(factors):
        cols_factor = df_factors[(~df_factors.index.isin(['Variance', 'Proportional Variance (%)', 'Cummulative (%)',
                                                          'Expl.Var/Tot (%)'])) &
                                 (df_factors[f'Factor {factor+1}'] >= threshold)].index
        try:
            list_c_alpha.append([f'Sq Norm Factor {factor+1}',
                                 pg.cronbach_alpha(df[cols_factor])[0], # C-Alpha
                                 pg.cronbach_alpha(df[cols_factor])[1]]) # Confidence Interval
        except:
            pass

    return pd.DataFrame(list_c_alpha, columns=['Factor', 'C-Alpha', 'Conf. Interval'])

def get_screeplot(df, cols):
    x = df[cols]
    fa = FactorAnalyzer()
    fa.fit(x, 10)
    #Get Eigen values and plot them
    ev, v = fa.get_eigenvalues()
    scree_plot = plt.plot(range(1, x.shape[1]+1), ev, marker='o')

    return scree_plot

#factors=4
#factors_method='principal'
#factors_rotation='varimax'
#cols=dict_cols['fw_cols']
#x=df_fw[dict_cols['fw_cols']]

def create_index(df, cols, dict_weights, position, factors, factors_method='principal', factors_rotation='varimax'):

    from sklearn.preprocessing import MinMaxScaler

    df_factors = get_factors(df[cols], factors=factors, method=factors_method, rotation=factors_rotation)[0]
    df_cronbach = get_factors(df[cols], factors=factors, method=factors_method, rotation=factors_rotation)[1]

    dict_weights_position = {}
    for id_factor in range(factors+1, 0, -1):
        if id_factor > 1:
            dict_weights_position["Factor "+str(factors-id_factor+2)] = np.array(
                    df_factors.iloc[:-(len(df_factors)-len(cols)), -id_factor])
        else:
            dict_weights_position["Weights"] = np.array(
                    df_factors.iloc[:-(len(df_factors)-len(cols)), -id_factor])

    df_perf_idx = df[df['player_preferred_position'] == position].set_index(['player_id', 'player_name'])[cols]

    for id_factor in dict_weights_position.keys():
        if id_factor != 'Weights':
            df_perf_idx[id_factor] = np.sum(df_perf_idx[cols]*dict_weights_position[id_factor], axis=1)
        else:
            df_perf_idx['Perf_Index'] = np.sum(df_perf_idx[cols]*dict_weights_position[id_factor], axis=1)

    df_perf_idx['Perf_Index_scaled'] = MinMaxScaler().fit_transform(pd.DataFrame(df_perf_idx['Perf_Index']))
    dict_weights[position] = dict_weights_position

    return df_perf_idx, dict_weights
