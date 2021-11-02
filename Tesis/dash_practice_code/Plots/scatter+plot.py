# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 19:22:53 2020

@author: anmol
"""


import plotly.graph_objects as go
import plotly.express as px
from plotly.offline import init_notebook_mode,  plot
init_notebook_mode()


# what is query() - Query the columns of a DataFrame with a boolean expression.

df = px.data.gapminder().query("country=='India'")


df2 = px.data.gapminder().query("country=='United States'")


fig = go.Figure()

fig.add_trace(go.Scatter(x = df['year'], y = df['lifeExp'], mode = 'markers'))
fig.add_trace(go.Scatter(x = df2['year'], y = df2['lifeExp'], mode = 'lines'))

fig.update_layout(title='Life Expectency over the years',
                   xaxis_title='Years',
                   yaxis_title='Life Expectancy (years)',
                   )

plot(fig)