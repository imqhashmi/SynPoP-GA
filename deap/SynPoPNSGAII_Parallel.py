import random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from deap import algorithms, base, creator, tools
from Person import Person
from collections import Counter
import plotly.graph_objs as go
import  plotly as py
import plotly.express as px
import cProfile
from scipy.integrate import trapz
import concurrent.futures
import multiprocessing
from functools import partial

def evaluate(individual):
    # fitness for sex_age
    fitness_sex_age = getfitness(individual,'sex_age')

    # fitness for sex_age_ethnicity
    fitness_sex_age_ethnicity = getfitness(individual, 'sex_age_ethnicity', SHIFT=True)

    # fitness for sex_age_religion
    fitness_sex_age_religion = getfitness(individual, 'sex_age_religion')

    # fitness for sex_age_marital_status
    fitness_sex_age_status = getfitness(individual, 'sex_age_status')

    # fitness for sex_age_qualification
    fitness_sex_age_qualification = getfitness(individual, 'sex_age_qualification')

    return fitness_sex_age, fitness_sex_age_ethnicity, fitness_sex_age_religion, \
           fitness_sex_age_status, fitness_sex_age_qualification

def shift_left(lst, n):
    """Shifts the elements of the list to the left by n positions."""
    return lst[n:] + lst[:n]

def plot(actual, predicted, name, width=1000, SHIFTLEFT=False):
    a = np.array(list(actual.values()))
    if SHIFTLEFT==True:
        p = np.array(shift_left(list(predicted.values()),1))
        y_pred = shift_left(list(predicted.values()), 1)
    else:
        p = np.array(list(predicted.values()))
        y_pred = list(predicted.values())

    rmse = np.sqrt(((p - a) ** 2).mean())


    fig = go.Figure()
    fig.add_trace(go.Scatter(x0='data', x=list(actual.keys()), name='actual', y=list(actual.values()), line_color='#636EFA'))
    fig.add_trace(go.Scatter(x0='data', x=list(predicted.keys()), name='pred', y=y_pred, line_color='#EF553B'))
    fig.update_layout(width=width, title=name + "  " + 'RMSE=' + str(rmse))
    py.offline.plot(fig, filename="graphs\\" + name + ".html")
    fig.show()

def reduce(dic: dict, percent, Total):
    for key in dic.keys():
        dic[key] = round(dic[key]*percent)
    dic_sum = sum(dic.values())
    diff = Total - dic_sum
    for i in range(diff):
        k = random.choice(list(dic.keys()))
        dic[k] +=1
    # print(sum(dic.values()))
    return dic

ages = {'0-4': 447, '5-7': 182, '8-9': 132, '10-14': 295, '15': 44, '16-17': 106, '18-19': 651, '20-24': 1460, '25-29': 759, '30-34': 617, '35-39': 464, '40-44': 345, '45-49': 300, '50-54': 248, '55-59': 248, '60-64': 232, '65-69': 177, '70-74': 162, '75-79': 127, '80-84': 165, '85+': 142}
sexes = {'M': 3473, 'F': 3830}
ethnicities = {'W1': 4225, 'W2': 73, 'W3': 1, 'W4': 797, 'M1': 76, 'M2': 40, 'M3': 71, 'M4': 78, 'A1': 365, 'A2': 282, 'A3': 112, 'A4': 201, 'A5': 379, 'B1': 322, 'B2': 98, 'B3': 53, 'O1': 75, 'O2': 55}
religions = {'C': 3633, 'B': 88, 'H': 157, 'J': 25, 'M': 659, 'S': 27, 'O': 37, 'N': 2136, 'NS': 541}
mstatuses = {'Single': 3727, 'Married': 1667, 'Partner': 13, 'Separated': 122, 'Divorced': 362, 'Widowed': 312}
qualifications = {'no': 1019, 'level1': 610, 'level2': 599, 'apprent': 106, 'level3': 1368, 'level4+': 1942, 'other': 559}


