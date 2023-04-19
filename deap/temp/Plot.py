import plotly.graph_objs as go
import  plotly as py
import numpy as np
from plotly.subplots import make_subplots

ages = {'0-4': 447, '5-7': 182, '8-9': 132, '10-14': 295, '15': 44, '16-17': 106, '18-19': 651, '20-24': 1460, '25-29': 759, '30-34': 617, '35-39': 464, '40-44': 345, '45-49': 300, '50-54': 248, '55-59': 248, '60-64': 232, '65-69': 177, '70-74': 162, '75-79': 127, '80-84': 165, '85+': 142}
sexes = {'M': 3473, 'F': 3830}
ethnicities = {'W1': 4225, 'W2': 73, 'W3': 1, 'W4': 797, 'M1': 76, 'M2': 40, 'M3': 71, 'M4': 78, 'A1': 365, 'A2': 282, 'A3': 112, 'A4': 201, 'A5': 379, 'B1': 322, 'B2': 98, 'B3': 53, 'O1': 75, 'O2': 55}
religions = {'C': 3633, 'B': 88, 'H': 157, 'J': 25, 'M': 659, 'S': 27, 'O': 37, 'N': 2136, 'NS': 541}
mstatuses = {'Single': 3727, 'Married': 1667, 'Partner': 13, 'Separated': 122, 'Divorced': 362, 'Widowed': 312}
qualifications = {'no': 1019, 'level1': 610, 'level2': 599, 'apprent': 106, 'level3': 1368, 'level4+': 1942, 'other': 559}

del ethnicities['W1']
ethnicities2 = {'W1':4225}

del religions['C']
religions2 = {'C':3633}

fig =  fig = make_subplots(rows=4, cols=2,
            subplot_titles=('Ages', 'Sex', 'Ethnicities', 'Dominant Ethnicity',  'Religions', 'Dominant Religion', 'Marital Status','Qualification'),
                            horizontal_spacing = 0.05, vertical_spacing=  0.15,  print_grid=True)
fig.add_trace(go.Bar(x0='data',x=list(ages.keys()), name='Ages', y=list(ages.values()), marker={'color':'#636EFA'}), row=1, col=1)
fig.add_trace(go.Bar(x0='data',x=list(sexes.keys()), name='Sexes', y=list(sexes.values()), marker={'color':'#EF553B'}, width=0.2), row=1, col=2)
fig.add_trace(go.Bar(x0='data',x=list(ethnicities.keys()), name='Ethnicities', y=list(ethnicities.values()), marker={'color':'#636EFA'}), row=2, col=1)
fig.add_trace(go.Bar(x0='data',x=list(ethnicities2.keys()), name='Dominant Ethnicity', y=list(ethnicities2.values()), marker={'color':'#636EFA'}, width = 0.1), row=2, col=2)

fig.add_trace(go.Bar(x0='data',x=list(religions.keys()), name='Religions', y=list(religions.values()), marker={'color':'#EF553B'}, width=0.4), row=3, col=1)
fig.add_trace(go.Bar(x0='data',x=list(religions2.keys()), name='Dominant Religion', y=list(religions2.values()), marker={'color':'#EF553B'}, width=0.1), row=3, col=2)

fig.add_trace(go.Bar(x0='data',x=list(mstatuses.keys()), name='Marital Status', y=list(mstatuses.values()), marker={'color':'#636EFA'}, width=0.4), row=4, col=1)
fig.add_trace(go.Bar(x0='data',x=list(qualifications.keys()), name='Qualification', y=list(qualifications.values()), marker={'color':'#EF553B'}), row=4, col=2)
# fig.add_trace(go.Scatter(x0='data', x=list(actual.keys()), name='pred', y=list(predicted.values()), line_color='#EF553B'))
fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True)
fig.update_layout(height= 600, showlegend=False)
py.offline.plot(fig, filename="plots.html")
fig.show()