import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash_table
import json

app = dash.Dash(external_stylesheets=[dbc.themes.YETI])

# Load data
df = pd.read_csv('C:/Repo/MiM_Analytics_Tesis/Tesis/DASH_PlayersScored_20211101.csv', sep='|', decimal='.')
config_data = json.load(open('C:/Repo/MiM_Analytics_Tesis/Tesis/dash_app/config_dash.json'))

df.columns

dict_options = {}

for country in df['team_country'].unique():
    dict_options[country] = {}
    for league in df['league_name'].unique():
        dict_options[country][league] = {}
        for season in df['league_season'].unique():
            dict_options[country][league][str(season)] = {}
            for team in df[df['league_name'] == league]['team_name']:
                dict_options[country][league][season][team] = df[(df['league_name'] == league) & (df['league_season'] == season) & (df['team_name'] == team)]['player_name'].unique()

with open('C:/Repo/MiM_Analytics_Tesis/Tesis/dash_app/data/dropdown_options.json', 'w') as file:
    json.dump(dict_options, file)

dict_options["Argentina"]["Primera Division"][2020]["Boca Juniors"]
team_name = df['team_name'].unique()
player_name = df['player_name'].unique()

dict_options.keys() = ['a', 'b']

dict_options['a'] = 1564

dict_options['b']['sd'] = '123'

df['season'] = df['league_season'].astype(str) + '/' + df['league_season'].apply(lambda x: str(x+1)[2:4])
df['Perf_Index_scaled'] = df['Perf_Index_scaled'].apply(lambda x: round(x*100))
df['wavg_player_rating'] = df['wavg_player_rating'].apply(lambda x: round(x, 2))

player = 'Enzo Perez'
df_player = df[df['player_name'] == player]

current_season = 2020


def create_table(df, phase, season):
    df = df_player[df_player['league_season'] == season][config_data["DashColumns"][phase]].transpose().reset_index()
    df.columns = ['Var', 'Value']
    for col in df['Var'].to_list():
        if col in config_data["PctVars"]:
            df.loc[df['Var'] == col, 'Value'] = df.loc[df['Var'] == col, 'Value'].apply(lambda x: str(round(x*100))+'%')
        elif col == 'player_preferred_position':
            df.loc[df['Var'] == col, 'Value'] = df.loc[df['Var'] == col, 'Value'].map(config_data["ColumnValues"][col])
        else:
            df.loc[df['Var'] == col, 'Value'] = df.loc[df['Var'] == col, 'Value'].apply(lambda x: round(x*-1, 2) if x < 0 else round(x, 2))

    df['Feature'] = df['Var'].map(config_data['ColumnNames'])

    return df[['Feature', 'Value']]

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
        dbc.Row([dbc.Col([html.H2(id='H2', children=f'{player} Statistics')], xl=12, lg=12, md=12, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 30, 'marginBottom': 5}),

        # Season
        dbc.Row([dbc.Col([html.Div(id='table_season', children=table(df_season))], xl=4, lg=4, md=4, sm=12, xs=12),
                dbc.Col([dcc.Graph(id='bar_plot', figure=bar_chart(df_player, 'Perf_Index_scaled', dict_layout))],
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

if __name__ == '__main__':
    app.run_server()