CROSS_TABLES = {}
CROSS_TABLES['sex_age'] = {'M 0-4': 227 , 'M 5-7': 102 , 'M 8-9': 67 , 'M 10-14': 141 , 'M 15': 20 , 'M 16-17': 60 , 'M 18-19': 270 , 'M 20-24': 669 , 'M 25-29': 365 , 'M 30-34': 311 , 'M 35-39': 221 , 'M 40-44': 196 , 'M 45-49': 147 , 'M 50-54': 115 , 'M 55-59': 118 , 'M 60-64': 109 , 'M 65-69': 91 , 'M 70-74': 77 , 'M 75-79': 49 , 'M 80-84': 70 , 'M 85+': 48 , 'F 0-4': 220 , 'F 5-7': 80 , 'F 8-9': 65 , 'F 10-14': 154 , 'F 15': 24 , 'F 16-17': 46 , 'F 18-19': 381 , 'F 20-24': 791 , 'F 25-29': 394 , 'F 30-34': 306 , 'F 35-39': 243 , 'F 40-44': 149 , 'F 45-49': 153 , 'F 50-54': 133 , 'F 55-59': 130 , 'F 60-64': 123 , 'F 65-69': 86 , 'F 70-74': 85 , 'F 75-79': 78 , 'F 80-84': 95 , 'F 85+': 94}
CROSS_TABLES['sex_age_ethnicity'] = {'M 0-4 W0': 93, 'M 0-4 W1': 0, 'M 0-4 W2': 0, 'M 0-4 W3': 14, 'M 0-4 M0': 3, 'M 0-4 M1': 3, 'M 0-4 M2': 9, 'M 0-4 M3': 13, 'M 0-4 A0': 17, 'M 0-4 A1': 14, 'M 0-4 A2': 10, 'M 0-4 A3': 0, 'M 0-4 A4': 25, 'M 0-4 B0': 19, 'M 0-4 B1': 1, 'M 0-4 B2': 2, 'M 0-4 O0': 1, 'M 0-4 O1': 3, 'M 5-7 W0': 41, 'M 5-7 W1': 0, 'M 5-7 W2': 0, 'M 5-7 W3': 5, 'M 5-7 M0': 0, 'M 5-7 M1': 2, 'M 5-7 M2': 3, 'M 5-7 M3': 2, 'M 5-7 A0': 9, 'M 5-7 A1': 7, 'M 5-7 A2': 5, 'M 5-7 A3': 0, 'M 5-7 A4': 9, 'M 5-7 B0': 8, 'M 5-7 B1': 1, 'M 5-7 B2': 6, 'M 5-7 O0': 3, 'M 5-7 O1': 1, 'M 8-9 W0': 33, 'M 8-9 W1': 0, 'M 8-9 W2': 0, 'M 8-9 W3': 4, 'M 8-9 M0': 0, 'M 8-9 M1': 0, 'M 8-9 M2': 1, 'M 8-9 M3': 2, 'M 8-9 A0': 5, 'M 8-9 A1': 4, 'M 8-9 A2': 4, 'M 8-9 A3': 0, 'M 8-9 A4': 2, 'M 8-9 B0': 6, 'M 8-9 B1': 1, 'M 8-9 B2': 2, 'M 8-9 O0': 2, 'M 8-9 O1': 1, 'M 10-14 W0': 70, 'M 10-14 W1': 0, 'M 10-14 W2': 0, 'M 10-14 W3': 6, 'M 10-14 M0': 2, 'M 10-14 M1': 1, 'M 10-14 M2': 2, 'M 10-14 M3': 6, 'M 10-14 A0': 7, 'M 10-14 A1': 14, 'M 10-14 A2': 8, 'M 10-14 A3': 1, 'M 10-14 A4': 13, 'M 10-14 B0': 3, 'M 10-14 B1': 2, 'M 10-14 B2': 4, 'M 10-14 O0': 1, 'M 10-14 O1': 1, 'M 15 W0': 13, 'M 15 W1': 0, 'M 15 W2': 0, 'M 15 W3': 0, 'M 15 M0': 1, 'M 15 M1': 2, 'M 15 M2': 0, 'M 15 M3': 1, 'M 15 A0': 0, 'M 15 A1': 1, 'M 15 A2': 0, 'M 15 A3': 0, 'M 15 A4': 0, 'M 15 B0': 2, 'M 15 B1': 0, 'M 15 B2': 0, 'M 15 O0': 0, 'M 15 O1': 0, 'M 16-17 W0': 34, 'M 16-17 W1': 0, 'M 16-17 W2': 0, 'M 16-17 W3': 4, 'M 16-17 M0': 0, 'M 16-17 M1': 0, 'M 16-17 M2': 0, 'M 16-17 M3': 1, 'M 16-17 A0': 5, 'M 16-17 A1': 6, 'M 16-17 A2': 2, 'M 16-17 A3': 1, 'M 16-17 A4': 4, 'M 16-17 B0': 1, 'M 16-17 B1': 0, 'M 16-17 B2': 2, 'M 16-17 O0': 0, 'M 16-17 O1': 0, 'M 18-19 W0': 171, 'M 18-19 W1': 1, 'M 18-19 W2': 0, 'M 18-19 W3': 30, 'M 18-19 M0': 1, 'M 18-19 M1': 2, 'M 18-19 M2': 4, 'M 18-19 M3': 1, 'M 18-19 A0': 6, 'M 18-19 A1': 6, 'M 18-19 A2': 4, 'M 18-19 A3': 17, 'M 18-19 A4': 4, 'M 18-19 B0': 12, 'M 18-19 B1': 5, 'M 18-19 B2': 0, 'M 18-19 O0': 6, 'M 18-19 O1': 0, 'M 20-24 W0': 404, 'M 20-24 W1': 9, 'M 20-24 W2': 1, 'M 20-24 W3': 89, 'M 20-24 M0': 8, 'M 20-24 M1': 7, 'M 20-24 M2': 7, 'M 20-24 M3': 7, 'M 20-24 A0': 18, 'M 20-24 A1': 13, 'M 20-24 A2': 5, 'M 20-24 A3': 38, 'M 20-24 A4': 16, 'M 20-24 B0': 31, 'M 20-24 B1': 3, 'M 20-24 B2': 1, 'M 20-24 O0': 8, 'M 20-24 O1': 4, 'M 25-29 W0': 157, 'M 25-29 W1': 7, 'M 25-29 W2': 0, 'M 25-29 W3': 83, 'M 25-29 M0': 1, 'M 25-29 M1': 1, 'M 25-29 M2': 0, 'M 25-29 M3': 1, 'M 25-29 A0': 19, 'M 25-29 A1': 28, 'M 25-29 A2': 5, 'M 25-29 A3': 22, 'M 25-29 A4': 11, 'M 25-29 B0': 12, 'M 25-29 B1': 1, 'M 25-29 B2': 0, 'M 25-29 O0': 9, 'M 25-29 O1': 8, 'M 30-34 W0': 135, 'M 30-34 W1': 2, 'M 30-34 W2': 0, 'M 30-34 W3': 68, 'M 30-34 M0': 3, 'M 30-34 M1': 0, 'M 30-34 M2': 1, 'M 30-34 M3': 1, 'M 30-34 A0': 22, 'M 30-34 A1': 13, 'M 30-34 A2': 7, 'M 30-34 A3': 11, 'M 30-34 A4': 23, 'M 30-34 B0': 17, 'M 30-34 B1': 1, 'M 30-34 B2': 2, 'M 30-34 O0': 1, 'M 30-34 O1': 4, 'M 35-39 W0': 95, 'M 35-39 W1': 1, 'M 35-39 W2': 0, 'M 35-39 W3': 31, 'M 35-39 M0': 1, 'M 35-39 M1': 0, 'M 35-39 M2': 2, 'M 35-39 M3': 1, 'M 35-39 A0': 22, 'M 35-39 A1': 10, 'M 35-39 A2': 2, 'M 35-39 A3': 7, 'M 35-39 A4': 28, 'M 35-39 B0': 10, 'M 35-39 B1': 2, 'M 35-39 B2': 0, 'M 35-39 O0': 5, 'M 35-39 O1': 4, 'M 40-44 W0': 105, 'M 40-44 W1': 0, 'M 40-44 W2': 0, 'M 40-44 W3': 18, 'M 40-44 M0': 0, 'M 40-44 M1': 0, 'M 40-44 M2': 0, 'M 40-44 M3': 1, 'M 40-44 A0': 19, 'M 40-44 A1': 9, 'M 40-44 A2': 5, 'M 40-44 A3': 0, 'M 40-44 A4': 11, 'M 40-44 B0': 15, 'M 40-44 B1': 9, 'M 40-44 B2': 2, 'M 40-44 O0': 2, 'M 40-44 O1': 0, 'M 45-49 W0': 91, 'M 45-49 W1': 0, 'M 45-49 W2': 0, 'M 45-49 W3': 10, 'M 45-49 M0': 0, 'M 45-49 M1': 0, 'M 45-49 M2': 0, 'M 45-49 M3': 0, 'M 45-49 A0': 7, 'M 45-49 A1': 10, 'M 45-49 A2': 3, 'M 45-49 A3': 0, 'M 45-49 A4': 7, 'M 45-49 B0': 4, 'M 45-49 B1': 4, 'M 45-49 B2': 7, 'M 45-49 O0': 4, 'M 45-49 O1': 0, 'M 50-54 W0': 76, 'M 50-54 W1': 0, 'M 50-54 W2': 0, 'M 50-54 W3': 10, 'M 50-54 M0': 0, 'M 50-54 M1': 1, 'M 50-54 M2': 1, 'M 50-54 M3': 0, 'M 50-54 A0': 9, 'M 50-54 A1': 1, 'M 50-54 A2': 1, 'M 50-54 A3': 0, 'M 50-54 A4': 3, 'M 50-54 B0': 6, 'M 50-54 B1': 2, 'M 50-54 B2': 2, 'M 50-54 O0': 2, 'M 50-54 O1': 1, 'M 55-59 W0': 99, 'M 55-59 W1': 1, 'M 55-59 W2': 0, 'M 55-59 W3': 5, 'M 55-59 M0': 0, 'M 55-59 M1': 1, 'M 55-59 M2': 0, 'M 55-59 M3': 0, 'M 55-59 A0': 1, 'M 55-59 A1': 4, 'M 55-59 A2': 0, 'M 55-59 A3': 0, 'M 55-59 A4': 1, 'M 55-59 B0': 4, 'M 55-59 B1': 0, 'M 55-59 B2': 2, 'M 55-59 O0': 0, 'M 55-59 O1': 0, 'M 60-64 W0': 99, 'M 60-64 W1': 2, 'M 60-64 W2': 0, 'M 60-64 W3': 1, 'M 60-64 M0': 0, 'M 60-64 M1': 0, 'M 60-64 M2': 0, 'M 60-64 M3': 0, 'M 60-64 A0': 1, 'M 60-64 A1': 1, 'M 60-64 A2': 0, 'M 60-64 A3': 4, 'M 60-64 A4': 0, 'M 60-64 B0': 0, 'M 60-64 B1': 0, 'M 60-64 B2': 1, 'M 60-64 O0': 0, 'M 60-64 O1': 0, 'M 65-69 W0': 74, 'M 65-69 W1': 3, 'M 65-69 W2': 0, 'M 65-69 W3': 4, 'M 65-69 M0': 0, 'M 65-69 M1': 0, 'M 65-69 M2': 0, 'M 65-69 M3': 0, 'M 65-69 A0': 0, 'M 65-69 A1': 3, 'M 65-69 A2': 0, 'M 65-69 A3': 1, 'M 65-69 A4': 3, 'M 65-69 B0': 1, 'M 65-69 B1': 2, 'M 65-69 B2': 0, 'M 65-69 O0': 0, 'M 65-69 O1': 0, 'M 70-74 W0': 68, 'M 70-74 W1': 4, 'M 70-74 W2': 0, 'M 70-74 W3': 1, 'M 70-74 M0': 1, 'M 70-74 M1': 0, 'M 70-74 M2': 0, 'M 70-74 M3': 0, 'M 70-74 A0': 0, 'M 70-74 A1': 0, 'M 70-74 A2': 0, 'M 70-74 A3': 1, 'M 70-74 A4': 1, 'M 70-74 B0': 0, 'M 70-74 B1': 1, 'M 70-74 B2': 0, 'M 70-74 O0': 0, 'M 70-74 O1': 0, 'M 75-79 W0': 45, 'M 75-79 W1': 1, 'M 75-79 W2': 0, 'M 75-79 W3': 1, 'M 75-79 M0': 0, 'M 75-79 M1': 0, 'M 75-79 M2': 0, 'M 75-79 M3': 0, 'M 75-79 A0': 0, 'M 75-79 A1': 0, 'M 75-79 A2': 0, 'M 75-79 A3': 0, 'M 75-79 A4': 0, 'M 75-79 B0': 0, 'M 75-79 B1': 2, 'M 75-79 B2': 0, 'M 75-79 O0': 0, 'M 75-79 O1': 0, 'M 80-84 W0': 63, 'M 80-84 W1': 2, 'M 80-84 W2': 0, 'M 80-84 W3': 0, 'M 80-84 M0': 0, 'M 80-84 M1': 0, 'M 80-84 M2': 0, 'M 80-84 M3': 0, 'M 80-84 A0': 1, 'M 80-84 A1': 2, 'M 80-84 A2': 0, 'M 80-84 A3': 0, 'M 80-84 A4': 1, 'M 80-84 B0': 0, 'M 80-84 B1': 0, 'M 80-84 B2': 0, 'M 80-84 O0': 0, 'M 80-84 O1': 1, 'M 85+ W0': 42, 'M 85+ W1': 3, 'M 85+ W2': 0, 'M 85+ W3': 0, 'M 85+ M0': 0, 'M 85+ M1': 0, 'M 85+ M2': 0, 'M 85+ M3': 0, 'M 85+ A0': 0, 'M 85+ A1': 0, 'M 85+ A2': 0, 'M 85+ A3': 0, 'M 85+ A4': 0, 'M 85+ B0': 0, 'M 85+ B1': 3, 'M 85+ B2': 0, 'M 85+ O0': 0, 'M 85+ O1': 0, 'F 0-4 W0': 99, 'F 0-4 W1': 0, 'F 0-4 W2': 0, 'F 0-4 W3': 12, 'F 0-4 M0': 7, 'F 0-4 M1': 2, 'F 0-4 M2': 11, 'F 0-4 M3': 5, 'F 0-4 A0': 21, 'F 0-4 A1': 19, 'F 0-4 A2': 4, 'F 0-4 A3': 1, 'F 0-4 A4': 23, 'F 0-4 B0': 9, 'F 0-4 B1': 2, 'F 0-4 B2': 0, 'F 0-4 O0': 4, 'F 0-4 O1': 1, 'F 5-7 W0': 33, 'F 5-7 W1': 1, 'F 5-7 W2': 0, 'F 5-7 W3': 2, 'F 5-7 M0': 4, 'F 5-7 M1': 2, 'F 5-7 M2': 7, 'F 5-7 M3': 2, 'F 5-7 A0': 9, 'F 5-7 A1': 6, 'F 5-7 A2': 3, 'F 5-7 A3': 0, 'F 5-7 A4': 5, 'F 5-7 B0': 5, 'F 5-7 B1': 0, 'F 5-7 B2': 0, 'F 5-7 O0': 1, 'F 5-7 O1': 0, 'F 8-9 W0': 20, 'F 8-9 W1': 0, 'F 8-9 W2': 0, 'F 8-9 W3': 3, 'F 8-9 M0': 5, 'F 8-9 M1': 0, 'F 8-9 M2': 0, 'F 8-9 M3': 2, 'F 8-9 A0': 6, 'F 8-9 A1': 6, 'F 8-9 A2': 2, 'F 8-9 A3': 0, 'F 8-9 A4': 4, 'F 8-9 B0': 9, 'F 8-9 B1': 0, 'F 8-9 B2': 7, 'F 8-9 O0': 1, 'F 8-9 O1': 0, 'F 10-14 W0': 75, 'F 10-14 W1': 0, 'F 10-14 W2': 0, 'F 10-14 W3': 11, 'F 10-14 M0': 6, 'F 10-14 M1': 2, 'F 10-14 M2': 1, 'F 10-14 M3': 3, 'F 10-14 A0': 5, 'F 10-14 A1': 13, 'F 10-14 A2': 4, 'F 10-14 A3': 1, 'F 10-14 A4': 12, 'F 10-14 B0': 11, 'F 10-14 B1': 5, 'F 10-14 B2': 1, 'F 10-14 O0': 0, 'F 10-14 O1': 4, 'F 15 W0': 10, 'F 15 W1': 0, 'F 15 W2': 0, 'F 15 W3': 1, 'F 15 M0': 0, 'F 15 M1': 0, 'F 15 M2': 1, 'F 15 M3': 0, 'F 15 A0': 0, 'F 15 A1': 3, 'F 15 A2': 1, 'F 15 A3': 0, 'F 15 A4': 4, 'F 15 B0': 1, 'F 15 B1': 2, 'F 15 B2': 0, 'F 15 O0': 0, 'F 15 O1': 1, 'F 16-17 W0': 24, 'F 16-17 W1': 0, 'F 16-17 W2': 0, 'F 16-17 W3': 2, 'F 16-17 M0': 1, 'F 16-17 M1': 0, 'F 16-17 M2': 0, 'F 16-17 M3': 3, 'F 16-17 A0': 3, 'F 16-17 A1': 5, 'F 16-17 A2': 2, 'F 16-17 A3': 2, 'F 16-17 A4': 2, 'F 16-17 B0': 1, 'F 16-17 B1': 1, 'F 16-17 B2': 0, 'F 16-17 O0': 0, 'F 16-17 O1': 0, 'F 18-19 W0': 277, 'F 18-19 W1': 0, 'F 18-19 W2': 0, 'F 18-19 W3': 35, 'F 18-19 M0': 3, 'F 18-19 M1': 1, 'F 18-19 M2': 5, 'F 18-19 M3': 0, 'F 18-19 A0': 8, 'F 18-19 A1': 8, 'F 18-19 A2': 1, 'F 18-19 A3': 8, 'F 18-19 A4': 10, 'F 18-19 B0': 15, 'F 18-19 B1': 3, 'F 18-19 B2': 0, 'F 18-19 O0': 4, 'F 18-19 O1': 3, 'F 20-24 W0': 457, 'F 20-24 W1': 9, 'F 20-24 W2': 0, 'F 20-24 W3': 103, 'F 20-24 M0': 13, 'F 20-24 M1': 1, 'F 20-24 M2': 7, 'F 20-24 M3': 9, 'F 20-24 A0': 36, 'F 20-24 A1': 12, 'F 20-24 A2': 4, 'F 20-24 A3': 37, 'F 20-24 A4': 39, 'F 20-24 B0': 41, 'F 20-24 B1': 11, 'F 20-24 B2': 2, 'F 20-24 O0': 7, 'F 20-24 O1': 3, 'F 25-29 W0': 162, 'F 25-29 W1': 5, 'F 25-29 W2': 0, 'F 25-29 W3': 78, 'F 25-29 M0': 9, 'F 25-29 M1': 1, 'F 25-29 M2': 6, 'F 25-29 M3': 3, 'F 25-29 A0': 29, 'F 25-29 A1': 14, 'F 25-29 A2': 8, 'F 25-29 A3': 20, 'F 25-29 A4': 24, 'F 25-29 B0': 13, 'F 25-29 B1': 9, 'F 25-29 B2': 5, 'F 25-29 O0': 5, 'F 25-29 O1': 3, 'F 30-34 W0': 128, 'F 30-34 W1': 3, 'F 30-34 W2': 0, 'F 30-34 W3': 59, 'F 30-34 M0': 0, 'F 30-34 M1': 4, 'F 30-34 M2': 2, 'F 30-34 M3': 2, 'F 30-34 A0': 26, 'F 30-34 A1': 16, 'F 30-34 A2': 4, 'F 30-34 A3': 8, 'F 30-34 A4': 27, 'F 30-34 B0': 16, 'F 30-34 B1': 3, 'F 30-34 B2': 1, 'F 30-34 O0': 1, 'F 30-34 O1': 6, 'F 35-39 W0': 86, 'F 35-39 W1': 2, 'F 35-39 W2': 0, 'F 35-39 W3': 39, 'F 35-39 M0': 0, 'F 35-39 M1': 1, 'F 35-39 M2': 0, 'F 35-39 M3': 3, 'F 35-39 A0': 20, 'F 35-39 A1': 12, 'F 35-39 A2': 11, 'F 35-39 A3': 5, 'F 35-39 A4': 34, 'F 35-39 B0': 19, 'F 35-39 B1': 4, 'F 35-39 B2': 0, 'F 35-39 O0': 3, 'F 35-39 O1': 4, 'F 40-44 W0': 78, 'F 40-44 W1': 0, 'F 40-44 W2': 0, 'F 40-44 W3': 13, 'F 40-44 M0': 3, 'F 40-44 M1': 3, 'F 40-44 M2': 1, 'F 40-44 M3': 3, 'F 40-44 A0': 10, 'F 40-44 A1': 6, 'F 40-44 A2': 2, 'F 40-44 A3': 3, 'F 40-44 A4': 12, 'F 40-44 B0': 12, 'F 40-44 B1': 1, 'F 40-44 B2': 2, 'F 40-44 O0': 0, 'F 40-44 O1': 0, 'F 45-49 W0': 90, 'F 45-49 W1': 0, 'F 45-49 W2': 0, 'F 45-49 W3': 13, 'F 45-49 M0': 1, 'F 45-49 M1': 3, 'F 45-49 M2': 0, 'F 45-49 M3': 1, 'F 45-49 A0': 12, 'F 45-49 A1': 3, 'F 45-49 A2': 3, 'F 45-49 A3': 2, 'F 45-49 A4': 12, 'F 45-49 B0': 4, 'F 45-49 B1': 6, 'F 45-49 B2': 0, 'F 45-49 O0': 3, 'F 45-49 O1': 0, 'F 50-54 W0': 91, 'F 50-54 W1': 1, 'F 50-54 W2': 0, 'F 50-54 W3': 10, 'F 50-54 M0': 2, 'F 50-54 M1': 0, 'F 50-54 M2': 0, 'F 50-54 M3': 4, 'F 50-54 A0': 5, 'F 50-54 A1': 4, 'F 50-54 A2': 0, 'F 50-54 A3': 2, 'F 50-54 A4': 2, 'F 50-54 B0': 9, 'F 50-54 B1': 2, 'F 50-54 B2': 0, 'F 50-54 O0': 0, 'F 50-54 O1': 1, 'F 55-59 W0': 107, 'F 55-59 W1': 2, 'F 55-59 W2': 0, 'F 55-59 W3': 5, 'F 55-59 M0': 0, 'F 55-59 M1': 0, 'F 55-59 M2': 0, 'F 55-59 M3': 0, 'F 55-59 A0': 2, 'F 55-59 A1': 3, 'F 55-59 A2': 0, 'F 55-59 A3': 3, 'F 55-59 A4': 4, 'F 55-59 B0': 3, 'F 55-59 B1': 0, 'F 55-59 B2': 0, 'F 55-59 O0': 1, 'F 55-59 O1': 0, 'F 60-64 W0': 96, 'F 60-64 W1': 5, 'F 60-64 W2': 0, 'F 60-64 W3': 6, 'F 60-64 M0': 0, 'F 60-64 M1': 0, 'F 60-64 M2': 0, 'F 60-64 M3': 0, 'F 60-64 A0': 4, 'F 60-64 A1': 3, 'F 60-64 A2': 0, 'F 60-64 A3': 3, 'F 60-64 A4': 2, 'F 60-64 B0': 2, 'F 60-64 B1': 2, 'F 60-64 B2': 0, 'F 60-64 O0': 0, 'F 60-64 O1': 0, 'F 65-69 W0': 71, 'F 65-69 W1': 1, 'F 65-69 W2': 0, 'F 65-69 W3': 3, 'F 65-69 M0': 1, 'F 65-69 M1': 0, 'F 65-69 M2': 0, 'F 65-69 M3': 0, 'F 65-69 A0': 1, 'F 65-69 A1': 2, 'F 65-69 A2': 1, 'F 65-69 A3': 1, 'F 65-69 A4': 0, 'F 65-69 B0': 0, 'F 65-69 B1': 4, 'F 65-69 B2': 0, 'F 65-69 O0': 1, 'F 65-69 O1': 0, 'F 70-74 W0': 69, 'F 70-74 W1': 2, 'F 70-74 W2': 0, 'F 70-74 W3': 7, 'F 70-74 M0': 0, 'F 70-74 M1': 0, 'F 70-74 M2': 0, 'F 70-74 M3': 0, 'F 70-74 A0': 0, 'F 70-74 A1': 1, 'F 70-74 A2': 1, 'F 70-74 A3': 2, 'F 70-74 A4': 0, 'F 70-74 B0': 0, 'F 70-74 B1': 2, 'F 70-74 B2': 0, 'F 70-74 O0': 0, 'F 70-74 O1': 1, 'F 75-79 W0': 69, 'F 75-79 W1': 4, 'F 75-79 W2': 0, 'F 75-79 W3': 3, 'F 75-79 M0': 0, 'F 75-79 M1': 0, 'F 75-79 M2': 0, 'F 75-79 M3': 0, 'F 75-79 A0': 0, 'F 75-79 A1': 0, 'F 75-79 A2': 0, 'F 75-79 A3': 0, 'F 75-79 A4': 1, 'F 75-79 B0': 0, 'F 75-79 B1': 0, 'F 75-79 B2': 1, 'F 75-79 O0': 0, 'F 75-79 O1': 0, 'F 80-84 W0': 90, 'F 80-84 W1': 0, 'F 80-84 W2': 0, 'F 80-84 W3': 3, 'F 80-84 M0': 0, 'F 80-84 M1': 0, 'F 80-84 M2': 0, 'F 80-84 M3': 1, 'F 80-84 A0': 0, 'F 80-84 A1': 0, 'F 80-84 A2': 0, 'F 80-84 A3': 0, 'F 80-84 A4': 0, 'F 80-84 B0': 0, 'F 80-84 B1': 0, 'F 80-84 B2': 1, 'F 80-84 O0': 0, 'F 80-84 O1': 0, 'F 85+ W0': 85, 'F 85+ W1': 2, 'F 85+ W2': 0, 'F 85+ W3': 5, 'F 85+ M0': 0, 'F 85+ M1': 0, 'F 85+ M2': 0, 'F 85+ M3': 0, 'F 85+ A0': 0, 'F 85+ A1': 0, 'F 85+ A2': 0, 'F 85+ A3': 0, 'F 85+ A4': 0, 'F 85+ B0': 1, 'F 85+ B1': 1, 'F 85+ B2': 0, 'F 85+ O0': 0, 'F 85+ O1': 0}
CROSS_TABLES['sex_age_religion'] = {'M 0-4 C': 102, 'M 0-4 B': 2, 'M 0-4 H': 7, 'M 0-4 J': 1, 'M 0-4 M': 42, 'M 0-4 S': 0, 'M 0-4 OR': 0, 'M 0-4 NR': 56, 'M 0-4 NS': 17, 'M 5-7 C': 45, 'M 5-7 B': 0, 'M 5-7 H': 1, 'M 5-7 J': 0, 'M 5-7 M': 17, 'M 5-7 S': 0, 'M 5-7 OR': 0, 'M 5-7 NR': 25, 'M 5-7 NS': 14, 'M 8-9 C': 44, 'M 8-9 B': 0, 'M 8-9 H': 1, 'M 8-9 J': 0, 'M 8-9 M': 10, 'M 8-9 S': 0, 'M 8-9 OR': 0, 'M 8-9 NR': 11, 'M 8-9 NS': 1, 'M 10-14 C': 70, 'M 10-14 B': 2, 'M 10-14 H': 1, 'M 10-14 J': 0, 'M 10-14 M': 25, 'M 10-14 S': 1, 'M 10-14 OR': 1, 'M 10-14 NR': 32, 'M 10-14 NS': 9, 'M 15 C': 13, 'M 15 B': 0, 'M 15 H': 0, 'M 15 J': 0, 'M 15 M': 1, 'M 15 S': 0, 'M 15 OR': 0, 'M 15 NR': 4, 'M 15 NS': 2, 'M 16-17 C': 24, 'M 16-17 B': 0, 'M 16-17 H': 1, 'M 16-17 J': 0, 'M 16-17 M': 11, 'M 16-17 S': 0, 'M 16-17 OR': 0, 'M 16-17 NR': 21, 'M 16-17 NS': 3, 'M 18-19 C': 99, 'M 18-19 B': 5, 'M 18-19 H': 4, 'M 18-19 J': 0, 'M 18-19 M': 25, 'M 18-19 S': 1, 'M 18-19 OR': 3, 'M 18-19 NR': 111, 'M 18-19 NS': 22, 'M 20-24 C': 262, 'M 20-24 B': 10, 'M 20-24 H': 9, 'M 20-24 J': 7, 'M 20-24 M': 44, 'M 20-24 S': 3, 'M 20-24 OR': 4, 'M 20-24 NR': 287, 'M 20-24 NS': 43, 'M 25-29 C': 140, 'M 25-29 B': 3, 'M 25-29 H': 11, 'M 25-29 J': 1, 'M 25-29 M': 39, 'M 25-29 S': 2, 'M 25-29 OR': 2, 'M 25-29 NR': 133, 'M 25-29 NS': 34, 'M 30-34 C': 117, 'M 30-34 B': 13, 'M 30-34 H': 16, 'M 30-34 J': 2, 'M 30-34 M': 27, 'M 30-34 S': 0, 'M 30-34 OR': 1, 'M 30-34 NR': 103, 'M 30-34 NS': 32, 'M 35-39 C': 89, 'M 35-39 B': 3, 'M 35-39 H': 12, 'M 35-39 J': 0, 'M 35-39 M': 28, 'M 35-39 S': 0, 'M 35-39 OR': 2, 'M 35-39 NR': 75, 'M 35-39 NS': 12, 'M 40-44 C': 88, 'M 40-44 B': 2, 'M 40-44 H': 5, 'M 40-44 J': 0, 'M 40-44 M': 18, 'M 40-44 S': 1, 'M 40-44 OR': 0, 'M 40-44 NR': 65, 'M 40-44 NS': 17, 'M 45-49 C': 71, 'M 45-49 B': 3, 'M 45-49 H': 2, 'M 45-49 J': 0, 'M 45-49 M': 18, 'M 45-49 S': 0, 'M 45-49 OR': 1, 'M 45-49 NR': 41, 'M 45-49 NS': 11, 'M 50-54 C': 62, 'M 50-54 B': 0, 'M 50-54 H': 2, 'M 50-54 J': 0, 'M 50-54 M': 10, 'M 50-54 S': 2, 'M 50-54 OR': 0, 'M 50-54 NR': 29, 'M 50-54 NS': 10, 'M 55-59 C': 82, 'M 55-59 B': 1, 'M 55-59 H': 1, 'M 55-59 J': 1, 'M 55-59 M': 6, 'M 55-59 S': 0, 'M 55-59 OR': 1, 'M 55-59 NR': 20, 'M 55-59 NS': 6, 'M 60-64 C': 71, 'M 60-64 B': 1, 'M 60-64 H': 1, 'M 60-64 J': 0, 'M 60-64 M': 1, 'M 60-64 S': 0, 'M 60-64 OR': 0, 'M 60-64 NR': 24, 'M 60-64 NS': 11, 'M 65-69 C': 53, 'M 65-69 B': 3, 'M 65-69 H': 0, 'M 65-69 J': 0, 'M 65-69 M': 3, 'M 65-69 S': 0, 'M 65-69 OR': 0, 'M 65-69 NR': 24, 'M 65-69 NS': 8, 'M 70-74 C': 58, 'M 70-74 B': 1, 'M 70-74 H': 1, 'M 70-74 J': 0, 'M 70-74 M': 1, 'M 70-74 S': 0, 'M 70-74 OR': 0, 'M 70-74 NR': 11, 'M 70-74 NS': 5, 'M 75-79 C': 42, 'M 75-79 B': 0, 'M 75-79 H': 0, 'M 75-79 J': 1, 'M 75-79 M': 0, 'M 75-79 S': 0, 'M 75-79 OR': 0, 'M 75-79 NR': 5, 'M 75-79 NS': 1, 'M 80-84 C': 53, 'M 80-84 B': 0, 'M 80-84 H': 0, 'M 80-84 J': 0, 'M 80-84 M': 1, 'M 80-84 S': 0, 'M 80-84 OR': 0, 'M 80-84 NR': 7, 'M 80-84 NS': 9, 'M 85+ C': 40, 'M 85+ B': 0, 'M 85+ H': 0, 'M 85+ J': 0, 'M 85+ M': 0, 'M 85+ S': 0, 'M 85+ OR': 0, 'M 85+ NR': 1, 'M 85+ NS': 7, 'F 0-4 C': 69, 'F 0-4 B': 3, 'F 0-4 H': 5, 'F 0-4 J': 0, 'F 0-4 M': 40, 'F 0-4 S': 0, 'F 0-4 OR': 0, 'F 0-4 NR': 77, 'F 0-4 NS': 26, 'F 5-7 C': 31, 'F 5-7 B': 0, 'F 5-7 H': 3, 'F 5-7 J': 0, 'F 5-7 M': 16, 'F 5-7 S': 1, 'F 5-7 OR': 0, 'F 5-7 NR': 23, 'F 5-7 NS': 6, 'F 8-9 C': 28, 'F 8-9 B': 2, 'F 8-9 H': 1, 'F 8-9 J': 0, 'F 8-9 M': 14, 'F 8-9 S': 0, 'F 8-9 OR': 0, 'F 8-9 NR': 11, 'F 8-9 NS': 9, 'F 10-14 C': 78, 'F 10-14 B': 2, 'F 10-14 H': 5, 'F 10-14 J': 0, 'F 10-14 M': 23, 'F 10-14 S': 0, 'F 10-14 OR': 0, 'F 10-14 NR': 42, 'F 10-14 NS': 4, 'F 15 C': 10, 'F 15 B': 0, 'F 15 H': 0, 'F 15 J': 0, 'F 15 M': 7, 'F 15 S': 0, 'F 15 OR': 0, 'F 15 NR': 5, 'F 15 NS': 2, 'F 16-17 C': 19, 'F 16-17 B': 0, 'F 16-17 H': 0, 'F 16-17 J': 0, 'F 16-17 M': 5, 'F 16-17 S': 0, 'F 16-17 OR': 1, 'F 16-17 NR': 15, 'F 16-17 NS': 6, 'F 18-19 C': 180, 'F 18-19 B': 4, 'F 18-19 H': 4, 'F 18-19 J': 2, 'F 18-19 M': 19, 'F 18-19 S': 1, 'F 18-19 OR': 1, 'F 18-19 NR': 154, 'F 18-19 NS': 16, 'F 20-24 C': 362, 'F 20-24 B': 8, 'F 20-24 H': 18, 'F 20-24 J': 7, 'F 20-24 M': 55, 'F 20-24 S': 3, 'F 20-24 OR': 8, 'F 20-24 NR': 289, 'F 20-24 NS': 41, 'F 25-29 C': 163, 'F 25-29 B': 3, 'F 25-29 H': 17, 'F 25-29 J': 0, 'F 25-29 M': 44, 'F 25-29 S': 7, 'F 25-29 OR': 2, 'F 25-29 NR': 125, 'F 25-29 NS': 33, 'F 30-34 C': 156, 'F 30-34 B': 6, 'F 30-34 H': 12, 'F 30-34 J': 0, 'F 30-34 M': 29, 'F 30-34 S': 1, 'F 30-34 OR': 0, 'F 30-34 NR': 85, 'F 30-34 NS': 17, 'F 35-39 C': 130, 'F 35-39 B': 2, 'F 35-39 H': 4, 'F 35-39 J': 0, 'F 35-39 M': 43, 'F 35-39 S': 1, 'F 35-39 OR': 3, 'F 35-39 NR': 54, 'F 35-39 NS': 6, 'F 40-44 C': 91, 'F 40-44 B': 1, 'F 40-44 H': 3, 'F 40-44 J': 0, 'F 40-44 M': 10, 'F 40-44 S': 1, 'F 40-44 OR': 3, 'F 40-44 NR': 32, 'F 40-44 NS': 8, 'F 45-49 C': 89, 'F 45-49 B': 1, 'F 45-49 H': 3, 'F 45-49 J': 1, 'F 45-49 M': 9, 'F 45-49 S': 1, 'F 45-49 OR': 1, 'F 45-49 NR': 35, 'F 45-49 NS': 13, 'F 50-54 C': 87, 'F 50-54 B': 1, 'F 50-54 H': 3, 'F 50-54 J': 0, 'F 50-54 M': 4, 'F 50-54 S': 1, 'F 50-54 OR': 0, 'F 50-54 NR': 25, 'F 50-54 NS': 12, 'F 55-59 C': 80, 'F 55-59 B': 5, 'F 55-59 H': 1, 'F 55-59 J': 0, 'F 55-59 M': 5, 'F 55-59 S': 0, 'F 55-59 OR': 1, 'F 55-59 NR': 30, 'F 55-59 NS': 8, 'F 60-64 C': 81, 'F 60-64 B': 0, 'F 60-64 H': 2, 'F 60-64 J': 0, 'F 60-64 M': 4, 'F 60-64 S': 0, 'F 60-64 OR': 2, 'F 60-64 NR': 20, 'F 60-64 NS': 14, 'F 65-69 C': 64, 'F 65-69 B': 0, 'F 65-69 H': 1, 'F 65-69 J': 1, 'F 65-69 M': 4, 'F 65-69 S': 0, 'F 65-69 OR': 0, 'F 65-69 NR': 12, 'F 65-69 NS': 4, 'F 70-74 C': 61, 'F 70-74 B': 0, 'F 70-74 H': 0, 'F 70-74 J': 0, 'F 70-74 M': 1, 'F 70-74 S': 0, 'F 70-74 OR': 0, 'F 70-74 NR': 9, 'F 70-74 NS': 14, 'F 75-79 C': 62, 'F 75-79 B': 1, 'F 75-79 H': 0, 'F 75-79 J': 0, 'F 75-79 M': 0, 'F 75-79 S': 0, 'F 75-79 OR': 0, 'F 75-79 NR': 3, 'F 75-79 NS': 12, 'F 80-84 C': 84, 'F 80-84 B': 0, 'F 80-84 H': 0, 'F 80-84 J': 1, 'F 80-84 M': 0, 'F 80-84 S': 0, 'F 80-84 OR': 0, 'F 80-84 NR': 2, 'F 80-84 NS': 8, 'F 85+ C': 83, 'F 85+ B': 0, 'F 85+ H': 0, 'F 85+ J': 0, 'F 85+ M': 0, 'F 85+ S': 0, 'F 85+ OR': 0, 'F 85+ NR': 3, 'F 85+ NS': 8}
CROSS_TABLES['sex_age_status'] = {'M 16-17 Single': 60, 'M 16-17 Married': 0, 'M 16-17 Partner': 0, 'M 16-17 Seperated': 0, 'M 16-17 Divorced': 0, 'M 16-17 Widowed': 0, 'F 16-17 Single': 46, 'F 16-17 Married': 0, 'F 16-17 Partner': 0, 'F 16-17 Seperated': 0, 'F 16-17 Divorced': 0, 'F 16-17 Widowed': 0, 'M 18-19 Single': 270, 'M 18-19 Married': 0, 'M 18-19 Partner': 0, 'M 18-19 Seperated': 0, 'M 18-19 Divorced': 0, 'M 18-19 Widowed': 0, 'F 18-19 Single': 378, 'F 18-19 Married': 3, 'F 18-19 Partner': 0, 'F 18-19 Seperated': 0, 'F 18-19 Divorced': 0, 'F 18-19 Widowed': 0, 'M 20-24 Single': 661, 'M 20-24 Married': 6, 'M 20-24 Partner': 0, 'M 20-24 Seperated': 0, 'M 20-24 Divorced': 2, 'M 20-24 Widowed': 0, 'F 20-24 Single': 766, 'F 20-24 Married': 20, 'F 20-24 Partner': 0, 'F 20-24 Seperated': 3, 'F 20-24 Divorced': 2, 'F 20-24 Widowed': 0, 'M 25-29 Single': 308, 'M 25-29 Married': 50, 'M 25-29 Partner': 1, 'M 25-29 Seperated': 2, 'M 25-29 Divorced': 3, 'M 25-29 Widowed': 1, 'F 25-29 Single': 291, 'F 25-29 Married': 83, 'F 25-29 Partner': 2, 'F 25-29 Seperated': 5, 'F 25-29 Divorced': 13, 'F 25-29 Widowed': 0, 'M 30-34 Single': 193, 'M 30-34 Married': 107, 'M 30-34 Partner': 1, 'M 30-34 Seperated': 4, 'M 30-34 Divorced': 6, 'M 30-34 Widowed': 0, 'F 30-34 Single': 154, 'F 30-34 Married': 128, 'F 30-34 Partner': 2, 'F 30-34 Seperated': 10, 'F 30-34 Divorced': 11, 'F 30-34 Widowed': 1, 'M 35-39 Single': 89, 'M 35-39 Married': 111, 'M 35-39 Partner': 0, 'M 35-39 Seperated': 6, 'M 35-39 Divorced': 14, 'M 35-39 Widowed': 1, 'F 35-39 Single': 85, 'F 35-39 Married': 110, 'F 35-39 Partner': 0, 'F 35-39 Seperated': 22, 'F 35-39 Divorced': 24, 'F 35-39 Widowed': 2, 'M 40-44 Single': 75, 'M 40-44 Married': 105, 'M 40-44 Partner': 0, 'M 40-44 Seperated': 6, 'M 40-44 Divorced': 8, 'M 40-44 Widowed': 2, 'F 40-44 Single': 50, 'F 40-44 Married': 65, 'F 40-44 Partner': 0, 'F 40-44 Seperated': 10, 'F 40-44 Divorced': 22, 'F 40-44 Widowed': 2, 'M 45-49 Single': 52, 'M 45-49 Married': 72, 'M 45-49 Partner': 0, 'M 45-49 Seperated': 5, 'M 45-49 Divorced': 18, 'M 45-49 Widowed': 0, 'F 45-49 Single': 46, 'F 45-49 Married': 73, 'F 45-49 Partner': 1, 'F 45-49 Seperated': 9, 'F 45-49 Divorced': 20, 'F 45-49 Widowed': 4, 'M 50-54 Single': 35, 'M 50-54 Married': 55, 'M 50-54 Partner': 0, 'M 50-54 Seperated': 9, 'M 50-54 Divorced': 12, 'M 50-54 Widowed': 4, 'F 50-54 Single': 28, 'F 50-54 Married': 64, 'F 50-54 Partner': 0, 'F 50-54 Seperated': 7, 'F 50-54 Divorced': 31, 'F 50-54 Widowed': 3, 'M 55-59 Single': 20, 'M 55-59 Married': 77, 'M 55-59 Partner': 0, 'M 55-59 Seperated': 2, 'M 55-59 Divorced': 17, 'M 55-59 Widowed': 2, 'F 55-59 Single': 12, 'F 55-59 Married': 72, 'F 55-59 Partner': 0, 'F 55-59 Seperated': 9, 'F 55-59 Divorced': 24, 'F 55-59 Widowed': 13, 'M 60-64 Single': 17, 'M 60-64 Married': 64, 'M 60-64 Partner': 0, 'M 60-64 Seperated': 2, 'M 60-64 Divorced': 24, 'M 60-64 Widowed': 2, 'F 60-64 Single': 13, 'F 60-64 Married': 60, 'F 60-64 Partner': 2, 'F 60-64 Seperated': 4, 'F 60-64 Divorced': 28, 'F 60-64 Widowed': 16, 'M 65-69 Single': 17, 'M 65-69 Married': 57, 'M 65-69 Partner': 0, 'M 65-69 Seperated': 1, 'M 65-69 Divorced': 16, 'M 65-69 Widowed': 0, 'F 65-69 Single': 7, 'F 65-69 Married': 47, 'F 65-69 Partner': 0, 'F 65-69 Seperated': 2, 'F 65-69 Divorced': 14, 'F 65-69 Widowed': 16, 'M 70-74 Single': 10, 'M 70-74 Married': 43, 'M 70-74 Partner': 0, 'M 70-74 Seperated': 2, 'M 70-74 Divorced': 10, 'M 70-74 Widowed': 12, 'F 70-74 Single': 11, 'F 70-74 Married': 33, 'F 70-74 Partner': 0, 'F 70-74 Seperated': 2, 'F 70-74 Divorced': 13, 'F 70-74 Widowed': 26, 'M 75-79 Single': 8, 'M 75-79 Married': 25, 'M 75-79 Partner': 0, 'M 75-79 Seperated': 0, 'M 75-79 Divorced': 5, 'M 75-79 Widowed': 11, 'F 75-79 Single': 3, 'F 75-79 Married': 35, 'F 75-79 Partner': 0, 'F 75-79 Seperated': 0, 'F 75-79 Divorced': 8, 'F 75-79 Widowed': 32, 'M 80-84 Single': 2, 'M 80-84 Married': 45, 'M 80-84 Partner': 0, 'M 80-84 Seperated': 0, 'M 80-84 Divorced': 3, 'M 80-84 Widowed': 20, 'F 80-84 Single': 10, 'F 80-84 Married': 22, 'F 80-84 Partner': 0, 'F 80-84 Seperated': 0, 'F 80-84 Divorced': 6, 'F 80-84 Widowed': 57, 'M 85+ Single': 4, 'M 85+ Married': 20, 'M 85+ Partner': 2, 'M 85+ Seperated': 0, 'M 85+ Divorced': 5, 'M 85+ Widowed': 17, 'F 85+ Single': 6, 'F 85+ Married': 15, 'F 85+ Partner': 2, 'F 85+ Seperated': 0, 'F 85+ Divorced': 3, 'F 85+ Widowed': 68}
CROSS_TABLES['sex_age_qualification'] = {'M 16-24 no': 38, 'M 16-24 level1': 116, 'M 16-24 level2': 107, 'M 16-24 apprent': 15, 'M 16-24 level3': 502, 'M 16-24 level4+': 145, 'M 16-24 other': 76, 'M 25-34 no': 53, 'M 25-34 level1': 50, 'M 25-34 level2': 50, 'M 25-34 apprent': 5, 'M 25-34 level3': 70, 'M 25-34 level4+': 376, 'M 25-34 other': 72, 'M 35-49 no': 80, 'M 35-49 level1': 73, 'M 35-49 level2': 52, 'M 35-49 apprent': 10, 'M 35-49 level3': 43, 'M 35-49 level4+': 217, 'M 35-49 other': 89, 'M 50-64 no': 117, 'M 50-64 level1': 20, 'M 50-64 level2': 25, 'M 50-64 apprent': 33, 'M 50-64 level3': 23, 'M 50-64 level4+': 89, 'M 50-64 other': 35, 'M 65+ no': 174, 'M 65+ level1': 20, 'M 65+ level2': 11, 'M 65+ apprent': 27, 'M 65+ level3': 5, 'M 65+ level4+': 72, 'M 65+ other': 26, 'F 16-24 no': 40, 'F 16-24 level1': 124, 'F 16-24 level2': 166, 'F 16-24 apprent': 4, 'F 16-24 level3': 595, 'F 16-24 level4+': 203, 'F 16-24 other': 86, 'F 25-34 no': 49, 'F 25-34 level1': 63, 'F 25-34 level2': 60, 'F 25-34 apprent': 3, 'F 25-34 level3': 69, 'F 25-34 level4+': 383, 'F 25-34 other': 73, 'F 35-49 no': 71, 'F 35-49 level1': 83, 'F 35-49 level2': 54, 'F 35-49 apprent': 3, 'F 35-49 level3': 38, 'F 35-49 level4+': 259, 'F 35-49 other': 37, 'F 50-64 no': 139, 'F 50-64 level1': 47, 'F 50-64 level2': 39, 'F 50-64 apprent': 2, 'F 50-64 level3': 15, 'F 50-64 level4+': 116, 'F 50-64 other': 28, 'F 65+ no': 258, 'F 65+ level1': 14, 'F 65+ level2': 35, 'F 65+ apprent': 4, 'F 65+ level3': 8, 'F 65+ level4+': 82, 'F 65+ other': 37}


