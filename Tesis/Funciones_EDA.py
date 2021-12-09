import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

######################################################################
# GRAFICOS
######################################################################

# Gráficos barras
def pct_bar_labels():
    plt.ylabel('Relative Frequency (%)')
    plt.xticks(rotation=0)
    plt.yticks([])
    # Set individual bar lebels in proportional scale
    for x in ax1.patches:
        ax1.annotate(str(x.get_height()) + '%',
                     (x.get_x() + x.get_width() / 2., x.get_height()), ha='center', va='center', xytext=(0, 7),
                     textcoords='offset points', fontsize=14, color='black')


def absolute_and_relative_freq(variable):
    global ax1
    # Dataframe of absolute and relative frequency
    absolute_frequency = variable.value_counts()
    # Will be multiplied by 100 and rounded to 2 decimal points for percentage
    relative_frequency = round(variable.value_counts(normalize=True) * 100, 2)
    df = pd.DataFrame({'Absolute Frequency': absolute_frequency, 'Relative Frequency(%)': relative_frequency})
    ax1 = relative_frequency.plot.bar(figsize=(10, 8))
    plt.title('Relative Frequency of %s' % variable.name)
    pct_bar_labels()
    plt.show()
    return df


def absolute_and_relative_amt(df, variable, var_sum):
    global ax1

    # Dataframe of absolute and relative frequency
    absolute_frequency = df.groupby(variable, as_index=False)[var_sum].sum()
    absolute_frequency['perc'] = round((absolute_frequency[var_sum] / df[var_sum].sum()) * 100, 2)
    absolute_frequency.set_index(variable)

    # Will be multiplied by 100 and rounded to 2 decimal points for percentage
    relative_frequency = absolute_frequency[[variable, 'perc']]
    df_final = pd.merge(absolute_frequency, relative_frequency, how='left', on=variable)

    ax1 = relative_frequency.sort_values(by='perc', ascending=False).plot.bar(x=variable, y='perc', figsize=(10, 8))
    ax1.set_facecolor('xkcd:white')
    pct_bar_labels()
    plt.show()
    return df_final.sort_values(by='perc_x', ascending=False)

# Graficos barra y linea

