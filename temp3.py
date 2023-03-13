import random
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

ages = ['0-4', '5-7', '8-9', '10-14', '15', '16-17', '18-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']
sexes = ['M', 'F']
import random
for i in range(0, 100):
    rnd = random.randrange(0, 10)
    print(rnd)

