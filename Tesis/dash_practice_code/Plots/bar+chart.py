# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 14:41:51 2020

@author: anmol
"""

import plotly.graph_objects as go
import plotly.express as px

from plotly.offline import init_notebook_mode,  plot
init_notebook_mode()


df = px.data.gapminder().query("country=='India'")
df2 = px.data.gapminder().query("country=='United States'")


fig = go.Figure([go.Bar(x = df['year'], y = df['gdpPercap'], marker_color = 'indianred',name = 'India'),
                 go.Bar(x = df2['year'], y = df2['gdpPercap'], marker_color = 'blue', name = 'US')
                 ])

fig.update_layout(title = 'GDP per capita over the years',
                  xaxis_title = 'Years',
                  yaxis_title = 'GDP per capita', 
                   barmode = 'group'
                  )

plot(fig)