def plot_barra(df, x_var, x_name, y_var, y_name, rotation = 90):
    # Configuracion del plot
    fig, ax1 = plt.subplots(figsize=(15, 5))
    font = {'family': 'sans-serif',
            'weight': 'bold',
            'size': 8}
    plt.rc('font', **font)

    # Titulo del grafico
    title_font = {'family': 'sans-serif',
                  'fontsize': 20,
                  'fontweight': 'normal',
                  'verticalalignment': 'baseline',
                  'horizontalalignment': 'center'}

    plt.title(label=y_name + ' por ' + x_name, fontdict=title_font)

    # Configuracion eje X
    ax1.set_xlabel(x_name, size=20)
    ax1.tick_params(axis='x', labelsize=12, labelrotation=rotation)

    # Configuracion eje Y Primario
    ax1.set_ylabel(y_name, color='steelblue', size=20)
    ax1.bar(df[x_var], df[y_var], color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue', labelsize=12)

    # Ploteo
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

# Graficos barra y linea

def plot_barra_freq(df, x_var, x_name, y1_var, y1_name, y2_var, y2_name, rotation = 90):
    # Configuracion del plot
    fig, ax1 = plt.subplots(figsize=(15, 5))
    font = {'family': 'sans-serif',
            'weight': 'bold',
            'size': 8}
    plt.rc('font', **font)

    # Titulo del grafico
    title_font = {'family': 'sans-serif',
                  'fontsize': 20,
                  'fontweight': 'normal',
                  'verticalalignment': 'baseline',
                  'horizontalalignment': 'center'}

    plt.title(label=y1_name + ' y ' + y2_name + ' por ' + x_name, fontdict=title_font)

    # Configuracion eje X
    ax1.set_xlabel(x_name, size=20)
    ax1.tick_params(axis='x', labelsize=12, labelrotation=rotation)

    # Configuracion eje Y Primario
    ax1.set_ylabel(y1_name, color='steelblue', size=20)
    ax1.bar(df[x_var], df[y1_var], color='steelblue')
    ax1.tick_params(axis='y', labelcolor='steelblue', labelsize=12)

    # Configuracion eje Y Secundario
    ax2 = ax1.twinx()
    ax2.set_ylabel(y2_name, color='darkblue', size=20)  # we already handled the x-label with ax1

    ax2.plot(df[x_var], df[y2_var], color='darkblue', linewidth=3.0)
    ax2.tick_params(axis='y', labelcolor='darkblue', labelsize=12)

    # Ploteo
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

def plot_boxplot(df, x_var, y_var, hue_var = None, fig_size=(15,6), y_ticks = None):

    if hue_var == None:
        df_boxplot = df[[x_var, y_var]][df[y_var]>0]
    else:
        df_boxplot = df[[x_var, hue_var, y_var]][df[y_var]>0]

    # Configuracion del plot
    fig, ax = plt.subplots(figsize=fig_size)

    # Titulo del grafico
    title_font = {'family': 'sans-serif',
                  'fontsize': 20,
                  'fontweight': 'normal',
                  'verticalalignment': 'baseline',
                  'horizontalalignment': 'center'}

    if hue_var == None:
        plt.title(label='Distribución de ' + y_var + ' por ' + x_var, fontdict=title_font)
    else:
        plt.title(label = 'Distribución de ' + y_var + ' por ' + hue_var, fontdict=title_font)

    # Configuracion eje X
    ax.set_xlabel(x_var, size=20)
    ax.tick_params(axis='x', labelsize=15)

    # Configuracion eje Y Primario
    ax.set_ylabel(ylabel = y_var, size=20)
    if type(y_ticks) == np.ndarray:
    	plt.yticks(y_ticks)
    ax.tick_params(axis='y', labelsize=15)
    sns.boxplot(x = x_var, y = y_var, hue = hue_var,data = df_boxplot, palette = "Set1")


def plot_histogram(df, x_var, hue_var = None, greater_than = None, density = False, log = False):
    """
    Grafica un histograma dada una variable continua

    Parameters:
    df: Dataframe con la variable a graficar
    x_var: variable continua a graficar
    hue_var: variable categorica a partir de la cual subdividir el grafico
    greater_than: valor a partir del cual filtrar el dataset por la variable x_var

    Returns:
    Histograma
    """
    # Generacion del dataset para graficar
    if greater_than == None:
        df_hist = df.copy()
    else:
        df_hist = df[df[x_var] > greater_than].fillna(0)

    # Generacion histograma
    if hue_var == None:
        f = plt.hist(df_hist[x_var].fillna(0), bins = 50, density = density, log = log)
    else:
        f = sns.FacetGrid(df_hist, col=hue_var, col_wrap=4, height=6)
        f = f.map(plt.hist, x_var, bins = 50, density = density, log = log)

    # Ploteo
    plt.show()

def outliers(variable,i):
    # Calculate 1st, 3rd quartiles and iqr.
    q1, q3 = variable.quantile(0.25), variable.quantile(0.75)
    iqr = q3 - q1
    
    # Calculate lower fence and upper fence for outliers
    l_fence, u_fence = q1 - 1.5*iqr , q3 + 1.5*iqr   # Any values less than l_fence and greater than u_fence are outliers.
    
    # Observations that are outliers
    outliers = variable[(variable<l_fence) | (variable>u_fence)]
    print('Total Outliers of', variable.name,i, ':', outliers.count())
    
    # Drop obsevations that are outliers
    filtered = variable.drop(outliers.index, axis = 0)

    # Create subplots
    fig, (ax1, ax2) = plt.subplots(2,1)
    
    # Gives space between two subplots
    fig.subplots_adjust(hspace = 1) 
    
    # Plot variable with outliers
    variable.plot.box(vert = False, color = 'coral', grid = False, ax = ax1, title = 'Distribution with Outliers for %s' %variable.name)

    # Plot variable without outliers
    filtered.plot.box(vert = False, color = 'coral', grid = False, ax = ax2, title = 'Distribution without Outliers for %s' %variable.name)

## Distribucion 
# Severidad
def distribucion_sev(var, var_nombre, df, target_cantidad, target_monto, rot = False):
    df_agr = df.groupby([var], as_index=False)[[target_cantidad, target_monto]].mean()
    df_agr['costo_stro'] = df_agr[target_monto] / df_agr[target_cantidad]
    df_agr.sort_values(by='costo_stro', inplace = True)

    sns.set(font_scale=2)
    sns.set(rc={'figure.figsize':(17,10)})
    if rot == False:
        plot = sns.barplot(x=var, 
                           y='costo_stro', 
                           data=df_agr, 
                           palette = 'Set3').set_title("Media costo por siniestro {costo} de acuerdo a {var}".format(costo=tipo_costo, var=var))
    else:
        print("Media costo por siniestro {costo} de acuerdo a {var}".format(costo=tipo_costo, var=var))
        plot = sns.barplot(x=var, 
                   y='costo_stro', 
                   data=df_agr, 
                   palette = 'Set3')
        for item in plot.get_xticklabels():
            item.set_rotation(90)
        
    plt.xlabel(var_nombre)
    plt.ylabel("Costo por siniestro")
    plt.show()

# Frecuencia
def distribucion_frec(var, var_nombre, df, target_cantidad):
    df_agr = df.groupby([var], as_index=False)[target_cantidad, 'capitas_12m'].sum()
    df_agr['frec'] = df_agr[target_cantidad] / df_agr['capitas_12m']

    sns.set(font_scale=2)
    sns.set(rc={'figure.figsize':(17,10)})
    if rot == False:
        plot = sns.barplot(x=var, 
                           y='costo_stro', 
                           data=df_agr, 
                           palette = 'Set3').set_title("Media costo por siniestro {costo} de acuerdo a {var}".format(costo=tipo_costo, var=var))
    else:
        print("Media costo por siniestro {costo} de acuerdo a {var}".format(costo=tipo_costo, var=var))
        plot = sns.barplot(x=var, 
                   y='costo_stro', 
                   data=df_agr, 
                   palette = 'Set3')
        for item in plot.get_xticklabels():
            item.set_rotation(90)
            
    plt.xlabel(var_nombre)
    plt.ylabel("Frecuencia")
    plt.show()
    

## Evolucion años 
# Severidad

def anios_sev(var, var_nombre, df, target_cantidad, target_monto):
    df_agr = df.groupby([var, 'anio_renovacion'], as_index=False)[target_cantidad, target_monto].sum()
    df_agr['costo_stro'] = df_agr[target_monto] / df_agr[target_cantidad]

    print('Costo por siniestro de acuerdo a {}'.format(var_nombre))
    g = sns.FacetGrid(df_agr, col="anio_renovacion", height=7)
    g = g.map(sns.barplot, var, "costo_stro", palette="Set2", order=df_agr[var].unique())
    g.axes[0,0].set_xlabel(var_nombre)
    g.axes[0,1].set_xlabel(var_nombre)
    g.axes[0,2].set_xlabel(var_nombre)
    g.axes[0,0].set_ylabel('Costo por siniestro')
    plt.show()
    
# Frecuencia 
def anios_frec(var, var_nombre, df, target_cantidad):
    df_agr = df.groupby(['anio_renovacion', var], as_index=False)[target_cantidad, 'capitas_12m'].sum()
    df_agr['frec'] = df_agr[target_cantidad] / df_agr['capitas_12m']

    print('Frecuencia por siniestro de acuerdo a {}'.format(var_nombre))
    g = sns.FacetGrid(df_agr, col="anio_renovacion", height=7)
    g = g.map(sns.barplot, var, "frec", palette="Set3", order=df_agr[var].unique())
    g.axes[0,0].set_xlabel(var_nombre)
    g.axes[0,1].set_xlabel(var_nombre)
    g.axes[0,2].set_xlabel(var_nombre)
    g.axes[0,0].set_ylabel('Frecuencia por siniestro')
    plt.show()
    
######################################################################
# VALIDACION DE DISTRIBUCIONES
######################################################################

def validate_homogeneidad(df, var_analisis, var_temporal, var_muestra1, var_muestra2):
    from scipy import stats
    #Muestras
    muestra1 = df[df[var_temporal] == var_muestra1][var_analisis].reset_index(drop=True).dropna()
    muestra2 = df[df[var_temporal] == var_muestra2][var_analisis].reset_index(drop=True).dropna()

    #Homocedasticidad
    bartlett = stats.bartlett(muestra1, muestra2)
    levene = stats.levene(muestra1, muestra2)

    #Homogeneidad
    kruskal_wallis = stats.kruskal(muestra1, muestra2)
    t_welch = stats.ttest_ind(muestra1, muestra2, equal_var=False)
    anova = stats.f_oneway(muestra1, muestra2)

    #Indice
    arrays = [['Homocedasticidad', 'Homocedasticidad', 'Homogeneidad', 'Homogeneidad', 'Homogeneidad'],
            ['Bartlett', 'Levene', 'Kruskal-Wallis', 't-Welch', 'Anova']]
    tuples = list(zip(*arrays))
    index = pd.MultiIndex.from_tuples(tuples, names=['Categoría','Test'])

    # Resultados
    df_stats = pd.concat([pd.Series(bartlett),pd.Series(levene),pd.Series(kruskal_wallis),pd.Series(t_welch),pd.Series(anova)],axis=1)
    df_stats.columns = ['Bartlett', 'Levene', 'Kruskal-Wallis', 't-Welch', 'Anova']
    df_stats.index = ['t-statistic', 'p-value']

    return df_stats.transpose().set_index(index)

# Create models from data
def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    import warnings
    import numpy as np
    import pandas as pd
    import scipy.stats as st
    import statsmodels as sm
    import matplotlib
    import matplotlib.pyplot as plt

    matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
    matplotlib.style.use('ggplot')

    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check
#    DISTRIBUTIONS = [
#         st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
#         st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
#         st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
#         st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
#         st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
#         st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
#         st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
#         st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
#         st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
#         st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
#     ]
    # Distribuciones en GLM
    DISTRIBUTIONS = [st.gamma, st.gengamma, st.norm, st.invgauss,st.loggamma,st.expon]

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    end
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params)

