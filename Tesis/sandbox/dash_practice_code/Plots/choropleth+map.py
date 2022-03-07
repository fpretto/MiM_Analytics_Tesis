# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 23:02:19 2020

@author: anmol
"""

import plotly.express as px
from plotly.offline import init_notebook_mode,  plot
init_notebook_mode()


df = px.data.election()
geojson = px.data.election_geojson()


fig = px.choropleth(df, geojson = geojson, locations= 'district', featureidkey= "properties.district",
                    projection= "mercator", color = 'Bergeron')


fig.update_geos(fitbounds="locations", visible = False)


df = px.data.gapminder().query("year==2007")

fig = px.choropleth(df, locations="iso_alpha", color = "lifeExp", 
                    hover_name= "country",
                    projection="orthographic",
                    color_continuous_scale=px.colors.sequential.Plasma)

plot(fig)