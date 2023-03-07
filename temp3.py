# import random
# import numpy as np
# import plotly.express as px
# import  plotly as py
#
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

ages = ['0-4', '5-7', '8-9', '10-14', '15', '16-17', '18-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
sexes = ['M', 'F']
import random
for i in range(0, 100):
    age = random.sample(ages, 1)[0]
    print(age)
