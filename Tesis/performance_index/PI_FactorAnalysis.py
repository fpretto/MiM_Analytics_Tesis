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

    scaler = MinMaxScaler()
    scaler = scaler.fit(pd.DataFrame(df_perf_idx['Perf_Index']))
    df_perf_idx['Perf_Index_scaled'] = scaler.transform(pd.DataFrame(df_perf_idx['Perf_Index']))
    dict_weights[position] = dict_weights_position
    dict_weights["index_scaler"] = scaler

    return df_perf_idx, dict_weights

def score_index(df, dict_perf_index):

    df_indexes = pd.DataFrame()

    for position in ['F', 'M', 'D', 'G']:

        # Filter and Scale
        df_index = df[df['player_preferred_position'] == position].reset_index(drop=True)
        df_index = pd.DataFrame(dict_perf_index['scalers'][position].transform(df_index[dict_perf_index['cols'][position]]))
        df_index.columns = dict_perf_index['cols'][position]

        # Calculate Performance Index
        for id_factor in dict_perf_index['index_weights'][position].keys():
            if id_factor != 'Weights':
                df_index[id_factor] = np.sum(df_index[dict_perf_index['cols'][position]]*dict_perf_index['index_weights'][position][id_factor], axis=1)
            else:
                df_index['Perf_Index'] = np.sum(df_index[dict_perf_index['cols'][position]]*dict_perf_index['index_weights'][position][id_factor], axis=1)

        df_index['Perf_Index_scaled'] = dict_perf_index['index_weights']['index_scaler'].transform(pd.DataFrame(df_index['Perf_Index']))

        # Append results
        df_indexes = df_indexes.append(pd.concat([df[df['player_preferred_position']==position].reset_index(drop=True),
                                                  df_index['Perf_Index_scaled']], axis=1)).reset_index(drop=True)

    return df_indexes

def sensitivity_analysis(df, dict_perf_index, path):

    dict_sensitivity_plots = {}

    for position in ['F', 'M', 'D', 'G']:

        df_index = df[df['player_preferred_position'] == position].reset_index(drop=True)

        # Extract steps values
        min_list = []
        half_step_min = []
        mean_list = []
        half_step_max = []
        max_list = []

        for col in dict_perf_index['cols'][position]:
            min_list.append(df_index[col].min())
            half_step_min.append((df_index[col].mean()+df_index[col].min())/2)
            mean_list.append(df_index[col].mean())
            half_step_max.append((df_index[col].max()+df_index[col].mean())/2)
            max_list.append(df_index[col].max())

        df_sensitivity = pd.DataFrame([min_list, half_step_min, mean_list, half_step_max, max_list],
                                      index=['Min', 'Half_Min', 'Mean', 'Half_Max', 'Max'],
                                      columns=dict_perf_index['cols'][position])

        # Calculate index variations
        dict_all = {}
        dict_step = {}

        for col in df_sensitivity.columns:
            for step in ['Min', 'Half_Min', 'Mean', 'Half_Max', 'Max']:
                list_vars = list(dict_perf_index['cols'][position])
                list_vars.remove(col)
                df_iter = pd.DataFrame(pd.concat([pd.Series(df_sensitivity.loc[step, col], name=col),
                                                  df_sensitivity.loc['Mean', list_vars]])).transpose()
                df_iter.columns = df_sensitivity.columns
                df_iter['Perf_Index'] = np.sum(df_iter[dict_perf_index['cols'][position]]**dict_perf_index['index_weights'][position]['Weights'], axis=1)
                df_iter['Perf_Index_scaled'] = dict_perf_index['index_weights']['index_scaler'].transform(pd.DataFrame(df_iter['Perf_Index']))
                dict_step[step] = df_iter.loc[0, 'Perf_Index_scaled']
                dict_all[col] = dict(dict_step)

        df_scored_steps = pd.DataFrame.from_dict(dict_all)

        # Calculate percentual variation
        for col in df_scored_steps.columns:
            df_scored_steps[col] = (df_scored_steps[col]/df_scored_steps.loc['Mean', col]-1)*100

        # Plot variations
        df_plot = df_scored_steps.transpose()
        df_plot['Min'] = df_plot['Min']-df_plot['Half_Min']
        df_plot['Max'] = df_plot['Max']-df_plot['Half_Max']
        plot_cols = ['Half_Min', 'Min', 'Half_Max', 'Max']

        fig, ax = plt.subplots(figsize=(8, 8))
        df_plot[plot_cols].plot(kind='barh', stacked=True, ax=ax, color=['lightcoral', 'indianred', 'mediumseagreen', 'forestgreen'])
        ax.set_xlabel('Variation in Performance Index (%)')
        ax.legend(['-1/2 Step', '-1 Step', '+1/2 Step', '+1 Step'])
        ax.xaxis.grid(linestyle='--')
        fig.savefig(path+'SensitivityAnalysis_' + position + '.png', bbox_inches='tight', pad_inches=1)

