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
config_data = json.load(open('C:/Repo/MiM_Analytics_Tesis/Tesis/dash_app/config_dash.json'))
preprocessing = ClassPreprocessing(config_data)
df_season_players = preprocessing.load_score_process_data(dataset='player_seasons', generate_dropdown=False)
df_players = preprocessing.load_score_process_data(dataset='player_all_seasons')
dropdown_options = joblib.load('C:/Repo/MiM_Analytics_Tesis/Tesis/dash_app/data/dropdown_options.pkl')

for country in list(dropdown_options.keys()):
    if country not in ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Mexico', 'Peru']:
        del dropdown_options[country]

cols_table = ['player_name', 'Perf_Index_scaled', 'player_preferred_position', 'team_name', 'team_country',
              'player_minutes', 'goals_total', 'goals_assists']

def table(df):
    df_table = df[cols_table].sort_values("Perf_Index_scaled", ascending=False).rename(columns=config_data["ScoutingHeader"]).copy()

    table = dash_table.DataTable(
            data=df_table.to_dict('records'),
            columns=[{'id': c, 'name': c} for c in df_table.columns],
            fixed_rows={'headers': False},
            style_table={'maxHeight': '500px', 'borderRadius': '15px'},
            style_header={
                    'backgroundColor': '#192280',
                    'textAlign': 'center',
                    'color': 'white',
                    'font-family': ['Roboto', 'sans-serif'],
                    'border': '2px solid white',
                    'fontSize': '14px',
                    'textOverflow': 'ellipsis'},
            style_data_conditional=[{
                    'backgroundColor': 'white',
                    'color': '#1e2794',
                    'border': '0.5px solid blue',
                    'font-family': ['Roboto', 'sans-serif'],
                    'fontSize': '12px',
                    'textOverflow': 'ellipsis',
                    'textAlign': 'center'}],
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
        dbc.Row([dbc.Col(
                [html.H6(id='measure_liga', children='Liga'),
                 dcc.Dropdown(id='dropdown_liga', placeholder='Todas las ligas', options=[{'label': i, 'value': i} for i in sorted(df_players['team_country'].unique())]),
                 html.Br(),
                 html.H6(id='measure_season', children='Temporada'),
                 dcc.Dropdown(id='dropdown_season', placeholder='Todas las temporadas', options=[{'label': i, 'value': i} for i in sorted(df_season_players['season'].unique())]),
                 html.Br(),
                 html.H6(id='measure_posicion', children='Posicion'),
                 dcc.Dropdown(id='dropdown_posicion', placeholder='Todas las posiciones', options=[{'label': i, 'value': i} for i in sorted(df_players['player_preferred_position'].unique())]),
                 html.Br(),
                 html.H6(id='measure_minutes', children='Minutos jugados'),
                 dcc.RangeSlider(id='slider_minutes', min=270, max=4500, value=[270, 4500], tooltip={"placement": "bottom", "always_visible": True}),
                 html.Br(),
                 html.H6(id='measure_goals', children='Goles'),
                 dcc.RangeSlider(id='slider_goals', min=0, max=50, value=[0, 200], tooltip={"placement": "bottom", "always_visible": True}),
                 html.Br(),
                 html.H6(id='measure_assists', children='Asistencias'),
                 dcc.RangeSlider(id='slider_assits', min=0, max=100, value=[0, 100], tooltip={"placement": "bottom", "always_visible": True}),
                 html.Br(),
                 html.H6(id='measure_yellow', children='Tarjetas amarillas'),
                 dcc.RangeSlider(id='slider_yellow', min=0, max=30, value=[0, 30], tooltip={"placement": "bottom", "always_visible": True}),
                 html.Br(),
                 html.H6(id='measure_red', children='Tarjetas rojas'),
                 dcc.RangeSlider(id='slider_red', min=0, max=10, value=[0, 10], tooltip={"placement": "bottom", "always_visible": True}),
                 html.Br(),
                 html.Br(),
                 html.H4(id='title_performance', children='Performance'),
                 html.H6(id='measure_index', children='Performance index'),
                 dcc.RangeSlider(id='slider_perf_index', min=0, max=100, value=[0, 100], tooltip={"placement": "bottom", "always_visible": True}),
                 html.Br(),
                 html.Br(),
                 html.H4(id='title_attack', children='Attacking'),
                 html.H6(id='measure_shots_p90', children='Shots P90'),
                 dcc.RangeSlider(id='slider_shots_p90', min=0, max=100, value=[0, 100], tooltip={"placement": "bottom", "always_visible": True})],
                xl=3, lg=3, md=3, sm=12, xs=12),
                dbc.Col([html.Div(id='table_season', children=table(df_players))],
                        xl=8, lg=8, md=8, sm=12, xs=12)]),
], fluid=True)

@app.callback(Output('table_season', 'children'),
              [Input('dropdown_liga', 'value'),
               Input('dropdown_season', 'value'),
               Input('dropdown_posicion', 'value'),
               Input('slider_minutes', 'value'),
               Input('slider_goals', 'value'),
               Input('slider_assits', 'value'),
               Input('slider_yellow', 'value'),
               Input('slider_red', 'value'),
               Input('slider_perf_index', 'value')])
def update_output(value_liga, value_season, value_posicion, value_minutes, value_goals, value_assists,
                  value_yellow, value_red, value_perf_index):

    if value_season != None:
        df_table = df_season_players[df_season_players['season'] == value_season].copy()
    else:
        df_table = df_players.copy()

    if value_liga != None:
        df_table = df_table[df_table['team_country'] == value_liga]

    if value_posicion != None:
        df_table = df_table[df_table['player_preferred_position'] == value_posicion]

    df_table = df_table[(df_table['player_minutes'] >= value_minutes[0]) & (df_table['player_minutes'] <= value_minutes[1])]
    df_table = df_table[(df_table['goals_total'] >= value_goals[0]) & (df_table['goals_total'] <= value_goals[1])]
    df_table = df_table[(df_table['goals_assists'] >= value_assists[0]) & (df_table['goals_assists'] <= value_assists[1])]
    df_table = df_table[(df_table['cards_yellow'] >= value_yellow[0]) & (df_table['cards_yellow'] <= value_yellow[1])]
    df_table = df_table[(df_table['cards_red'] >= value_red[0]) & (df_table['cards_red'] <= value_red[1])]
    df_table = df_table[(df_table['Perf_Index_scaled'] >= value_perf_index[0]) & (df_table['Perf_Index_scaled'] <= value_perf_index[1])]

    return table(df_table)

if __name__ == '__main__':
    app.run_server()