# compensate the marital status of < 16 as single
total_population = sum(list(CROSS_TABLES['sex_age'].values()))
total_16_and_above = sum(list(CROSS_TABLES['sex_age_status'].values()))
Male_0_15 = round((total_population - total_16_and_above) * sexes['M']/total_population)
Female_0_15 = round((total_population - total_16_and_above) * sexes['F']/total_population)
mstatuses['Single'] += Male_0_15 + Female_0_15
CROSS_TABLES['sex_age_status']['M 0-15 Single'] = Male_0_15
CROSS_TABLES['sex_age_status']['F 0-15 Single'] = Female_0_15

# compensate the highest level of qualification for < 16 as No Qualificaiton
total_population = sum(list(CROSS_TABLES['sex_age'].values()))
total_16_and_above = sum(list(CROSS_TABLES['sex_age_qualification'].values()))
Male_0_15 = round((total_population - total_16_and_above) * sexes['M']/total_population)
Female_0_15 = round((total_population - total_16_and_above) * sexes['F']/total_population)
qualifications['no'] += Male_0_15 + Female_0_15
CROSS_TABLES['sex_age_qualification']['M 0-15 no'] = Male_0_15
CROSS_TABLES['sex_age_qualification']['F 0-15 no'] = Female_0_15

# Total = 7303
Total = 7303
num_workers = multiprocessing.cpu_count()  # Number of CPU cores to use

