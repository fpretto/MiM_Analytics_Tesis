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

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

# Load data
df = pd.read_csv('C:/Repo/MiM_Analytics_Tesis/Tesis/DASH_PlayersScored_20211101.csv', sep='|', decimal='.')
config_data = json.load(open('C:/Repo/MiM_Analytics_Tesis/Tesis/dash_app/config_dash.json'))

df['season'] = df['league_season'].astype(str) + '/' + df['league_season'].apply(lambda x: str(x+1)[2:4])
df['Perf_Index_scaled'] = df['Perf_Index_scaled'].apply(lambda x: round(x*100))
df['wavg_player_rating'] = df['wavg_player_rating'].apply(lambda x: round(x, 2))

player = 'Ignacio Scocco'
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
df_season = create_table(df, phase='stats_season', season=current_season)
df_attack = create_table(df, phase='attack', season=current_season)
df_buildup = create_table(df, phase='build_up', season=current_season)
df_defense = create_table(df, phase='defense', season=current_season)

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
            width=500,
            height=250,
            margin=layout['margins'],
            showlegend=False,
            plot_bgcolor='white'
    )

    return fig

def line_chart(df, var, layout):

    fig = go.Figure(data = [go.Scatter(x=df['season'], y=df[var],
                                       line=dict(color='firebrick', width=3), fill='tozeroy',
                                       text=df[var], textposition='top center')])

    fig.update_layout(
            title='Total Goals',
            xaxis=layout['xaxis'],
            yaxis=layout['yaxis'],
            autosize=False,
            width=500,
            height=250,
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
                    'backgroundColor': 'rgb(30, 10, 130)',
                    'color': 'white',
                    'font-family': ['Verdana', 'sans-serif'], # https://www.w3.org/Style/Examples/007/fonts.en.html
                    'fontSize': '16px'},
                    {
                    'if': {'column_id': 'Feature'},
                    'textAlign': 'left'}],
            style_cell={
                    'textAlign': 'center',
                    'border': '2px solid white',
                    'maxWidth': '50px',

                    'textOverflow': 'ellipsis'},
            style_as_list_view=True
    )
    return table

# Navigation Bar
PATH_logo = 'https://www.pinclipart.com/picdir/big/209-2095185_champions-league-logo-champions-league-football-logo-clipart.png'

navbar = dbc.Navbar(id='navbar', children=[
        dbc.Row([
                dbc.Col(html.Img(src=PATH_logo, height="60px")),
                dbc.Col(dbc.NavbarBrand("App Title", style={'color': 'black', 'fontSize': '25px'}))],
                align="center"), # no_gutters elimina los espacios feos y alinea todo
        dbc.Button(id='button', children="Log in", color="primary", className='ml-auto')
        ], dark=True, color='dark')

app.layout = dbc.Container([
        dbc.Row([dbc.Col([html.Div(id='parent', children=[navbar])], xl=12, lg=12, md=12, sm=12, xs=12)]),
        dbc.Row([dbc.Col([html.H2(id='H2', children=f'{player} Statistics')], xl=12, lg=12, md=12, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 30, 'marginBottom': 30}),
        dbc.Row([
                dbc.Col([html.Div(id='table_season', children=table(df_season))], xl=4, lg=4, md=4, sm=12, xs=12),
                dbc.Col([dcc.Graph(id='bar_plot', figure=bar_chart(df_player, 'Perf_Index_scaled', dict_layout))],
                        xl=4, lg=4, md=4, sm=12, xs=12),
                dbc.Col([dcc.Graph(id='line_plot', figure=line_chart(df_player, 'goals_total', dict_layout))],
                        xl=4, lg=4, md=4, sm=12, xs=12)]),
        dbc.Row([dbc.Col([html.H4(id='title_attack', children='Ataque')], xl=4, lg=4, md=4, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 30, 'marginBottom': 30}),
        dbc.Row([dbc.Col([html.Div(id='table_attack', children=table(df_attack))], xl=4, lg=4, md=4, sm=12, xs=12)]),
        dbc.Row([dbc.Col([html.H4(id='title_buildup', children='Creación de juego y 1-vs-1')], xl=4, lg=4, md=4, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 30, 'marginBottom': 30}),
        dbc.Row([dbc.Col([html.Div(id='table_buildup', children=table(df_buildup))], xl=4, lg=4, md=4, sm=12, xs=12)]),
        dbc.Row([dbc.Col([html.H4(id='title_defense', children='Defensa y Disciplina')], xl=4, lg=4, md=4, sm=12, xs=12)],
                style={'textAlign': 'left', 'marginTop': 30, 'marginBottom': 30}),
        dbc.Row([dbc.Col([html.Div(id='table_defense', children=table(df_defense))], xl=4, lg=4, md=4, sm=12, xs=12)]),

], fluid=True)

if __name__ == '__main__':
    app.run_server()

