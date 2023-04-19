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

def getdictionary(df):
    if 'total' in df.columns:
        df = df.iloc[:, 1:] #drop total column
    dic = {}
    for index, row in df.iterrows():
        for index, column in enumerate(df.columns):
            if index==0:
                continue
            dic[column] = int(row[column])
    # return dict(sorted(dic.items()))
    return dic

def get_weighted_sample(df):
    groups = list(df.columns)[2:] #drop first two columns: areacode and total
    values = df.values.flatten().tolist()[1:]
    total = values.pop(0)
    weights = [x / total for x in values]
    # print(sum(weights))
    # get random values based on prob. distribution
    # result = [str(i) for i in list()]
    return np.random.choice(groups, size=1, replace=True, p=weights).tolist()[0]


def get_weighted_samples(df, size):
    groups = [col.strip() for col in list(df.columns)][2:] #drop first two columns: areacode and total
    values = df.values.flatten().tolist()[1:]
    total = values.pop(0)
    weights = [x / total for x in values]
    # print(sum(weights))
    # get random values based on prob. distribution
    return np.random.choice(groups, size=size, replace=True, p=weights).tolist()

def get_weighted_samples_by_age_sex(df, age, sex, size):
    print(df.columns)
    df = df[[col for col in df.columns if age in col]]
    df = df[[col for col in df.columns if sex in col]]
    groups = list(df.columns)
    values = df.values.flatten().tolist()
    total = sum(values)
    weights = [x / total for x in values]
    return np.random.choice(groups, size=size, replace=True, p=weights).tolist()


path = os.path.join(os.path.dirname(os.getcwd()))
# Read census data
agedf = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'individual', 'Age.csv'))
agedf = agedf[agedf['geography code'] == 'E02005949']
Total = agedf['total'].values[0]

age5ydf = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'individual', 'Age_5yrs.csv'))
age5ydf = age5ydf[age5ydf['geography code'] == 'E02005949']

sexdf = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'individual', 'Sex.csv'))
sexdf = sexdf[sexdf['geography code'] == 'E02005949']

ethnicdf = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'individual', 'Ethnic.csv'))
ethnicdf = ethnicdf[ethnicdf['geography code'] == 'E02005949']
ethnicdf = ethnicdf.drop(columns=[col for col in ethnicdf.columns if '0' in col]) #remove all category columns

religiondf = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'individual', 'Religion.csv'))
religiondf = religiondf[religiondf['geography code'] == 'E02005949']

mstatusdf = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'individual', 'Marital.csv'))
mstatusdf = mstatusdf[mstatusdf['geography code'] == 'E02005949']

qualdf = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'individual', 'Qualification.csv'))
qualdf = qualdf[qualdf['geography code'] == 'E02005949']


HHsizedf = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'individual', 'HH_size.csv'))
HHsizedf = HHsizedf[HHsizedf['geography code'] == 'E02005949']

HHcomdf = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'individual', 'HH_composition.csv'))
HHcomdf = HHcomdf[HHcomdf['geography code'] == 'E02005949']

HHtypedf = pd.read_csv(os.path.join(path, 'SPONGE', 'Census_2011_MSOA', 'individual', 'HH_type.csv'))
HHtypedf = HHtypedf[HHtypedf['geography code'] == 'E02005949']

