import streamlit as stm 
import pandas as pd
import plotly
import numpy as np

plotly.offline.init_notebook_mode()
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_us_ag_exports.csv')

data = [dict(type='choropleth',
             locations = df['code'].astype(str),
             z=df['total exports'].astype(float),
             locationmode='USA-states')]

# let's create some additional, random data
for i in range(5):
    data.append(data[0].copy())
    data[-1]['z'] = data[0]['z'] * np.random.rand(*data[0]['z'].shape)

# let's create the steps for the slider
steps = []
for i in range(len(data)):
    step = dict(method='restyle',
                args=['visible', [False] * len(data)],
                label='Year {}'.format(i + 1980))
    step['args'][1][i] = True
    steps.append(step)

sliders = [dict(active=0,
                pad={"t": 1},
                steps=steps)]    
layout = dict(geo=dict(scope='usa',
                       projection={'type': 'albers usa'}),
              sliders=sliders)

fig = dict(data=data, 
           layout=layout)
#plotly.offline.iplot(fig)


stm.plotly_chart(fig, use_container_width=True)