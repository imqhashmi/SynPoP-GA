import random
import numpy as np
import pandas as pd
import plotly.express as px
import  plotly as py
import plotly.graph_objects as go

# import plotly.graph_objs as go
# import pandas as pd
#
# fig = px.bar(df, x="age_group", y="count", color="gender", barmode="group")
# fig.show()
#
# # # Create figure and plot
# # fig = go.Figure(data=[trace_male, trace_female], layout=layout)
# # py.offline.plot(fig, filename= "bar.html")
# # fig.show()
#
# ages = ['0-4', ' 5-7', ' 8-9', ' 10-14', '15', ' 16-17', ' 18-19', ' 20-24', ' 25-29', ' 30-34', ' 35-39', ' 40-44', ' 45-49', ' 50-54', ' 55-59', ' 60-64', ' 65-69', ' 70-74', ' 75-79', ' 80-84', ' 85+']
# result = []
# for age in ages:
#     result.append(age + " M")
#     result.append(age + " F")
# print(result)

# temp = []
# for gene in self.genes:
#     temp.append(gene.age + " " + gene.sex)
#
# predicted_sex_by_age_5yrs = Counter(temp)
# actual_sex_by_age_5yrs = ICT.get_dictionary(ICT.sex_by_age_5yrs)
#
# predicted = []
# actual = []
#
# keys = ['0-4 M', '0-4 F', '5-7 M', '5-7 F', '8-9 M', '8-9 F', '10-14 M', '10-14 F', '15 M', '15 F', '16-17 M', '16-17 F', '18-19 M', '18-19 F', '20-24 M', '20-24 F', '25-29 M', '25-29 F', '30-34 M', '30-34 F', '35-39 M', '35-39 F', '40-44 M', '40-44 F', '45-49 M', '45-49 F', '50-54 M', '50-54 F', '55-59 M', '55-59 F', '60-64 M', '60-64 F', '65-69 M', '65-69 F', '70-74 M', '70-74 F', '75-79 M', '75-79 F', '80-84 M', '80-84 F', '85+ M', '85+ F']
#
# for key in keys:
#     avalue = actual_sex_by_age_5yrs.get(key)
#     pvalue = predicted_sex_by_age_5yrs.get(key)
#     if pvalue==None:
#         pvalue=0
#
#     actual.append(avalue)
#     predicted.append(pvalue)

# dic = dict(filter(lambda item: c in item[0], dictionary.items()))

# ages = ['0-4', '5-7', '8-9', '10-14', '15', '16-17', '18-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
# sexes = ['M', 'F']
# import random
# for i in range(0, 100):
#     rnd = random.randrange(0, 10)
#     print(rnd)
#
# import  plotly as py
# import plotly.graph_objs as go
# trace1 = go.Bar(
#     x=['giraffes', 'orangutans', 'monkeys'],
#     y=[20, 14, 23],
#     name='SF Zoo'
# )
# trace2 = go.Bar(
#     x=['giraffes', 'orangutans', 'monkeys'],
#     y=[12, 18, 29],
#     name='LA Zoo'
# )
# data = [trace1, trace2]
# layout = go.Layout(
#     barmode='group'
# )
# fig = go.Figure(data=data, layout=layout)
# py.offline.plot(fig, filename="bar.html")
# fig.show()

# import plotly.express as px
# df = px.data.tips()
# fig = px.scatter(df, x="total_bill", y="tip", color="smoker",
#                  title="String 'smoker' values mean discrete colors")
#
# py.offline.plot(fig, filename="bar.html")
# fig.show()
#
# fig = go.Figure()
#
# # Add traces
# fig.add_trace(go.Scatter(x=random_x, y=random_y0,
#                     mode='markers',
#                     name='markers'))
# fig.add_trace(go.Scatter(x=random_x, y=random_y1,
#                     mode='lines+markers',
#                     name='lines+markers'))
# fig.add_trace(go.Scatter(x=random_x, y=random_y2,
#                     mode='lines',
#                     name='lines'))
#
# fig.show()
#
# import numpy as np
#
# def KL(a, b):
#     a = np.asarray(a, dtype=np.float)
#     b = np.asarray(b, dtype=np.float)
#
#     return np.sum(np.where(a != 0, a * np.log(a / b), 0))
#
#
# # [1.346112,1.337432,1.246655, 0]
# #  [1.033836,1.082015,1.117323, 0]
#
# values1 = [102, 2, 7, 1, 42, 0, 0, 56, 17, 0, 1]
# values2 = [54, 26, 72, 11, 1, 378, 26, 205, 92, 0, 0]
# print(KL(values1, values2))
#
# df = pd.DataFrame(dict(
#     x=list(range(0, len(self.actual))),
#     y1=list(self.actual.values()),
#     y2=list(self.predicted.values())
# ))