def make_pdf(dist, params, size=10000):
    """Generate distributions's Probability Distribution Function """
    import warnings
    import numpy as np
    import pandas as pd
    import scipy.stats as st
    import statsmodels as sm
    import matplotlib
    import matplotlib.pyplot as plt

    matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
    matplotlib.style.use('ggplot')

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf

######################################################################
# OUTLIERS
######################################################################

def tratamiento_outliers(df, x_var, quantile_min , quantile_max, desvios):
    # Calculate 1st, 3rd quartiles and iqr.
    q1 = df[df[x_var] > 0][x_var].quantile(quantile_min)
    q3 = df[df[x_var] > 0][x_var].quantile(quantile_max)
    iqr = q3 - q1

    # Calculate lower fence and upper fence for outliers
    l_fence, u_fence = q1 - desvios * iqr, q3 + desvios * iqr  # Any values less than l_fence and greater than u_fence are outliers.

    # Observations that are outliers
    outliers = df[x_var][(df[x_var] < l_fence) | (df[x_var] > u_fence)]

    # Drop obsevations that are outliers
    df_filtered = df.drop(outliers.index, axis=0)

    print('Outliers removidos:', len(df) - len(df_filtered), '(', round((1 - len(df_filtered) / len(df)) * 100, 2), '%)')

    return df_filtered