# reduce_percent = 0.1
# Total = round(7303*reduce_percent)
# ages = reduce(ages, reduce_percent, Total)
# sexes = reduce(sexes, reduce_percent, Total)
# ethnicities = reduce(ethnicities, reduce_percent, Total)
# CROSS_TABLES['sex_age'] = reduce(CROSS_TABLES['sex_age'], reduce_percent, Total)
# CROSS_TABLES['sex_age_ethnicity'] = reduce(CROSS_TABLES['sex_age_ethnicity'], reduce_percent, Total)
# CROSS_TABLES['sex_age_religion'] = reduce(CROSS_TABLES['sex_age_religion'], reduce_percent, Total)
# CROSS_TABLES['sex_age_status'] = reduce(CROSS_TABLES['sex_age_status'], reduce_percent, Total)
# CROSS_TABLES['sex_age_qualification'] = reduce(CROSS_TABLES['sex_age_qualification'], reduce_percent, Total)

def agemap_maritalstatus(age):
    if age in ['0-4', '5-7', '8-9', '10-14', '15']:
        return "0-15"
    else:
        return age

def agemap_qualification(age):
    if age in ['0-4', '5-7', '8-9', '10-14', '15']:
        return "0-15"
    elif age in ['16-17', '18-19', '20-24']:
        return "16-24"
    elif age in ['25-29', '30-34']:
        return "25-34"
    elif age in ['35-39', '40-44', '45-49']:
        return "35-49"
    elif age in ['50-54', '55-59', '60-64']:
        return "50-64"
    elif age in ['65-69', '70-74', '75-79', '80-84', '85+']:
        return "65+"
    else:
        return age

