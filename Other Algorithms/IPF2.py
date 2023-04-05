import numpy as np
import plotly.graph_objs as go
import  plotly as py
import plotly.express as px

import numpy as np

# census data
census_data = {'Male 24* Single': 105, 'Male 24* Married': 3, 'Male 24* Partner': 0, 'Male 24* Seperated': 0, 'Male 24* Divorced': 0, 'Male 24* Widowed': 0, 'Male 25-34 Single': 203, 'Male 25-34 Married': 100, 'Male 25-34 Partner': 0, 'Male 25-34 Seperated': 3, 'Male 25-34 Divorced': 3, 'Male 25-34 Widowed': 1, 'Female 24* Single': 175, 'Female 24* Married': 2, 'Female 24* Partner': 0, 'Female 24* Seperated': 2, 'Female 24* Divorced': 0, 'Female 24* Widowed': 0, 'Female 25-34 Single': 197, 'Female 25-34 Married': 50, 'Female 25-34 Partner': 3, 'Female 25-34 Seperated': 10, 'Female 25-34 Divorced': 15, 'Female 25-34 Widowed': 0}

# create initial population counts with random numbers
pop_data = {}
for k in census_data.keys():
    pop_data[k] = np.random.randint(low=0, high=100, size=1)[0]

# iterative proportional fitting
while True:
    # normalize the population counts to match the census data proportions
    total = sum(pop_data.values())
    for k in pop_data.keys():
        pop_data[k] = pop_data[k] / total * sum(census_data.values())

    # calculate the absolute difference between the current and census proportions
    diff = sum([abs(pop_data[k] - census_data[k]) for k in pop_data.keys()])
    print(diff)
    # stop if the difference is below a certain threshold
    if diff < 1:
        break
#
# # print the final population counts
# print(pop_data)


# fig = go.Figure()
# fig.add_trace(
#     go.Scatter(x0='data', name='actual', y=list(census_data.values()), line_color='#636EFA'))
# fig.add_trace(
#     go.Scatter(x0='data', name='pred', y=list(pop_data.values()), line_color='#EF553B'))
# fig.update_layout(width=1000, title='RMSE=' + str(self.RMSE()))
# py.offline.plot(fig, filename="plot.html")
# fig.show()