######################################################################
# CLUSTERING
######################################################################

def k(df):
    from sklearn.cluster import KMeans
    from scipy.spatial.distance import cdist
    import numpy as np

    ### _Encuentro el K_
    clusters = range(1, 10)
    meandist = []

    # loop through each cluster and fit the model to the train set
    # generate the predicted cluster assingment and append the mean distance my taking the sum divided by the shape
    for k in clusters:
        model = KMeans(n_clusters=k, max_iter=300, tol=0.001).fit(df)
        meandist.append(sum(np.min(cdist(df, model.cluster_centers_, 'euclidean'), axis=1)) / df.shape[0])

    plt.figure()
    plt.plot(clusters, meandist)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average distance')
    plt.title('Selecting k with the Elbow Method')  # pick the fewest number of clusters that reduces the squared distance
    plt.show()


def cluster(df, n):
    from sklearn.cluster import KMeans
    model = KMeans(n_clusters = n)
    kmeans = model.fit(df)  # has cluster assingments based on using 3 clusters
    clusassign = model.predict(df)
    return clusassign

######################################################################
# GLM
######################################################################

def results_summary_to_dataframe(results):
    '''This takes the result of an statsmodel results table and transforms it into a dataframe'''
    pvals = round(results.pvalues,2)
    coeff = results.params#round(results.params,2)
    conf_lower = round(results.conf_int()[0],2)
    conf_higher = round(results.conf_int()[1],2)
    results_df = pd.DataFrame({"pvals":pvals,
                               "coeff":coeff,
                               "conf_lower":conf_lower,
                               "conf_higher":conf_higher
                                })
    #Reordering...
    results_df = results_df[["coeff","pvals","conf_lower","conf_higher"]]
    return results_df