def getStats(persons, crosstable):
    actual = CROSS_TABLES[crosstable]
    temp = []
    attributes = crosstable.split('_')
    for person in persons:
        record = ""
        for attribute in attributes:
            if 'status' in attributes and attribute == 'age':
                record = record + agemap_maritalstatus(person['age']) + " "
            elif 'qualification' in attributes and attribute == 'age':
                record = record + agemap_qualification(person['age']) + " "
            else:
                record = record + person[attribute] + " "
        record = record.rstrip()
        temp.append(record)
    predicted = Counter(temp)
    return dict([(k, predicted[k]) for k in list(actual.keys())])

def area_of_difference(actual, predicted):
    # Create x-axis values
    x = np.arange(len(actual))
    # Calculate the difference and plot it as a shaded area
    diff = np.abs(np.array(actual) - np.array(predicted))
    # Compute and print the area of difference
    area = trapz(diff, x)
    return area

def getfitness(individual, crosstable, SHIFT=False):
    a = list(CROSS_TABLES[crosstable].values())
    if SHIFT==True:
        p = list(getStats(individual, crosstable).values())
    else:
        p = shift_left(list(getStats(individual, crosstable).values()), 1)
    return area_of_difference(a, p)

def parallel_evaluation(individual):
    with multiprocessing.Pool(processes=num_workers) as pool:
        fitnesses = pool.map(evaluate, individual)
    return fitnesses

