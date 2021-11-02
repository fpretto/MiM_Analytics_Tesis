# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 14:14:23 2020

@author: anmol
"""

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html


app = dash.Dash(external_stylesheets = [ dbc.themes.FLATLY],)


PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"


navbar = dbc.Navbar( id = 'navbar', children = [
    dbc.Row([
        dbc.Col(html.Img(src = PLOTLY_LOGO, height = "70px")),
        dbc.Col(
            dbc.NavbarBrand("App Title", style = {'color':'black', 'fontSize':'25px','fontFamily':'Times New Roman'}
                            )
            
            )
        
        
        ],align = "center",
        no_gutters = True),
    dbc.Button(id = 'button', children = "Click Me!", color = "primary", className = 'ml-auto')
    
    
    ])


app.layout = html.Div(id = 'parent', children = [navbar])


if __name__ == "__main__":
    app.run_server()



