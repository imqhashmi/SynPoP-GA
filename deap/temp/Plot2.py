import plotly.graph_objs as go
import  plotly as py
import numpy as np
from plotly.subplots import make_subplots

HH_sizes = {'1': 857, '2': 684, '3': 413, '4': 324, '5': 149, '6': 74, '7': 16, '8+': 10}
HH_types = {'person': 857, 'family': 1166, 'other': 504}
HH_compositions = {'1E_0C': 285, '1A_0C': 572, '1A_1C': 205, '2E_0C': 187, '2A_1C': 238, '2A_0C': 389, '2A_3C': 53,
                   '3A_1C': 118, '3A_0C': 480}
for key in HH_compositions.keys():
    print(key)
fig =  fig = make_subplots(rows=1, cols=3,
            subplot_titles=('Household Size', 'Household Type', 'Household Composition'),
                            horizontal_spacing = 0.05, vertical_spacing=  0.25,  print_grid=True)
fig.add_trace(go.Bar(x0='data',x=list(HH_sizes.keys()), name='Sizes', y=list(HH_sizes.values()), marker={'color':'#636EFA'}), row=1, col=1)
fig.add_trace(go.Bar(x0='data',x=list(HH_types.keys()), name='Types', y=list(HH_types.values()), marker={'color':'#EF553B'}, width=0.4), row=1, col=2)
fig.add_trace(go.Bar(x0='data',x=list(HH_compositions.keys()), name='Compositions', y=list(HH_compositions.values()), marker={'color':'#636EFA'}), row=1, col=3)
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
fig.update_layout(height = 300, showlegend=False)
py.offline.plot(fig, filename="plots2.html")
fig.show()