def random_person():
    # age = random.choice(list(ages.keys()))
    # sex = random.choice(list(sexes.keys()))
    age = random.choices(list(ages.keys()), list(ages.values()), k=1)[0]
    sex = random.choices(list(sexes.keys()), list(sexes.values()), k=1)[0]
    ethnicity = random.choices(list(ethnicities.keys()), list(ethnicities.values()), k=1)[0]
    religion = random.choices(list(religions.keys()), list(religions.values()), k=1)[0]
    status = random.choices(list(mstatuses.keys()), list(mstatuses.values()), k=1)[0]
    qual = random.choices(list(qualifications.keys()), list(qualifications.values()), k=1)[0]
    person = validate({'age': age, 'sex': sex, 'ethnicity': ethnicity, 'religion': religion,
            'status': status, 'qualification': qual})
    return person

def validate(person):
    #validation rule#1:
    if person['age'] in ['0-4', '5-7', '8-9', '10-14', '15']:
        if person['status'] != 'Single':
            person['status'] = 'Single'
    if person['age'] in ['0-4', '5-7', '8-9', '10-14', '15']:
        if person['qualification'] != 'no':
            person['qualification'] = 'no'
    return person

# def random_individual():
#     age = random.choices(list(ages.keys()), list(ages.values()), k=Total)
#     sex = random.choices(list(sexes.keys()), list(sexes.values()), k=Total)
#     ethnicity = random.choices(list(ethnicities.keys()), list(ethnicities.values()), k=Total)
#     religion = random.choices(list(religions.keys()), list(religions.values()), k=Total)
#     status = random.choices(list(mstatuses.keys()), list(mstatuses.values()), k=Total)
#     qual = random.choices(list(qualifications.keys()), list(qualifications.values()), k=Total)
#     comb = [(age[i], sex[i], ethnicity[i], religion[i], status[i], qual[i]) for i in range(0,Total)]
#     individual = [validate({'age':c[0], 'sex':c[1], 'ethnicity':c[2], 'religion':c[3],
#                    'status': c[4], 'qualification': c[5]}) for c in comb]
#     return creator.Individual(individual)