######################################################################
# MODELOS
######################################################################
def Gini(y_true, y_pred):
    import numpy as np
    # check and get number of samples
    assert y_true.shape == y_pred.shape
    n_samples = y_true.shape[0]

    # sort rows on prediction column
    # (from largest to smallest)
    arr = np.array([y_true, y_pred]).transpose()
    true_order = arr[arr[:, 0].argsort()][::-1, 0]
    pred_order = arr[arr[:, 1].argsort()][::-1, 0]

    # get Lorenz curves
    L_true = np.cumsum(true_order) / np.sum(true_order)
    L_pred = np.cumsum(pred_order) / np.sum(pred_order)
    L_ones = np.linspace(0, 1, n_samples)

    # get Gini coefficients (area between curves)
    G_true = np.sum(L_ones - L_true)
    G_pred = np.sum(L_ones - L_pred)

    # normalize to true Gini coefficient
    return G_pred / G_true

def scale_factor(y_pred, y_true):
    from sklearn.utils import resample
    import numpy as np
    from matplotlib import pyplot

    # Parametros Bootstrap
    n_iterations = 100
    n_size = int(len(y_pred) * 0.50)
    df_scalefactor = pd.DataFrame(y_pred, y_true).reset_index()
    df_scalefactor.columns = ['y_pred', 'y_true']
    # Bootstrap
    stats = list()
    for i in range(n_iterations):
        muestra = resample(df_scalefactor, n_samples=n_size)
        scale_factor = muestra['y_pred'].sum() / muestra['y_true'].sum()
        stats.append(scale_factor)

    return np.round(pd.Series(stats).mean(), 3)

def train_test(model, X_train, X_test, y_train, y_test, mape=False, prt=False, feature_importances=False, msle=False):
    from scipy.stats import ks_2samp
    import numpy as np
    from sklearn import metrics
    import math as math

    model_name = str(model.__class__.__name__)
    mdl = model.fit(X_train, y_train)

    y_pred_train = mdl.predict(X_train)
    y_pred_test = mdl.predict(X_test)

    train_R2 = np.round(metrics.r2_score(y_train, y_pred_train) * 100, 2)
    test_R2 = np.round(metrics.r2_score(y_test, y_pred_test) * 100, 2)

    train_mae = np.round(
        metrics.mean_absolute_error(y_train, y_pred_train, sample_weight=None, multioutput='uniform_average'), 3)
    test_mae = np.round(
        metrics.mean_absolute_error(y_test, y_pred_test, sample_weight=None, multioutput='uniform_average'), 3)

    train_rmse = np.round(math.sqrt(
        metrics.mean_squared_error(y_train, y_pred_train, sample_weight=None, multioutput='uniform_average')), 3)
    test_rmse = np.round(math.sqrt(
        metrics.mean_squared_error(y_test, y_pred_test, sample_weight=None, multioutput='uniform_average')), 3)

    train_KS = ks_2samp(y_pred_train, y_train)[0]
    test_KS = ks_2samp(y_pred_test, y_test)[0]

    train_gini = Gini(y_train, y_pred_train)
    test_gini = Gini(y_test, y_pred_test)

    train_SF = scale_factor(y_pred_train, y_train)
    test_SF = scale_factor(y_pred_test, y_test)

    if msle == True:
        train_MSLE = np.round(metrics.mean_squared_log_error(y_train, y_pred_train), 3)
        test_MSLE = np.round(metrics.mean_squared_log_error(y_test, y_pred_test), 3)

    else:
        train_MSLE = '-'
        test_MSLE = '-'

    if mape == True:
        train_MAPE = np.round(np.mean(np.abs((y_train - y_pred_train) / y_train)) * 100, 3)
        test_MAPE = np.round(np.mean(np.abs((y_test - y_pred_test) / y_test)) * 100, 3)

    else:
        train_MAPE = '-'
        test_MAPE = '-'

    if feature_importances == True:
        feature_imp = pd.DataFrame({'columns': X_train.columns, 'importance': model.feature_importances_}).sort_values(
            'importance', ascending=False)
        display(feature_imp[feature_imp['importance'] > 0].head(20))

    Resultados = pd.concat([pd.Series(model_name), pd.Series(train_R2), pd.Series(test_R2),
                            pd.Series(train_MAPE), pd.Series(test_MAPE), pd.Series(train_mae), pd.Series(test_mae),
                            pd.Series(train_gini), pd.Series(test_gini), pd.Series(train_SF), pd.Series(test_SF),
                            pd.Series(train_KS), pd.Series(test_KS), pd.Series(train_rmse), pd.Series(test_rmse),
                            pd.Series(train_MSLE), pd.Series(test_MSLE)], axis=1)

    Resultados.columns = ['Modelo', 'Train_R2', 'Test_R2', 'Train_MAPE', 'Test_MAPE', 'Train_MAE', 'Test_MAE',
                          'Train_Gini_Norm', 'Test_Gini_Norm', 'Train_SF', 'Test_SF', 'Train_KS', 'Test_KS',
                          'Train_RMSE', 'Test_RMSE', 'Train_MSLE', 'Test_MSLE']

    return Resultados

