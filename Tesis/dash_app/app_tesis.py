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

app = dash.Dash(external_stylesheets=[dbc.themes.YETI])

# Load data
df = pd.read_csv('C:/Repo/MiM_Analytics_Tesis/Tesis/DASH_PlayersScored_20211101.csv', sep='|', decimal='.')
config_data = json.load(open('C:/Repo/MiM_Analytics_Tesis/Tesis/dash_app/config_dash.json'))

# dict_options = {}
#
# for country in df['team_country'].unique():
#     print('Pais: ', country)
#     dict_options[country] = {}
#     for league in df[df['team_country'] == country]['league_name'].unique():
#         print('Liga: ', league)
#         dict_options[country][league] = {}
#         for season in df[(df['team_country'] == country) & (df['league_name'] == league)]['league_season'].unique():
#             print('Temporada: ', season)
#             dict_options[country][league][str(season)] = {}
#             for team in df[(df['team_country'] == country) & (df['league_name'] == league) & (df['league_season'] == season)]['team_name']:
#                 dict_options[country][league][str(season)][team] = df[(df['league_name'] == league) & (df['league_season'] == season) & (df['team_name'] == team)]['player_name'].unique()
#
# joblib.dump(dict_options, 'C:/Repo/MiM_Analytics_Tesis/Tesis/dash_app/data/dropdown_options.pkl')

dict_options = joblib.load('C:/Repo/MiM_Analytics_Tesis/Tesis/dash_app/data/dropdown_options.pkl')

df['season'] = df['league_season'].astype(str) + '/' + df['league_season'].apply(lambda x: str(x+1)[2:4])
df['Perf_Index_scaled'] = df['Perf_Index_scaled'].apply(lambda x: round(x*100))
df['wavg_player_rating'] = df['wavg_player_rating'].apply(lambda x: round(x, 2))

player = 'Enzo Perez'
df_player = df[df['player_name'] == player]

current_season = 2020
df_player.columns
df_player[['passes_p90', 'passes_total', 'passes_completed', 'passing_accuracy']]


def create_table(df, phase, season):
    df_filtered = df[df['league_season'] == season][config_data["DashColumns"][phase]].transpose().reset_index()
    df_filtered.columns = ['Var', 'Value']
    for col in df_filtered['Var'].to_list():
        if col in config_data["PctVars"]:
            df_filtered.loc[df_filtered['Var'] == col, 'Value'] = df_filtered.loc[df_filtered['Var'] == col, 'Value'].apply(lambda x: str(round(x*100))+'%')
        elif col == 'player_preferred_position':
            df_filtered.loc[df_filtered['Var'] == col, 'Value'] = df_filtered.loc[df_filtered['Var'] == col, 'Value'].map(config_data["ColumnValues"][col])
        else:
            df_filtered.loc[df_filtered['Var'] == col, 'Value'] = df_filtered.loc[df_filtered['Var'] == col, 'Value'].apply(lambda x: round(x*-1, 2) if x < 0 else round(x, 2))

    df_filtered['Feature'] = df_filtered['Var'].map(config_data['ColumnNames'])

    return df_filtered[['Feature', 'Value']]

# Tables
df_season = create_table(df_player, phase='stats_season', season=current_season)
df_attack = create_table(df_player, phase='attack', season=current_season)
df_buildup = create_table(df_player, phase='build_up', season=current_season)
df_defense = create_table(df_player, phase='defense', season=current_season)