def mutation(individual, mutation_probability):
    # Apply the mutation operator to the individual
    # for i in range(len(individual)):
    #     if random.random() < mutation_probability:
    #         individual[i] = random_person()
    a = random.randrange(0, len(individual) - 1)
    b = random.randrange(0, len(individual) - 1)
    if a != b:
        A = individual[a]
        B = individual[b]
        attribute = random.choice(['age', 'sex' , 'ethnicity' , 'religion', 'status' , 'qualification'])
        temp = A[attribute]
        A[attribute] = B[attribute]
        B[attribute] = temp
        individual[a] = A
        individual[b] = B
    return individual,


# Define the problem dimensions
creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0, -1.0))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()
toolbox.register("person", random_person)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.person, n=Total)
# toolbox.register("individual", random_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the genetic operators
toolbox.register("evaluate", parallel_evaluation)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", mutation, mutation_probability=0.2)
toolbox.register("select", tools.selNSGA2)

# Define the algorithm
POP_SIZE = 100
NGEN = 3
mu = 50
lambda_ = POP_SIZE
cxpb = 0.6
mutpb = 0.4

pop = toolbox.population(n=POP_SIZE)

mutation(pop[0], 1)
hof = tools.ParetoFront()
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("min", np.min, axis=0)
stats.register("max", np.max, axis=0)