def metricas(y_pred_train, y_train, y_pred_test, y_test):
    from scipy.stats import ks_2samp
    import numpy as np
    from sklearn import metrics
    import math as math

    train_MAE = np.round(
        metrics.mean_absolute_error(y_train, y_pred_train, sample_weight=None, multioutput='uniform_average'), 3)
    train_MAPE = np.round(np.mean(np.abs((y_train - y_pred_train) / y_train)) * 100, 3)
    train_RMSE = np.round(math.sqrt(metrics.mean_squared_error(y_train, y_pred_train)), 3)
    train_R2 = np.round(metrics.r2_score(y_train, y_pred_train), 3)
    # train_R2_Adj = 1-(1-train_R2)*(len(X_train)-1)/(len(X_train)-len(X_train.columns)-1)
    train_KS = ks_2samp(y_pred_train, y_train)[1]
    train_gini = Gini(y_train, y_pred_train)
    train_SF = scale_factor(y_pred_train, y_train)
    #train_MSLE = np.round(metrics.mean_squared_log_error(y_train, y_pred_train), 3)

    test_MAE = np.round(
        metrics.mean_absolute_error(y_test, y_pred_test, sample_weight=None, multioutput='uniform_average'), 3)
    test_MAPE = np.round(np.mean(np.abs((y_test - y_pred_test) / y_test)) * 100, 3)
    test_RMSE = np.round(math.sqrt(metrics.mean_squared_error(y_test, y_pred_test)), 3)
    test_R2 = np.round(metrics.r2_score(y_test, y_pred_test), 3)
    # test_R2_Adj = 1-(1-test_R2)*(len(X_test)-1)/(len(X_test)-len(X_test.columns)-1)
    test_KS = ks_2samp(y_pred_test, y_test)[1]
    test_gini = Gini(y_test, y_pred_test)
    test_SF = scale_factor(y_pred_test, y_test)
    #test_MSLE = np.round(metrics.mean_squared_log_error(y_test, y_pred_test), 3)

    Resultados = pd.concat([pd.Series(train_R2), pd.Series(test_R2),
                            pd.Series(train_MAPE), pd.Series(test_MAPE), pd.Series(train_MAE), pd.Series(test_MAE),
                            pd.Series(train_gini), pd.Series(test_gini), pd.Series(train_SF), pd.Series(test_SF),
                            pd.Series(train_KS), pd.Series(test_KS), pd.Series(train_RMSE), pd.Series(test_RMSE),
                            #pd.Series(train_MSLE), pd.Series(test_MSLE)
                            ], axis=1)

    Resultados.columns = ['Train_R2', 'Test_R2', 'Train_MAPE', 'Test_MAPE', 'Train_MAE', 'Test_MAE',
                          'Train_Gini_Norm', 'Test_Gini_Norm', 'Train_SF', 'Test_SF', 'Train_KS', 'Test_KS',
                          'Train_RMSE', 'Test_RMSE',
                          #'Train_MSLE', 'Test_MSLE'
                          ]

    return Resultados

######## Calculo de residuos ########

