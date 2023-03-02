import random
import numpy as np
import geopandas as gpd
import pandas as pd
import os
import json
import plotly.express as px
import  plotly as py
import InputData as id
import InputCrossTables as ict
from Person import Person
import math
from collections import Counter

#Defining MAPE function
def MAPE(actual, predicted):
    actual = np.array(actual)
    predicted = np.array(predicted)
    mape = np.mean(np.abs((actual - predicted)/actual))*100
    return mape


actual = ict.get_dictionary(ict.sex_by_age_5yrs)
total = actual.pop('total')

plist = []
actual = id.agedf.values.flatten().tolist()[2:]
predicted = id.get_weighted_samples(id.agedf, len(actual))

c_pred = Counter(predicted)
c_act = Counter(actual)

print(c_act)
# for i in range(0, total):
#     p = Person(i+1, ages[i],sexes[i],'W1', 'C')
#     plist.append(p.getdic())
#
# persons = pd.DataFrame(plist)
# actual = {}
# predicted = {}
# groups = persons.groupby(['age','sex'])
# for name, group in groups:
#     predicted[name[0].strip() + " " +  name[1]] = group.size




# act = []
# pred = []
# for key, value in actual.items():
#     act.append(value)
#     pred.append(predicted.get(key))
#
# print(MAPE(list(c_act.values()), list(c_pred.values())))