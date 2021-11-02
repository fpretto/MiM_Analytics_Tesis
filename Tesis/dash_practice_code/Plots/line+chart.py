# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 13:37:32 2020

@author: anmol
"""

# line 

import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import init_notebook_mode,  plot
init_notebook_mode()


df = px.data.gapminder().query("country=='India'")
df2 = px.data.gapminder().query("country=='United States'")


fig = go.Figure(data = [go.Scatter(x = df['year'], y = df['lifeExp'],\
                                   line = dict(color = 'firebrick', width = 4), text = df['country'], name = 'India'),
                        go.Scatter(x = df2['year'], y = df2['lifeExp'],\
                                   line = dict(color = 'firebrick', width = 4), text = df2['country'], name = 'US')])

    
fig.update_layout(title='Life Expectency over the years',
                   xaxis_title='Years',
                   yaxis_title='Life Expectancy (years)',
                   )

plot(fig)