pop, log = algorithms.eaMuPlusLambda(pop, toolbox, mu, lambda_, cxpb, mutpb, ngen=NGEN, stats=stats, verbose=True, halloffame=hof)

# plot_data = []
# for entry in log:
#     min = entry['min']
#     dic = {'gen': entry['gen'], 'A':min[0], 'B': min[1], 'C': min[2], 'D': min[3], 'E': min[4]}
#     plot_data.append(dic)
#
# pdf = pd.DataFrame(plot_data)
# pdf['A'] =(pdf['A']-pdf['A'].min())/(pdf['A'].max()-pdf['A'].min())
# pdf['B'] =(pdf['B']-pdf['B'].min())/(pdf['B'].max()-pdf['B'].min())
# pdf['C'] =(pdf['C']-pdf['C'].min())/(pdf['C'].max()-pdf['C'].min())
# pdf['D'] =(pdf['D']-pdf['D'].min())/(pdf['D'].max()-pdf['D'].min())
# pdf['E'] =(pdf['E']-pdf['E'].min())/(pdf['E'].max()-pdf['E'].min())
# fig = px.line(pdf, x=pdf.columns[0], y=pdf.columns[1:])
# py.offline.plot(fig, filename="graphs\convergence.html")
# fig.show()


# Assign weights to the objectives
sex_age = 0.2
sex_age_ethnicity = 0.3
sex_age_religion = 0.1
sex_age_status = 0.3
sex_age_qualification = 0.1

# Calculate the weighted sum for each individual in the Pareto front (Hall of Fame)
weighted_sums = [sex_age * ind.fitness.values[0] +
                 sex_age_ethnicity * ind.fitness.values[1] +
                 sex_age_religion * ind.fitness.values[2] +
                 sex_age_status * ind.fitness.values[3] +
                 sex_age_qualification * ind.fitness.values[4]  for ind in hof]

# Find the index of the individual with the lowest weighted sum
best_index = weighted_sums.index(np.min(weighted_sums))

# Select the best individual from the Pareto front (Hall of Fame)
best_individual = hof[best_index]
# records = []
# for ind in best_individual:
#     records.append(ind)
#
# df = pd.DataFrame(records)
# df.to_csv('graphs\population2.csv', index=False)
# plot(CROSS_TABLES['sex_age'], getStats(best_individual, 'sex_age') ,'sex_age')
# plot(CROSS_TABLES['sex_age_ethnicity'], getStats(best_individual, 'sex_age_ethnicity') ,'sex_age_ethnicity', SHIFTLEFT=True)
# plot(CROSS_TABLES['sex_age_religion'], getStats(best_individual, 'sex_age_religion'), 'sex_age_religion')
# plot(CROSS_TABLES['sex_age_status'], getStats(best_individual, 'sex_age_status'), 'sex_age_status')
# plot(CROSS_TABLES['sex_age_qualification'], getStats(best_individual, 'sex_age_qualification'), 'sex_age_qualification')
import numpy as np
from deap import tools
from deap.tools._hypervolume import hv

# Assuming you have already run the NSGA-II algorithm and have the final population

# Step 1: Obtain the Pareto front
pareto_front = tools.selNSGA2(pop, len(pop))

# Step 2: Normalize the objective function values if necessary
# (This step is optional and depends on your specific objectives)

# Step 3: Convert the Pareto front to an array of objective values
pareto_array = np.array([ind.fitness.values for ind in pareto_front])

# Step 4: Define the reference point
reference_point = np.max(pareto_array, axis=0) + 0.1

# Step 5: Calculate the hypervolume
hypervolume = hv.hypervolume(pareto_array, reference_point)

print("Hypervolume:", hypervolume)
