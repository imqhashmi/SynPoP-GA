import random
import numpy as np
import geopandas as gpd
import pandas as pd
import os
import json
import plotly.express as px
import plotly as py
from Person import Person
import math
from collections import Counter
import plotly.graph_objs as go
import  plotly as py
import plotly.express as px
import itertools

def getkeys(df):
    groups = list(df.columns)[2:] #drop first two columns: areacode and total
    return groups

def get_weighted_samples(df, size):
    groups = list(df.columns)[2:] #drop first two columns: areacode and total
    values = df.values.flatten().tolist()[1:]
    total = values.pop(0)
    weights = [x / total for x in values]
    return np.random.choice(groups, size=size, replace=True, p=weights).tolist()

def get_weighted_samples_by_age_sex(df, age, sex, size):
    df = df[[col for col in df.columns if age in col]]
    df = df[[col for col in df.columns if sex in col]]
    groups = list(df.columns)
    values = df.values.flatten().tolist()
    total = sum(values)
    weights = [x / total for x in values]
    return np.random.choice(groups, size=size, replace=True, p=weights).tolist()

def get_weight(key, df):
    value = getdictionary(df).get(key)
    total = df.values.flatten().tolist()[1:].pop(0)
    return value/total

def getdictionary(df):
    if 'total' in df.columns:
        df = df.iloc[:, 1:] #drop total column
    dic = {}
    for index, row in df.iterrows():
        for index, column in enumerate(df.columns):
            if index==0:
                continue
            dic[column] = int(row[column])
    return dic

def plot(actual, predicted, rmse):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x0='data', name='actual', y=actual, line_color='#636EFA'))
    fig.add_trace(
        go.Scatter(x0='data', name='pred', y=predicted, line_color='#EF553B', opacity=0.6))
    fig.update_layout(width=1000, title='RMSE=' + str(rmse), showlegend=False)
    py.offline.plot(fig, filename="temp.html")
    fig.show()

def generate_combinations(left, right, total):
    # generate all possible combinations
    combinations = itertools.product(left, right)
    return [combo for combo in combinations if combo[0].split(' ')[:2] == combo[1].split(' ')[:2]]


path = os.path.join(os.path.dirname(os.getcwd()))

sex_by_age = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'crosstables', 'sex_by_age_5yrs.csv'))
sex_by_age = sex_by_age[sex_by_age['geography code'] == 'E02005949']
# d = getdictionary(sex_by_age)
# for key, value in d.items():
#     k = key.split(' ')
#     print("'" + k[1] + " " + k[0]+"':",value,",")
#
religion_by_sex_by_age = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'crosstables', 'religion_by_sex_by_age.csv'))
religion_by_sex_by_age = religion_by_sex_by_age[religion_by_sex_by_age['geography code'] == 'E02005949']
religion_by_sex_by_age = religion_by_sex_by_age.drop(columns=[col for col in religion_by_sex_by_age.columns if 'All' in col])

ethnic_by_sex_by_age = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'crosstables', 'ethnic_by_sex_by_age.csv'))
ethnic_by_sex_by_age = ethnic_by_sex_by_age[ethnic_by_sex_by_age['geography code'] == 'E02005949']


marital_by_sex_by_age = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'crosstables', 'marital_by_sex_by_age.csv'))
marital_by_sex_by_age = marital_by_sex_by_age[marital_by_sex_by_age['geography code'] == 'E02005949']

qualification_by_sex_by_age = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'crosstables', 'qualification_by_sex_by_age.csv'))
qualification_by_sex_by_age = qualification_by_sex_by_age[qualification_by_sex_by_age['geography code'] == 'E02005949']

# print(getdictionary(marital_by_sex_by_age))