def residuos(y_pred_test, y_test):
    import matplotlib.pyplot as plt
    from sklearn.preprocessing import StandardScaler

    res = pd.concat([pd.Series(y_pred_test).reset_index(drop=True), pd.Series(y_test).reset_index(drop=True)], axis=1)
    res.columns = ['y_pred', 'y_test']
    res['dif'] = res['y_pred'] - res['y_test']
    var_error = (1 / (len(X_train_final) - len(X_train_final.columns) - 1)) * ((res['dif'] ** 2).sum())
    scaler = StandardScaler()
    res['dif_norm'] = (res['dif'] - res['dif'].mean()) / np.var(res['dif'])
    ser = var_error ** (1 / 2)

    print('Error Total:', res['dif'].sum())
    print('Error Medio:', res['dif'].sum() / len(res))
    print('Error Absoluto Medio:', abs(res['dif']).sum() / len(res))
    print('Varianza Error:', var_error)
    print('Desvio Estandar Error:', ser)

    ### Grafico de Real vs Predicho por Decil
    res['decil_pred'] = np.where(res['y_pred'] <= np.quantile(res['y_pred'], 0.1), 1,
                                 np.where(res['y_pred'] <= np.quantile(res['y_pred'], 0.2), 2,
                                          np.where(res['y_pred'] <= np.quantile(res['y_pred'], 0.3), 3,
                                                   np.where(res['y_pred'] <= np.quantile(res['y_pred'], 0.4), 4,
                                                            np.where(res['y_pred'] <= np.quantile(res['y_pred'], 0.5),
                                                                     5,
                                                                     np.where(
                                                                         res['y_pred'] <= np.quantile(res['y_pred'],
                                                                                                      0.6), 6,
                                                                         np.where(
                                                                             res['y_pred'] <= np.quantile(res['y_pred'],
                                                                                                          0.7), 7,
                                                                             np.where(res['y_pred'] <= np.quantile(
                                                                                 res['y_pred'], 0.8), 8,
                                                                                      np.where(
                                                                                          res['y_pred'] <= np.quantile(
                                                                                              res['y_pred'], 0.9), 9,
                                                                                          10)))))))))

    res['decil_test'] = np.where(res['y_test'] <= np.quantile(res['y_test'], 0.1), 1,
                                 np.where(res['y_test'] <= np.quantile(res['y_test'], 0.2), 2,
                                          np.where(res['y_test'] <= np.quantile(res['y_test'], 0.3), 3,
                                                   np.where(res['y_test'] <= np.quantile(res['y_test'], 0.4), 4,
                                                            np.where(res['y_test'] <= np.quantile(res['y_test'], 0.5),
                                                                     5,
                                                                     np.where(
                                                                         res['y_test'] <= np.quantile(res['y_test'],
                                                                                                      0.6), 6,
                                                                         np.where(
                                                                             res['y_test'] <= np.quantile(res['y_test'],
                                                                                                          0.7), 7,
                                                                             np.where(res['y_test'] <= np.quantile(
                                                                                 res['y_test'], 0.8), 8,
                                                                                      np.where(
                                                                                          res['y_test'] <= np.quantile(
                                                                                              res['y_test'], 0.9), 9,
                                                                                          10)))))))))

    prediccion_deciles = res[['decil_pred', 'y_pred']].groupby('decil_pred').mean()
    real_deciles = res[['decil_test', 'y_test']].groupby('decil_test').mean()

    deciles = pd.concat([prediccion_deciles, real_deciles], axis=1)
    deciles['relativo'] = deciles['y_pred'] / deciles['y_test'] - 1

    sns.set(font_scale=1)
    plt.figure(figsize=(6, 4))
    sns.set_style("whitegrid")

    f = sns.lineplot(x=real_deciles.index, y='y_test', data=real_deciles, label='Real')
    g = sns.lineplot(x=prediccion_deciles.index, y='y_pred', data=prediccion_deciles, color='r', label='Predicho')

    plt.xlabel("Deciles")
    plt.ylabel("Costo Judicial Medio")
    plt.title("Costo Judicial Medio por Deciles")
    plt.legend(loc='upper left')
    plt.show()

    ### Grafico de Distribucion de Residuos
    plt.figure(figsize=(20, 5))
    sns.set_style("whitegrid")
    sns.set(font_scale=1.5)

    f = sns.lineplot(x=res.index, y="dif_norm", data=res, label='Residuos')
    g = sns.lineplot(x=res.index, y=0, data=res, color='r')

    plt.xlabel("Observaciones")
    plt.ylabel("Error Estandarizado")
    # plt.ylim([-2000000,2000000])
    plt.title("Distribucion de los Residuos")
    plt.legend(loc='upper right')
    plt.xticks(rotation=45)
    sns.set(font_scale=1)
    plt.show()