# Plots Config
dict_xaxis = dict(
        title='Season',
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

# Table
def table(df):
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

    # table = dbc.Table.from_dataframe(df[['Feature', 'Value']], striped=False, borderless=True, responsive=True,
    #                                  className="table-primary", size='md', style={"style_header": False})

    return table

# Navigation Bar
PATH_logo = 'https://cdn.imgbin.com/0/5/11/imgbin-logo-football-photography-football-white-and-black-soccer-ball-Gyz1CSJpkP6NGb7GmuJuSDt2a.jpg'

navbar = dbc.Navbar(id='navbar', children=[
        dbc.Row([
                dbc.Col(html.Img(src=PATH_logo, height="60px")),
                dbc.Col(dbc.NavbarBrand("Football Analytics App", style={'color': 'white', 'fontSize': '20px'}))],
                align="center"), # no_gutters elimina los espacios feos y alinea todo
        dbc.Col([], xl=5, lg=5, md=5, sm=5, xs=5),
        dbc.Nav([dbc.NavLink('Home', href='/apps/home', active=True),
                 dbc.NavLink('Equipos', href='/apps/equipos'),
                 dbc.NavLink('Jugador', href='/apps/jugador'),
                 dbc.NavLink('Comparativa', href='/apps/comparativa')],
                style={"fontSize": "17px"}),
        dbc.Button(id='button', children="Log in", color="primary", className='ml-auto')
        ], dark=True, color='dark')

app.layout = dbc.Container([
        dbc.Row([dbc.Col([html.Div(id='parent', children=[navbar])], xl=12, lg=12, md=12, sm=12, xs=12)]),
        html.Br(),
        dbc.Row([dbc.Col(dcc.Dropdown(id='country-dropdown', placeholder='Seleccione un pais', options=[{'label': i, 'value': i} for i in dict_options.keys()], value='Argentina')),
                 dbc.Col(dcc.Dropdown(id='league-dropdown', placeholder='Seleccione una liga')),
                 dbc.Col(dcc.Dropdown(id='season-dropdown', placeholder='Seleccione una temporada')),
                 dbc.Col(dcc.Dropdown(id='team-dropdown', placeholder='Seleccione un equipo')),
                 dbc.Col(dcc.Dropdown(id='player-dropdown', placeholder='Seleccione un jugador'))]),
        dbc.Row([dbc.Col([html.H2(id='H2', children=f'{player} Statistics')], xl=12, lg=12, md=12, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 30, 'marginBottom': 5}),

        # Season
        dbc.Row([dbc.Col([html.Div(id='table_season', children=table(df_season))], xl=4, lg=4, md=4, sm=12, xs=12),
                dbc.Col([dcc.Graph(id='bar_plot_index', figure=bar_chart(df_player, 'Perf_Index_scaled', dict_layout))],
                        xl=8, lg=8, md=8, sm=12, xs=12)]),
        # Attack
        dbc.Row([dbc.Col([html.H4(id='title_attack', children='Ataque')], xl=4, lg=4, md=4, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 15, 'marginBottom': 5}),
        dbc.Row([dbc.Col([html.Div(id='table_attack', children=table(df_attack))], xl=4, lg=4, md=4, sm=12, xs=12),
                 dbc.Col([dbc.Row([
                             dbc.Col([dcc.Graph(id='line_plot_goals', figure=line_chart(df_player, 'goals_p90', config_data, dict_layout))],
                                     xl=4, lg=4, md=4, sm=12, xs=12),
                             dbc.Col([dcc.Graph(id='line_plot_assists', figure=line_chart(df_player, 'assists_p90', config_data, dict_layout))],
                                     xl=4, lg=4, md=4, sm=12, xs=12)]),

                         dbc.Row([
                             dbc.Col([dcc.Graph(id='line_plot_shots', figure=line_chart(df_player, 'shots_p90', config_data, dict_layout))],
                                     xl=4, lg=4, md=4, sm=12, xs=12),
                             dbc.Col([dcc.Graph(id='line_plot_shooting_acc', figure=line_chart(df_player, 'shooting_accuracy', config_data, dict_layout))],
                                     xl=4, lg=4, md=4, sm=12, xs=12)])])]),

        # Build-up
        dbc.Row([dbc.Col([html.H4(id='title_buildup', children='Creación de juego y 1-vs-1')], xl=4, lg=4, md=4, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 15, 'marginBottom': 5}),
        dbc.Row([dbc.Col([html.Div(id='table_buildup', children=table(df_buildup))], xl=4, lg=4, md=4, sm=12, xs=12),
                 dbc.Col([dbc.Row([
                         dbc.Col([dcc.Graph(id='line_plot_passes', figure=line_chart(df_player, 'passes_p90', config_data, dict_layout))],
                                 xl=4, lg=4, md=4, sm=12, xs=12),
                         dbc.Col([dcc.Graph(id='line_plot_passing_acc', figure=line_chart(df_player, 'passing_accuracy', config_data, dict_layout))],
                                 xl=4, lg=4, md=4, sm=12, xs=12)]),

                         dbc.Row([
                                 dbc.Col([dcc.Graph(id='line_plot_dribbles', figure=line_chart(df_player, 'dribbles_p90', config_data, dict_layout))],
                                         xl=4, lg=4, md=4, sm=12, xs=12),
                                 dbc.Col([dcc.Graph(id='line_plot_duels', figure=line_chart(df_player, 'duels_p90', config_data, dict_layout))],
                                         xl=4, lg=4, md=4, sm=12, xs=12)])])]),

        # Defense
        dbc.Row([dbc.Col([html.H4(id='title_defense', children='Defensa y Disciplina')], xl=4, lg=4, md=4, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 15, 'marginBottom': 5}),
        dbc.Row([dbc.Col([html.Div(id='table_defense', children=table(df_defense))], xl=4, lg=4, md=4, sm=12, xs=12),
                 dbc.Col([dbc.Row([
                         dbc.Col([dcc.Graph(id='line_plot_saves', figure=line_chart(df_player, 'saves_p90', config_data, dict_layout))],
                                 xl=4, lg=4, md=4, sm=12, xs=12),
                         dbc.Col([dcc.Graph(id='line_plot_tackles', figure=line_chart(df_player, 'tackles_p90', config_data, dict_layout))],
                                 xl=4, lg=4, md=4, sm=12, xs=12)]),

                         dbc.Row([
                                 dbc.Col([dcc.Graph(id='line_plot_interceptions', figure=line_chart(df_player, 'interceptions_p90', config_data, dict_layout))],
                                         xl=4, lg=4, md=4, sm=12, xs=12),
                                 dbc.Col([dcc.Graph(id='line_plot_blocks', figure=line_chart(df_player, 'blocks_p90', config_data, dict_layout))],
                                         xl=4, lg=4, md=4, sm=12, xs=12)])])]),

], fluid=True)


@app.callback(Output('league-dropdown', 'options'),
              [Input('country-dropdown', 'value')])
def set_league_options(selected_country):
    return [{'label': i, 'value': i} for i in dict_options['{}'.format(selected_country)].keys()]

@app.callback(Output('league-dropdown', 'value'),
              [Input('league-dropdown', 'options')])
def set_league_value(leagues_options):
    return sorted(leagues_options)[0]['value']

@app.callback(Output('season-dropdown', 'options'),
              [Input('league-dropdown', 'value'),
               Input('country-dropdown', 'value')])
def set_season_options(selected_league, selected_country):
    return [{'label': i, 'value': i} for i in dict_options['{}'.format(selected_country)]['{}'.format(selected_league)].keys()]

@app.callback(Output('season-dropdown', 'value'),
              [Input('season-dropdown', 'options')])
def set_season_value(season_options):
    return sorted(season_options)[0]['value']

@app.callback(Output('team-dropdown', 'options'),
              [Input('season-dropdown', 'value'),
               Input('league-dropdown', 'value'),
               Input('country-dropdown', 'value')])
def set_team_options(selected_season, selected_league, selected_country):
    return [{'label': i, 'value': i} for i in dict_options['{}'.format(selected_country)]['{}'.format(selected_league)]['{}'.format(selected_season)].keys()]

@app.callback(Output('team-dropdown', 'value'),
              [Input('team-dropdown', 'options')])
def set_team_value(team_options):
    return sorted(team_options)[0]['value']

@app.callback(Output('player-dropdown', 'options'),
              [Input('team-dropdown', 'value'),
               Input('season-dropdown', 'value'),
               Input('league-dropdown', 'value'),
               Input('country-dropdown', 'value')])
def set_players_options(selected_team, selected_season, selected_league, selected_country):
    return [{'label': i, 'value': i} for i in dict_options['{}'.format(selected_country)]['{}'.format(selected_league)]['{}'.format(selected_season)]['{}'.format(selected_team)]]

@app.callback(Output('player-dropdown', 'value'),
              [Input('player-dropdown', 'options')])
def set_players_value(player_options):
    return sorted(player_options)[0]['value']

@app.callback([Output(component_id='table_season', component_property='children'),
               Output(component_id='table_attack', component_property='children'),
               Output(component_id='table_buildup', component_property='children'),
               Output(component_id='table_defense', component_property='children'),
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
              Input('player-dropdown', 'value'))
def update_player_data(player_dropdown_value):

    if player_dropdown_value != None:
        df_player = df.loc[(df['player_name'] == player_dropdown_value), :]

    # Tables
    df_season = create_table(df_player, phase='stats_season', season=2020)
    df_attack = create_table(df_player, phase='attack', season=2020)
    df_buildup = create_table(df_player, phase='build_up', season=2020)
    df_defense = create_table(df_player, phase='defense', season=2020)
    table_season = table(df_season)
    table_attack = table(df_attack)
    table_buildup = table(df_buildup)
    table_defense = table(df_defense)
    # Plots
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

    return table_season, table_attack, table_buildup, table_defense, \
           fig_index, fig_goals, fig_assists, fig_shots, fig_shooting_acc, fig_passes, fig_passing_acc, fig_dribbles, \
           fig_duels, fig_saves, fig_tackles, fig_interceptions, fig_blocks

# selected_country='Argentina'
# selected_league='Primera Division'
# selected_season='2016'
# selected_team='Boca Juniors'


if __name__ == '__main__':
    app.run_server()

