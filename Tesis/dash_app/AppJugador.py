import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash_table
import json
import joblib
import sys
PATH_PI = 'C:/Repo/MiM_Analytics_Tesis/Tesis/dash_app/'
sys.path.insert(0, PATH_PI)
from ClassAppPreprocessing import ClassPreprocessing

app = dash.Dash(external_stylesheets=[dbc.themes.YETI])

# Load data
config_data = json.load(open(PATH_PI+'config_dash.json'))
preprocessing = ClassPreprocessing(config_data)
df_season_players = preprocessing.load_score_process_data(dataset='player_seasons', source='csv', generate_dropdown=False)
df_players = preprocessing.load_score_process_data(dataset='player_all_seasons', source='csv')
dropdown_options = joblib.load(PATH_PI+'data/dropdown_options.pkl')
countries_latam = ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Mexico', 'Peru']
dropdown_options = {country: dropdown_options[country] for country in countries_latam}

def create_player_table(df, phase, season):
    """
    Creates table of statistics to display for selected player in a specific phase of the game and season
    :param df: dataframe with player's metrics
    :param phase: phase of the game (attack, build-up, defense, general stats)
    :param season: season of the league
    :return:
        Filtered dataframe with relevant statistics to display
    """
    df_filtered = df[df['season'] == season][config_data["DashColumns"][phase]].transpose().reset_index()
    df_filtered.columns = ['Var', 'Value']
    for col in df_filtered['Var'].to_list():
        if col in config_data["PctVars"]:
            df_filtered.loc[df_filtered['Var'] == col, 'Value'] = df_filtered.loc[df_filtered['Var'] == col, 'Value'].apply(lambda x: str(round(x*100))+'%')
        elif col == 'player_preferred_position':
            pass
        else:
            df_filtered.loc[df_filtered['Var'] == col, 'Value'] = df_filtered.loc[df_filtered['Var'] == col, 'Value'].apply(lambda x: round(x*-1, 2) if x < 0 else round(x, 2))

    df_filtered['Feature'] = df_filtered['Var'].map(config_data['ColumnNames'])

    return df_filtered[['Feature', 'Value']]

# Tables
initial_player = 'Julian Alvarez'
initial_team = 'River Plate'
df_initial_player = df_season_players[df_season_players['player_name'] == initial_player]
h2_player_title = f'{initial_player}'
df_season = create_player_table(df_initial_player, phase='stats_season', season=config_data['Parameters']['current_season'])
df_attack = create_player_table(df_initial_player, phase='attack', season=config_data['Parameters']['current_season'])
df_buildup = create_player_table(df_initial_player, phase='build_up', season=config_data['Parameters']['current_season'])
df_defense = create_player_table(df_initial_player, phase='defense', season=config_data['Parameters']['current_season'])

# Plots Config
dict_xaxis = dict(
        title='Temporada',
        showline=True,
        showgrid=False,
        showticklabels=True,
        linecolor='rgb(204, 204, 204)',
        linewidth=2,
        ticks='outside'
)

dict_yaxis = dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False
)

dict_margins = dict(
        autoexpand=False,
        l=100,
        r=25,
        t=60,
)

dict_layout = {'xaxis': dict_xaxis, 'yaxis': dict_yaxis, 'margins': dict_margins}

# Define plots' functions

def bar_chart(df, var, layout):
    """
    Creates a bar chart for a specified variable
    :param df: dataframe with feature to plot
    :param var: variable to plot
    :param layout: layout to use in the axis and margins
    :return:
        figure object to display in the Dash app
    """
    fig = go.Figure([go.Bar(x=df['season'], y=df[var],
                            text=df[var], textposition='auto',
                            marker_color='darkblue', name='PI')])

    fig.update_layout(
            title='Performance Index',
            xaxis=layout['xaxis'],
            yaxis=layout['yaxis'],
            autosize=False,
            width=1000,
            height=250,
            margin=layout['margins'],
            showlegend=False,
            plot_bgcolor='white'
    )

    return fig