# p = [67, 53, 43, 47, 62, 151, 127, 119, 2, 29, 60, 340, 33, 24, 7, 7, 144, 68, 44, 97, 380, 38, 18, 140, 3, 29, 16, 74, 6, 59, 3, 113, 97, 38, 21, 205, 42, 196, 22, 63, 2, 111, 85, 35, 21, 54, 85, 30, 12, 27, 104, 73, 14, 48, 41, 180, 35, 30, 31, 2, 23, 23, 24, 35, 29, 27, 44, 210, 86, 8, 7, 43, 29, 171, 28, 7, 76, 3, 13, 11, 43, 8, 31, 44, 7, 4, 32, 37, 9, 18, 8, 4, 67, 16, 10, 62, 13, 10, 30, 28, 9, 17, 16, 4, 136, 6, 46, 28, 55, 111, 43, 10, 24, 25, 66, 24, 23, 105, 26, 29, 37, 7, 7, 3, 19, 57, 2, 35, 6, 1, 4, 5, 63, 23, 12, 3, 19, 13, 9, 8, 8, 8, 10, 6, 10, 11, 33, 6, 10, 1, 9, 12, 13, 4, 4, 14, 5, 3, 11, 1, 19, 5, 7, 24, 13, 6, 8, 5, 11, 18, 1, 2, 12, 6, 17, 17, 8, 7, 1, 1, 6, 1, 3, 1, 6, 13, 2, 1, 8, 14, 10, 1, 7, 8, 16, 11, 3, 6, 13, 6, 6, 2, 9, 1, 3, 1, 4, 3, 1, 2, 2, 3, 2, 2, 2, 3, 4, 2, 2, 4, 3, 3, 5, 1, 5, 2, 6, 2, 1, 1, 1, 1, 1, 3, 1, 1, 5, 4, 2, 1, 1, 1, 3, 6, 2, 1, 1, 1, 1, 4, 3, 1, 3, 4, 1, 1, 2, 1, 1, 2, 1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 2, 1, 2, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
# a= [102, 2, 7, 1, 42, 0, 0, 56, 17, 45, 0, 1, 0, 17, 0, 0, 25, 14, 44, 0, 1, 0, 10, 0, 0, 11, 1, 70, 2, 1, 0, 25, 1, 1, 32, 9, 13, 0, 0, 0, 1, 0, 0, 4, 2, 24, 0, 1, 0, 11, 0, 0, 21, 3, 99, 5, 4, 0, 25, 1, 3, 111, 22, 262, 10, 9, 7, 44, 3, 4, 287, 43, 140, 3, 11, 1, 39, 2, 2, 133, 34, 117, 13, 16, 2, 27, 0, 1, 103, 32, 89, 3, 12, 0, 28, 0, 2, 75, 12, 88, 2, 5, 0, 18, 1, 0, 65, 17, 71, 3, 2, 0, 18, 0, 1, 41, 11, 62, 0, 2, 0, 10, 2, 0, 29, 10, 82, 1, 1, 1, 6, 0, 1, 20, 6, 71, 1, 1, 0, 1, 0, 0, 24, 11, 53, 3, 0, 0, 3, 0, 0, 24, 8, 58, 1, 1, 0, 1, 0, 0, 11, 5, 42, 0, 0, 1, 0, 0, 0, 5, 1, 53, 0, 0, 0, 1, 0, 0, 7, 9, 40, 0, 0, 0, 0, 0, 0, 1, 7, 69, 3, 5, 0, 40, 0, 0, 77, 26, 31, 0, 3, 0, 16, 1, 0, 23, 6, 28, 2, 1, 0, 14, 0, 0, 11, 9, 78, 2, 5, 0, 23, 0, 0, 42, 4, 10, 0, 0, 0, 7, 0, 0, 5, 2, 19, 0, 0, 0, 5, 0, 1, 15, 6, 180, 4, 4, 2, 19, 1, 1, 154, 16, 362, 8, 18, 7, 55, 3, 8, 289, 41, 163, 3, 17, 0, 44, 7, 2, 125, 33, 156, 6, 12, 0, 29, 1, 0, 85, 17, 130, 2, 4, 0, 43, 1, 3, 54, 6, 91, 1, 3, 0, 10, 1, 3, 32, 8, 89, 1, 3, 1, 9, 1, 1, 35, 13, 87, 1, 3, 0, 4, 1, 0, 25, 12, 80, 5, 1, 0, 5, 0, 1, 30, 8, 81, 0, 2, 0, 4, 0, 2, 20, 14, 64, 0, 1, 1, 4, 0, 0, 12, 4, 61, 0, 0, 0, 1, 0, 0, 9, 14, 62, 1, 0, 0, 0, 0, 0, 3, 12, 84, 0, 0, 1, 0, 0, 0, 2, 8, 83, 0, 0, 0, 0, 0, 0, 3, 8]
# d = ['actual', 'pred']
# a = [(x,'actual') for x in a]
# p = [(x,'pred') for x in p]
# df = pd.DataFrame(a + p, columns=['data', 'group'])
# fig = px.violin(df, y="data", color="group", violinmode='overlay')

# fig = go.Figure()
#
# fig.add_trace(go.Violin(x0='data', name='actual', y=a, line_color='#636EFA',   side='negative'))
# fig.add_trace(go.Violin(x0='data',name='pred',  y=p,  line_color='#EF553B',   side='positive'))
#
# fig.update_traces(meanline_visible=True)
# fig.update_layout(width=1000, violinmode='overlay')
# py.offline.plot(fig, filename="bar.html")
# fig.show()