def line_chart(df, var, dict_vars, layout):
    """
    Creates a line chart for a specified variable
    :param df: dataframe with feature to plot
    :param var: variable to plot
    :param layout: layout to use in the axis and margins
    :return:
        figure object to display in the Dash app
    """
    df[var] = round(df[var], 2)

    fig = go.Figure(data=[go.Scatter(x=df['season'], y=df[var],
                                     line=dict(color='firebrick', width=3), fill='tozeroy',
                                     text=df[var], textposition='top center')])

    fig.update_layout(
            title=dict_vars["ColumnNames"][var],
            xaxis=layout['xaxis'],
            yaxis=layout['yaxis'],
            autosize=False,
            width=400,
            height=200,
            margin=layout['margins'],
            showlegend=False,
            plot_bgcolor='white'
    )

    return fig

# Radar chart
# df = df_season_players
# player_name = initial_player
# season = config_data['Parameters']['current_season']


def radar_chart(df, player_name, team_name, season):

    # Player
    factors_cols = ['player_name',  'Factor 1_scaled', 'Factor 2_scaled', 'Factor 3_scaled', 'Factor 4_scaled', 'Factor 5_scaled']
    player_mask = (df['player_name'] == player_name) & (df['season'] == season) & (df['team_name'] == team_name)
    player_position = df[player_mask]['player_preferred_position'].values[0]
    df_player_radar = round(df[player_mask][factors_cols].set_index('player_name')*100)
    player_values = df_player_radar.values.flatten().tolist()
    player_values += player_values[:1]

    # Avg Player
    factor1_avg = df[df['player_preferred_position'] == player_position]['Factor 1_scaled'].mean()
    factor2_avg = df[df['player_preferred_position'] == player_position]['Factor 2_scaled'].mean()
    factor3_avg = df[df['player_preferred_position'] == player_position]['Factor 3_scaled'].mean()
    factor4_avg = df[df['player_preferred_position'] == player_position]['Factor 4_scaled'].mean()
    factor5_avg = df[df['player_preferred_position'] == player_position]['Factor 5_scaled'].mean()
    df_avg_player = round(pd.DataFrame({'AvgPlayer': [factor1_avg, factor2_avg, factor3_avg, factor4_avg, factor5_avg]}).transpose()*100)
    avg_player_values = df_avg_player.values.flatten().tolist()
    avg_player_values += avg_player_values[:1]

    if player_position == 'Delantero':
        categories = ['Efectividad', 'Asistencia', 'Ataque', 'Dribbling', 'Defensa']
    if player_position == 'Mediocampista':
        categories = ['Ataque', 'Defensa', 'Pases', 'Agresividad', 'Dribbling']
    if player_position == 'Defensor':
        categories = ['Agresividad', 'Pases', 'Duelos', 'Penales', 'Cruces']
    if player_position == 'Arquero':
        categories = ['Defensa', 'Pases', 'Arco invicto', 'Duelos', 'Salvadas']

    categories = [*categories, categories[0]]

    fig = go.Figure(
            data=[
                    go.Scatterpolar(r=avg_player_values, theta=categories, fill='toself', name='{} promedio'.format(player_position)),
                    go.Scatterpolar(r=player_values, theta=categories, fill='toself', name=player_name)
            ],
            layout=go.Layout(
                    # title=go.layout.Title(text='Player comparison'),
                    polar={'radialaxis': {'visible': True, 'range': [0, 100]}},
                    showlegend=True
            )
    )

    return fig

# Table
def table(df):
    """
    Transforms a given dataframe into a DataTable for Dash to display
    :param df: dataframe with players to display
    :return:
        dataframe in DataTable format for Dash to display
    """
    table = dash_table.DataTable(
            data=df[['Feature', 'Value']].to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df[['Feature', 'Value']].columns],
            fixed_rows={'headers': False},
            style_table={'maxHeight': '500px'},
            style_header={'display': 'none'},
            style_data_conditional=[{
                    'backgroundColor': '#008cba',
                    'color': 'white',
                    'font-family': ['Roboto', 'sans-serif'],
                    'fontSize': '16px'},
                    {'if': {'column_id': 'Feature'}, 'textAlign': 'left'}],
            style_cell={
                    'textAlign': 'center',
                    'border': '2px solid white',
                    'maxWidth': '50px',
                    'textOverflow': 'ellipsis'},
            style_as_list_view=True
    )

    return table

# Navigation Bar
PATH_logo = 'https://cdn.imgbin.com/0/5/11/imgbin-logo-football-photography-football-white-and-black-soccer-ball-Gyz1CSJpkP6NGb7GmuJuSDt2a.jpg'
navbar = dbc.Navbar(id='navbar', children=[
        dbc.Row([
                dbc.Col(html.Img(src=PATH_logo, height="60px")),
                dbc.Col(dbc.NavbarBrand("Football Analytics App", style={'color': 'white', 'fontSize': '20px'}))],
                align="center"), # no_gutters elimina los espacios feos y alinea todo
        ], dark=True, color='dark')

app.layout = dbc.Container([
        dbc.Row([dbc.Col([html.Div(id='parent', children=[navbar])], xl=12, lg=12, md=12, sm=12, xs=12)]),
        html.Br(),
        # Filters
        dbc.Row([dbc.Col(dcc.Dropdown(id='country-dropdown', placeholder='Seleccione un pais', options=[{'label': i, 'value': i} for i in dropdown_options.keys()], value='Argentina')),
                 dbc.Col(dcc.Dropdown(id='season-dropdown', placeholder='Seleccione una temporada', value='2021/22')),
                 dbc.Col(dcc.Dropdown(id='team-dropdown', placeholder='Seleccione un equipo', value='River Plate')),
                 dbc.Col(dcc.Dropdown(id='player-dropdown', placeholder='Seleccione un jugador', value='Julian Alvarez'))]),
        dbc.Row([dbc.Col([html.H2(id='H2_player_title', children=h2_player_title)], xl=12, lg=12, md=12, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 30, 'marginBottom': 5}),

        # Season
        dbc.Row([dbc.Col([dcc.Graph(id='radar_chart', figure=radar_chart(df_season_players, initial_player, initial_team, config_data['Parameters']['current_season']))],
                         xl=12, lg=12, md=12, sm=12, xs=12)]),

        dbc.Row([dbc.Col([html.Div(id='table_season', children=table(df_season))], xl=3, lg=3, md=3, sm=12, xs=12),
                 dbc.Col([dcc.Graph(id='bar_plot_index', figure=bar_chart(df_initial_player, 'Perf_Index_scaled', dict_layout))],
                         xl=9, lg=9, md=9, sm=12, xs=12)]),
        # Attack
        dbc.Row([dbc.Col([html.H4(id='title_attack', children='Ataque')], xl=4, lg=4, md=4, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 15, 'marginBottom': 5}),
        dbc.Row([dbc.Col([html.Div(id='table_attack', children=table(df_attack))], xl=3, lg=3, md=3, sm=12, xs=12),
                 dbc.Col([dbc.Row([
                             dbc.Col([dcc.Graph(id='line_plot_goals', figure=line_chart(df_initial_player, 'goals_p90', config_data, dict_layout))],
                                     xl=5, lg=5, md=5, sm=12, xs=12),
                             dbc.Col([dcc.Graph(id='line_plot_assists', figure=line_chart(df_initial_player, 'assists_p90', config_data, dict_layout))],
                                     xl=4, lg=4, md=4, sm=12, xs=12)]),

                         dbc.Row([
                             dbc.Col([dcc.Graph(id='line_plot_shots', figure=line_chart(df_initial_player, 'shots_p90', config_data, dict_layout))],
                                     xl=5, lg=5, md=5, sm=12, xs=12),
                             dbc.Col([dcc.Graph(id='line_plot_shooting_acc', figure=line_chart(df_initial_player, 'shooting_accuracy', config_data, dict_layout))],
                                     xl=4, lg=4, md=4, sm=12, xs=12)])])]),

        # Build-up
        dbc.Row([dbc.Col([html.H4(id='title_buildup', children='Creación de juego y 1-vs-1')], xl=4, lg=4, md=4, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 15, 'marginBottom': 5}),
        dbc.Row([dbc.Col([html.Div(id='table_buildup', children=table(df_buildup))], xl=3, lg=3, md=3, sm=12, xs=12),
                 dbc.Col([dbc.Row([
                         dbc.Col([dcc.Graph(id='line_plot_passes', figure=line_chart(df_initial_player, 'passes_p90', config_data, dict_layout))],
                                 xl=5, lg=5, md=5, sm=12, xs=12),
                         dbc.Col([dcc.Graph(id='line_plot_passing_acc', figure=line_chart(df_initial_player, 'passing_accuracy', config_data, dict_layout))],
                                 xl=4, lg=4, md=4, sm=12, xs=12)]),

                         dbc.Row([
                                 dbc.Col([dcc.Graph(id='line_plot_dribbles', figure=line_chart(df_initial_player, 'dribbles_p90', config_data, dict_layout))],
                                         xl=5, lg=5, md=5, sm=12, xs=12),
                                 dbc.Col([dcc.Graph(id='line_plot_duels', figure=line_chart(df_initial_player, 'duels_p90', config_data, dict_layout))],
                                         xl=4, lg=4, md=4, sm=12, xs=12)])])]),

        # Defense
        dbc.Row([dbc.Col([html.H4(id='title_defense', children='Defensa y Disciplina')], xl=4, lg=4, md=4, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 15, 'marginBottom': 5}),
        dbc.Row([dbc.Col([html.Div(id='table_defense', children=table(df_defense))], xl=3, lg=3, md=3, sm=12, xs=12),
                 dbc.Col([dbc.Row([
                         dbc.Col([dcc.Graph(id='line_plot_saves', figure=line_chart(df_initial_player, 'saves_p90', config_data, dict_layout))],
                                 xl=5, lg=5, md=5, sm=12, xs=12),
                         dbc.Col([dcc.Graph(id='line_plot_tackles', figure=line_chart(df_initial_player, 'tackles_p90', config_data, dict_layout))],
                                 xl=4, lg=4, md=4, sm=12, xs=12)]),

                         dbc.Row([
                                 dbc.Col([dcc.Graph(id='line_plot_interceptions', figure=line_chart(df_initial_player, 'interceptions_p90', config_data, dict_layout))],
                                         xl=5, lg=5, md=5, sm=12, xs=12),
                                 dbc.Col([dcc.Graph(id='line_plot_blocks', figure=line_chart(df_initial_player, 'blocks_p90', config_data, dict_layout))],
                                         xl=4, lg=4, md=4, sm=12, xs=12)])])]),

], fluid=True)

@app.callback(Output('season-dropdown', 'options'),
              [Input('country-dropdown', 'value')])
def set_season_options(selected_country):
    return sorted([{'label': i, 'value': i} for i in dropdown_options['{}'.format(selected_country)].keys()], key=lambda x: x['value'], reverse=True)

@app.callback(Output('season-dropdown', 'value'),
              [Input('season-dropdown', 'options')])
def set_season_value(season_options):
    return season_options[0]['value']

@app.callback(Output('team-dropdown', 'options'),
              [Input('season-dropdown', 'value'),
               Input('country-dropdown', 'value')])
def set_team_options(selected_season, selected_country):
    return sorted([{'label': i, 'value': i} for i in dropdown_options['{}'.format(selected_country)]['{}'.format(selected_season)].keys()], key=lambda x: x['value'])

@app.callback(Output('team-dropdown', 'value'),
              [Input('team-dropdown', 'options')])
def set_team_value(team_options):
    return team_options[0]['value']

@app.callback(Output('player-dropdown', 'options'),
              [Input('team-dropdown', 'value'),
               Input('season-dropdown', 'value'),
               Input('country-dropdown', 'value')])
def set_players_options(selected_team, selected_season, selected_country):
    return sorted([{'label': i, 'value': i} for i in dropdown_options['{}'.format(selected_country)]['{}'.format(selected_season)]['{}'.format(selected_team)]], key=lambda x: x['value'])

@app.callback(Output('player-dropdown', 'value'),
              [Input('player-dropdown', 'options')])
def set_players_value(player_options):
    return player_options[0]['value']

@app.callback([Output(component_id='H2_player_title', component_property='children'),
               Output(component_id='table_season', component_property='children'),
               Output(component_id='table_attack', component_property='children'),
               Output(component_id='table_buildup', component_property='children'),
               Output(component_id='table_defense', component_property='children'),
               Output(component_id='radar_chart', component_property='figure'),
               Output(component_id='bar_plot_index', component_property='figure'),
               Output(component_id='line_plot_goals', component_property='figure'),
               Output(component_id='line_plot_assists', component_property='figure'),
               Output(component_id='line_plot_shots', component_property='figure'),
               Output(component_id='line_plot_shooting_acc', component_property='figure'),
               Output(component_id='line_plot_passes', component_property='figure'),
               Output(component_id='line_plot_passing_acc', component_property='figure'),
               Output(component_id='line_plot_dribbles', component_property='figure'),
               Output(component_id='line_plot_duels', component_property='figure'),
               Output(component_id='line_plot_saves', component_property='figure'),
               Output(component_id='line_plot_tackles', component_property='figure'),
               Output(component_id='line_plot_interceptions', component_property='figure'),
               Output(component_id='line_plot_blocks', component_property='figure')],
              [Input('season-dropdown', 'value'),
               Input('team-dropdown', 'value'),
               Input('player-dropdown', 'value')])
def update_player_data(season_dropdown_value, team_dropdown_value, player_dropdown_value):

    if player_dropdown_value != None:
        player_id = df_season_players.loc[(df_season_players['player_name'] == player_dropdown_value) &
                                          (df_season_players['team_name'] == team_dropdown_value), 'player_id'].values[0]
        df_player = df_season_players.loc[(df_season_players['player_id'] == player_id), :]

    # Tables
    df_season = create_player_table(df_player, phase='stats_season', season=season_dropdown_value)
    df_attack = create_player_table(df_player, phase='attack', season=season_dropdown_value)
    df_buildup = create_player_table(df_player, phase='build_up', season=season_dropdown_value)
    df_defense = create_player_table(df_player, phase='defense', season=season_dropdown_value)
    table_season = table(df_season)

    table_attack = table(df_attack)
    table_buildup = table(df_buildup)
    table_defense = table(df_defense)
    # Plots
    fig_radar = radar_chart(df_season_players, player_dropdown_value, team_dropdown_value, season_dropdown_value)
    fig_index = bar_chart(df_player, 'Perf_Index_scaled', dict_layout)
    fig_goals = line_chart(df_player, 'goals_p90', config_data, dict_layout)
    fig_assists = line_chart(df_player, 'assists_p90', config_data, dict_layout)
    fig_shots = line_chart(df_player, 'shots_p90', config_data, dict_layout)
    fig_shooting_acc = line_chart(df_player, 'shooting_accuracy', config_data, dict_layout)
    fig_passes = line_chart(df_player, 'passes_p90', config_data, dict_layout)
    fig_passing_acc = line_chart(df_player, 'passing_accuracy', config_data, dict_layout)
    fig_dribbles = line_chart(df_player, 'dribbles_p90', config_data, dict_layout)
    fig_duels = line_chart(df_player, 'duels_p90', config_data, dict_layout)
    fig_saves = line_chart(df_player, 'saves_p90', config_data, dict_layout)
    fig_tackles = line_chart(df_player, 'tackles_p90', config_data, dict_layout)
    fig_interceptions = line_chart(df_player, 'interceptions_p90', config_data, dict_layout)
    fig_blocks = line_chart(df_player, 'blocks_p90', config_data, dict_layout)

    h2_player_title = f'{player_dropdown_value}'

    return h2_player_title, table_season, table_attack, table_buildup, table_defense, fig_radar, \
           fig_index, fig_goals, fig_assists, fig_shots, fig_shooting_acc, fig_passes, fig_passing_acc, fig_dribbles, \
           fig_duels, fig_saves, fig_tackles, fig_interceptions, fig_blocks

if __name__ == '__main__':
    app.run_server()

