import random
import numpy as np
import matplotlib.pyplot as plt
from deap import algorithms, base, creator, tools
from Person import Person
from collections import Counter, OrderedDict
import plotly.graph_objs as go
import  plotly as py
import plotly.express as px
import cProfile
import statistics
import concurrent.futures
import time

def plot(actual, predicted, name, width=1000):
    a = np.array(list(actual.values()))
    p = np.array(list(predicted.values()))
    rmse = np.sqrt(((p - a) ** 2).mean())

    fig = go.Figure()
    fig.add_trace(go.Scatter(x0='data', x=list(actual.keys()), name='actual', y=list(actual.values()), line_color='#636EFA'))
    fig.add_trace(go.Scatter(x0='data', x=list(actual.keys()), name='pred', y=list(predicted.values()), line_color='#EF553B'))
    fig.update_layout(width=width, title=name + "  " + 'RMSE=' + str(rmse))
    py.offline.plot(fig, filename=name + ".html")
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

CROSS_TABLES = {}
CROSS_TABLES['sex_age'] = {'M 0-4': 227 , 'M 5-7': 102 , 'M 8-9': 67 , 'M 10-14': 141 , 'M 15': 20 , 'M 16-17': 60 , 'M 18-19': 270 , 'M 20-24': 669 , 'M 25-29': 365 , 'M 30-34': 311 , 'M 35-39': 221 , 'M 40-44': 196 , 'M 45-49': 147 , 'M 50-54': 115 , 'M 55-59': 118 , 'M 60-64': 109 , 'M 65-69': 91 , 'M 70-74': 77 , 'M 75-79': 49 , 'M 80-84': 70 , 'M 85+': 48 , 'F 0-4': 220 , 'F 5-7': 80 , 'F 8-9': 65 , 'F 10-14': 154 , 'F 15': 24 , 'F 16-17': 46 , 'F 18-19': 381 , 'F 20-24': 791 , 'F 25-29': 394 , 'F 30-34': 306 , 'F 35-39': 243 , 'F 40-44': 149 , 'F 45-49': 153 , 'F 50-54': 133 , 'F 55-59': 130 , 'F 60-64': 123 , 'F 65-69': 86 , 'F 70-74': 85 , 'F 75-79': 78 , 'F 80-84': 95 , 'F 85+': 94}
CROSS_TABLES['sex_age_ethnicity'] = {'M 0-4 W0': 93, 'M 0-4 W1': 0, 'M 0-4 W2': 0, 'M 0-4 W3': 14, 'M 0-4 M0': 3, 'M 0-4 M1': 3, 'M 0-4 M2': 9, 'M 0-4 M3': 13, 'M 0-4 A0': 17, 'M 0-4 A1': 14, 'M 0-4 A2': 10, 'M 0-4 A3': 0, 'M 0-4 A4': 25, 'M 0-4 B0': 19, 'M 0-4 B1': 1, 'M 0-4 B2': 2, 'M 0-4 O0': 1, 'M 0-4 O1': 3, 'M 5-7 W0': 41, 'M 5-7 W1': 0, 'M 5-7 W2': 0, 'M 5-7 W3': 5, 'M 5-7 M0': 0, 'M 5-7 M1': 2, 'M 5-7 M2': 3, 'M 5-7 M3': 2, 'M 5-7 A0': 9, 'M 5-7 A1': 7, 'M 5-7 A2': 5, 'M 5-7 A3': 0, 'M 5-7 A4': 9, 'M 5-7 B0': 8, 'M 5-7 B1': 1, 'M 5-7 B2': 6, 'M 5-7 O0': 3, 'M 5-7 O1': 1, 'M 8-9 W0': 33, 'M 8-9 W1': 0, 'M 8-9 W2': 0, 'M 8-9 W3': 4, 'M 8-9 M0': 0, 'M 8-9 M1': 0, 'M 8-9 M2': 1, 'M 8-9 M3': 2, 'M 8-9 A0': 5, 'M 8-9 A1': 4, 'M 8-9 A2': 4, 'M 8-9 A3': 0, 'M 8-9 A4': 2, 'M 8-9 B0': 6, 'M 8-9 B1': 1, 'M 8-9 B2': 2, 'M 8-9 O0': 2, 'M 8-9 O1': 1, 'M 10-14 W0': 70, 'M 10-14 W1': 0, 'M 10-14 W2': 0, 'M 10-14 W3': 6, 'M 10-14 M0': 2, 'M 10-14 M1': 1, 'M 10-14 M2': 2, 'M 10-14 M3': 6, 'M 10-14 A0': 7, 'M 10-14 A1': 14, 'M 10-14 A2': 8, 'M 10-14 A3': 1, 'M 10-14 A4': 13, 'M 10-14 B0': 3, 'M 10-14 B1': 2, 'M 10-14 B2': 4, 'M 10-14 O0': 1, 'M 10-14 O1': 1, 'M 15 W0': 13, 'M 15 W1': 0, 'M 15 W2': 0, 'M 15 W3': 0, 'M 15 M0': 1, 'M 15 M1': 2, 'M 15 M2': 0, 'M 15 M3': 1, 'M 15 A0': 0, 'M 15 A1': 1, 'M 15 A2': 0, 'M 15 A3': 0, 'M 15 A4': 0, 'M 15 B0': 2, 'M 15 B1': 0, 'M 15 B2': 0, 'M 15 O0': 0, 'M 15 O1': 0, 'M 16-17 W0': 34, 'M 16-17 W1': 0, 'M 16-17 W2': 0, 'M 16-17 W3': 4, 'M 16-17 M0': 0, 'M 16-17 M1': 0, 'M 16-17 M2': 0, 'M 16-17 M3': 1, 'M 16-17 A0': 5, 'M 16-17 A1': 6, 'M 16-17 A2': 2, 'M 16-17 A3': 1, 'M 16-17 A4': 4, 'M 16-17 B0': 1, 'M 16-17 B1': 0, 'M 16-17 B2': 2, 'M 16-17 O0': 0, 'M 16-17 O1': 0, 'M 18-19 W0': 171, 'M 18-19 W1': 1, 'M 18-19 W2': 0, 'M 18-19 W3': 30, 'M 18-19 M0': 1, 'M 18-19 M1': 2, 'M 18-19 M2': 4, 'M 18-19 M3': 1, 'M 18-19 A0': 6, 'M 18-19 A1': 6, 'M 18-19 A2': 4, 'M 18-19 A3': 17, 'M 18-19 A4': 4, 'M 18-19 B0': 12, 'M 18-19 B1': 5, 'M 18-19 B2': 0, 'M 18-19 O0': 6, 'M 18-19 O1': 0, 'M 20-24 W0': 404, 'M 20-24 W1': 9, 'M 20-24 W2': 1, 'M 20-24 W3': 89, 'M 20-24 M0': 8, 'M 20-24 M1': 7, 'M 20-24 M2': 7, 'M 20-24 M3': 7, 'M 20-24 A0': 18, 'M 20-24 A1': 13, 'M 20-24 A2': 5, 'M 20-24 A3': 38, 'M 20-24 A4': 16, 'M 20-24 B0': 31, 'M 20-24 B1': 3, 'M 20-24 B2': 1, 'M 20-24 O0': 8, 'M 20-24 O1': 4, 'M 25-29 W0': 157, 'M 25-29 W1': 7, 'M 25-29 W2': 0, 'M 25-29 W3': 83, 'M 25-29 M0': 1, 'M 25-29 M1': 1, 'M 25-29 M2': 0, 'M 25-29 M3': 1, 'M 25-29 A0': 19, 'M 25-29 A1': 28, 'M 25-29 A2': 5, 'M 25-29 A3': 22, 'M 25-29 A4': 11, 'M 25-29 B0': 12, 'M 25-29 B1': 1, 'M 25-29 B2': 0, 'M 25-29 O0': 9, 'M 25-29 O1': 8, 'M 30-34 W0': 135, 'M 30-34 W1': 2, 'M 30-34 W2': 0, 'M 30-34 W3': 68, 'M 30-34 M0': 3, 'M 30-34 M1': 0, 'M 30-34 M2': 1, 'M 30-34 M3': 1, 'M 30-34 A0': 22, 'M 30-34 A1': 13, 'M 30-34 A2': 7, 'M 30-34 A3': 11, 'M 30-34 A4': 23, 'M 30-34 B0': 17, 'M 30-34 B1': 1, 'M 30-34 B2': 2, 'M 30-34 O0': 1, 'M 30-34 O1': 4, 'M 35-39 W0': 95, 'M 35-39 W1': 1, 'M 35-39 W2': 0, 'M 35-39 W3': 31, 'M 35-39 M0': 1, 'M 35-39 M1': 0, 'M 35-39 M2': 2, 'M 35-39 M3': 1, 'M 35-39 A0': 22, 'M 35-39 A1': 10, 'M 35-39 A2': 2, 'M 35-39 A3': 7, 'M 35-39 A4': 28, 'M 35-39 B0': 10, 'M 35-39 B1': 2, 'M 35-39 B2': 0, 'M 35-39 O0': 5, 'M 35-39 O1': 4, 'M 40-44 W0': 105, 'M 40-44 W1': 0, 'M 40-44 W2': 0, 'M 40-44 W3': 18, 'M 40-44 M0': 0, 'M 40-44 M1': 0, 'M 40-44 M2': 0, 'M 40-44 M3': 1, 'M 40-44 A0': 19, 'M 40-44 A1': 9, 'M 40-44 A2': 5, 'M 40-44 A3': 0, 'M 40-44 A4': 11, 'M 40-44 B0': 15, 'M 40-44 B1': 9, 'M 40-44 B2': 2, 'M 40-44 O0': 2, 'M 40-44 O1': 0, 'M 45-49 W0': 91, 'M 45-49 W1': 0, 'M 45-49 W2': 0, 'M 45-49 W3': 10, 'M 45-49 M0': 0, 'M 45-49 M1': 0, 'M 45-49 M2': 0, 'M 45-49 M3': 0, 'M 45-49 A0': 7, 'M 45-49 A1': 10, 'M 45-49 A2': 3, 'M 45-49 A3': 0, 'M 45-49 A4': 7, 'M 45-49 B0': 4, 'M 45-49 B1': 4, 'M 45-49 B2': 7, 'M 45-49 O0': 4, 'M 45-49 O1': 0, 'M 50-54 W0': 76, 'M 50-54 W1': 0, 'M 50-54 W2': 0, 'M 50-54 W3': 10, 'M 50-54 M0': 0, 'M 50-54 M1': 1, 'M 50-54 M2': 1, 'M 50-54 M3': 0, 'M 50-54 A0': 9, 'M 50-54 A1': 1, 'M 50-54 A2': 1, 'M 50-54 A3': 0, 'M 50-54 A4': 3, 'M 50-54 B0': 6, 'M 50-54 B1': 2, 'M 50-54 B2': 2, 'M 50-54 O0': 2, 'M 50-54 O1': 1, 'M 55-59 W0': 99, 'M 55-59 W1': 1, 'M 55-59 W2': 0, 'M 55-59 W3': 5, 'M 55-59 M0': 0, 'M 55-59 M1': 1, 'M 55-59 M2': 0, 'M 55-59 M3': 0, 'M 55-59 A0': 1, 'M 55-59 A1': 4, 'M 55-59 A2': 0, 'M 55-59 A3': 0, 'M 55-59 A4': 1, 'M 55-59 B0': 4, 'M 55-59 B1': 0, 'M 55-59 B2': 2, 'M 55-59 O0': 0, 'M 55-59 O1': 0, 'M 60-64 W0': 99, 'M 60-64 W1': 2, 'M 60-64 W2': 0, 'M 60-64 W3': 1, 'M 60-64 M0': 0, 'M 60-64 M1': 0, 'M 60-64 M2': 0, 'M 60-64 M3': 0, 'M 60-64 A0': 1, 'M 60-64 A1': 1, 'M 60-64 A2': 0, 'M 60-64 A3': 4, 'M 60-64 A4': 0, 'M 60-64 B0': 0, 'M 60-64 B1': 0, 'M 60-64 B2': 1, 'M 60-64 O0': 0, 'M 60-64 O1': 0, 'M 65-69 W0': 74, 'M 65-69 W1': 3, 'M 65-69 W2': 0, 'M 65-69 W3': 4, 'M 65-69 M0': 0, 'M 65-69 M1': 0, 'M 65-69 M2': 0, 'M 65-69 M3': 0, 'M 65-69 A0': 0, 'M 65-69 A1': 3, 'M 65-69 A2': 0, 'M 65-69 A3': 1, 'M 65-69 A4': 3, 'M 65-69 B0': 1, 'M 65-69 B1': 2, 'M 65-69 B2': 0, 'M 65-69 O0': 0, 'M 65-69 O1': 0, 'M 70-74 W0': 68, 'M 70-74 W1': 4, 'M 70-74 W2': 0, 'M 70-74 W3': 1, 'M 70-74 M0': 1, 'M 70-74 M1': 0, 'M 70-74 M2': 0, 'M 70-74 M3': 0, 'M 70-74 A0': 0, 'M 70-74 A1': 0, 'M 70-74 A2': 0, 'M 70-74 A3': 1, 'M 70-74 A4': 1, 'M 70-74 B0': 0, 'M 70-74 B1': 1, 'M 70-74 B2': 0, 'M 70-74 O0': 0, 'M 70-74 O1': 0, 'M 75-79 W0': 45, 'M 75-79 W1': 1, 'M 75-79 W2': 0, 'M 75-79 W3': 1, 'M 75-79 M0': 0, 'M 75-79 M1': 0, 'M 75-79 M2': 0, 'M 75-79 M3': 0, 'M 75-79 A0': 0, 'M 75-79 A1': 0, 'M 75-79 A2': 0, 'M 75-79 A3': 0, 'M 75-79 A4': 0, 'M 75-79 B0': 0, 'M 75-79 B1': 2, 'M 75-79 B2': 0, 'M 75-79 O0': 0, 'M 75-79 O1': 0, 'M 80-84 W0': 63, 'M 80-84 W1': 2, 'M 80-84 W2': 0, 'M 80-84 W3': 0, 'M 80-84 M0': 0, 'M 80-84 M1': 0, 'M 80-84 M2': 0, 'M 80-84 M3': 0, 'M 80-84 A0': 1, 'M 80-84 A1': 2, 'M 80-84 A2': 0, 'M 80-84 A3': 0, 'M 80-84 A4': 1, 'M 80-84 B0': 0, 'M 80-84 B1': 0, 'M 80-84 B2': 0, 'M 80-84 O0': 0, 'M 80-84 O1': 1, 'M 85+ W0': 42, 'M 85+ W1': 3, 'M 85+ W2': 0, 'M 85+ W3': 0, 'M 85+ M0': 0, 'M 85+ M1': 0, 'M 85+ M2': 0, 'M 85+ M3': 0, 'M 85+ A0': 0, 'M 85+ A1': 0, 'M 85+ A2': 0, 'M 85+ A3': 0, 'M 85+ A4': 0, 'M 85+ B0': 0, 'M 85+ B1': 3, 'M 85+ B2': 0, 'M 85+ O0': 0, 'M 85+ O1': 0, 'F 0-4 W0': 99, 'F 0-4 W1': 0, 'F 0-4 W2': 0, 'F 0-4 W3': 12, 'F 0-4 M0': 7, 'F 0-4 M1': 2, 'F 0-4 M2': 11, 'F 0-4 M3': 5, 'F 0-4 A0': 21, 'F 0-4 A1': 19, 'F 0-4 A2': 4, 'F 0-4 A3': 1, 'F 0-4 A4': 23, 'F 0-4 B0': 9, 'F 0-4 B1': 2, 'F 0-4 B2': 0, 'F 0-4 O0': 4, 'F 0-4 O1': 1, 'F 5-7 W0': 33, 'F 5-7 W1': 1, 'F 5-7 W2': 0, 'F 5-7 W3': 2, 'F 5-7 M0': 4, 'F 5-7 M1': 2, 'F 5-7 M2': 7, 'F 5-7 M3': 2, 'F 5-7 A0': 9, 'F 5-7 A1': 6, 'F 5-7 A2': 3, 'F 5-7 A3': 0, 'F 5-7 A4': 5, 'F 5-7 B0': 5, 'F 5-7 B1': 0, 'F 5-7 B2': 0, 'F 5-7 O0': 1, 'F 5-7 O1': 0, 'F 8-9 W0': 20, 'F 8-9 W1': 0, 'F 8-9 W2': 0, 'F 8-9 W3': 3, 'F 8-9 M0': 5, 'F 8-9 M1': 0, 'F 8-9 M2': 0, 'F 8-9 M3': 2, 'F 8-9 A0': 6, 'F 8-9 A1': 6, 'F 8-9 A2': 2, 'F 8-9 A3': 0, 'F 8-9 A4': 4, 'F 8-9 B0': 9, 'F 8-9 B1': 0, 'F 8-9 B2': 7, 'F 8-9 O0': 1, 'F 8-9 O1': 0, 'F 10-14 W0': 75, 'F 10-14 W1': 0, 'F 10-14 W2': 0, 'F 10-14 W3': 11, 'F 10-14 M0': 6, 'F 10-14 M1': 2, 'F 10-14 M2': 1, 'F 10-14 M3': 3, 'F 10-14 A0': 5, 'F 10-14 A1': 13, 'F 10-14 A2': 4, 'F 10-14 A3': 1, 'F 10-14 A4': 12, 'F 10-14 B0': 11, 'F 10-14 B1': 5, 'F 10-14 B2': 1, 'F 10-14 O0': 0, 'F 10-14 O1': 4, 'F 15 W0': 10, 'F 15 W1': 0, 'F 15 W2': 0, 'F 15 W3': 1, 'F 15 M0': 0, 'F 15 M1': 0, 'F 15 M2': 1, 'F 15 M3': 0, 'F 15 A0': 0, 'F 15 A1': 3, 'F 15 A2': 1, 'F 15 A3': 0, 'F 15 A4': 4, 'F 15 B0': 1, 'F 15 B1': 2, 'F 15 B2': 0, 'F 15 O0': 0, 'F 15 O1': 1, 'F 16-17 W0': 24, 'F 16-17 W1': 0, 'F 16-17 W2': 0, 'F 16-17 W3': 2, 'F 16-17 M0': 1, 'F 16-17 M1': 0, 'F 16-17 M2': 0, 'F 16-17 M3': 3, 'F 16-17 A0': 3, 'F 16-17 A1': 5, 'F 16-17 A2': 2, 'F 16-17 A3': 2, 'F 16-17 A4': 2, 'F 16-17 B0': 1, 'F 16-17 B1': 1, 'F 16-17 B2': 0, 'F 16-17 O0': 0, 'F 16-17 O1': 0, 'F 18-19 W0': 277, 'F 18-19 W1': 0, 'F 18-19 W2': 0, 'F 18-19 W3': 35, 'F 18-19 M0': 3, 'F 18-19 M1': 1, 'F 18-19 M2': 5, 'F 18-19 M3': 0, 'F 18-19 A0': 8, 'F 18-19 A1': 8, 'F 18-19 A2': 1, 'F 18-19 A3': 8, 'F 18-19 A4': 10, 'F 18-19 B0': 15, 'F 18-19 B1': 3, 'F 18-19 B2': 0, 'F 18-19 O0': 4, 'F 18-19 O1': 3, 'F 20-24 W0': 457, 'F 20-24 W1': 9, 'F 20-24 W2': 0, 'F 20-24 W3': 103, 'F 20-24 M0': 13, 'F 20-24 M1': 1, 'F 20-24 M2': 7, 'F 20-24 M3': 9, 'F 20-24 A0': 36, 'F 20-24 A1': 12, 'F 20-24 A2': 4, 'F 20-24 A3': 37, 'F 20-24 A4': 39, 'F 20-24 B0': 41, 'F 20-24 B1': 11, 'F 20-24 B2': 2, 'F 20-24 O0': 7, 'F 20-24 O1': 3, 'F 25-29 W0': 162, 'F 25-29 W1': 5, 'F 25-29 W2': 0, 'F 25-29 W3': 78, 'F 25-29 M0': 9, 'F 25-29 M1': 1, 'F 25-29 M2': 6, 'F 25-29 M3': 3, 'F 25-29 A0': 29, 'F 25-29 A1': 14, 'F 25-29 A2': 8, 'F 25-29 A3': 20, 'F 25-29 A4': 24, 'F 25-29 B0': 13, 'F 25-29 B1': 9, 'F 25-29 B2': 5, 'F 25-29 O0': 5, 'F 25-29 O1': 3, 'F 30-34 W0': 128, 'F 30-34 W1': 3, 'F 30-34 W2': 0, 'F 30-34 W3': 59, 'F 30-34 M0': 0, 'F 30-34 M1': 4, 'F 30-34 M2': 2, 'F 30-34 M3': 2, 'F 30-34 A0': 26, 'F 30-34 A1': 16, 'F 30-34 A2': 4, 'F 30-34 A3': 8, 'F 30-34 A4': 27, 'F 30-34 B0': 16, 'F 30-34 B1': 3, 'F 30-34 B2': 1, 'F 30-34 O0': 1, 'F 30-34 O1': 6, 'F 35-39 W0': 86, 'F 35-39 W1': 2, 'F 35-39 W2': 0, 'F 35-39 W3': 39, 'F 35-39 M0': 0, 'F 35-39 M1': 1, 'F 35-39 M2': 0, 'F 35-39 M3': 3, 'F 35-39 A0': 20, 'F 35-39 A1': 12, 'F 35-39 A2': 11, 'F 35-39 A3': 5, 'F 35-39 A4': 34, 'F 35-39 B0': 19, 'F 35-39 B1': 4, 'F 35-39 B2': 0, 'F 35-39 O0': 3, 'F 35-39 O1': 4, 'F 40-44 W0': 78, 'F 40-44 W1': 0, 'F 40-44 W2': 0, 'F 40-44 W3': 13, 'F 40-44 M0': 3, 'F 40-44 M1': 3, 'F 40-44 M2': 1, 'F 40-44 M3': 3, 'F 40-44 A0': 10, 'F 40-44 A1': 6, 'F 40-44 A2': 2, 'F 40-44 A3': 3, 'F 40-44 A4': 12, 'F 40-44 B0': 12, 'F 40-44 B1': 1, 'F 40-44 B2': 2, 'F 40-44 O0': 0, 'F 40-44 O1': 0, 'F 45-49 W0': 90, 'F 45-49 W1': 0, 'F 45-49 W2': 0, 'F 45-49 W3': 13, 'F 45-49 M0': 1, 'F 45-49 M1': 3, 'F 45-49 M2': 0, 'F 45-49 M3': 1, 'F 45-49 A0': 12, 'F 45-49 A1': 3, 'F 45-49 A2': 3, 'F 45-49 A3': 2, 'F 45-49 A4': 12, 'F 45-49 B0': 4, 'F 45-49 B1': 6, 'F 45-49 B2': 0, 'F 45-49 O0': 3, 'F 45-49 O1': 0, 'F 50-54 W0': 91, 'F 50-54 W1': 1, 'F 50-54 W2': 0, 'F 50-54 W3': 10, 'F 50-54 M0': 2, 'F 50-54 M1': 0, 'F 50-54 M2': 0, 'F 50-54 M3': 4, 'F 50-54 A0': 5, 'F 50-54 A1': 4, 'F 50-54 A2': 0, 'F 50-54 A3': 2, 'F 50-54 A4': 2, 'F 50-54 B0': 9, 'F 50-54 B1': 2, 'F 50-54 B2': 0, 'F 50-54 O0': 0, 'F 50-54 O1': 1, 'F 55-59 W0': 107, 'F 55-59 W1': 2, 'F 55-59 W2': 0, 'F 55-59 W3': 5, 'F 55-59 M0': 0, 'F 55-59 M1': 0, 'F 55-59 M2': 0, 'F 55-59 M3': 0, 'F 55-59 A0': 2, 'F 55-59 A1': 3, 'F 55-59 A2': 0, 'F 55-59 A3': 3, 'F 55-59 A4': 4, 'F 55-59 B0': 3, 'F 55-59 B1': 0, 'F 55-59 B2': 0, 'F 55-59 O0': 1, 'F 55-59 O1': 0, 'F 60-64 W0': 96, 'F 60-64 W1': 5, 'F 60-64 W2': 0, 'F 60-64 W3': 6, 'F 60-64 M0': 0, 'F 60-64 M1': 0, 'F 60-64 M2': 0, 'F 60-64 M3': 0, 'F 60-64 A0': 4, 'F 60-64 A1': 3, 'F 60-64 A2': 0, 'F 60-64 A3': 3, 'F 60-64 A4': 2, 'F 60-64 B0': 2, 'F 60-64 B1': 2, 'F 60-64 B2': 0, 'F 60-64 O0': 0, 'F 60-64 O1': 0, 'F 65-69 W0': 71, 'F 65-69 W1': 1, 'F 65-69 W2': 0, 'F 65-69 W3': 3, 'F 65-69 M0': 1, 'F 65-69 M1': 0, 'F 65-69 M2': 0, 'F 65-69 M3': 0, 'F 65-69 A0': 1, 'F 65-69 A1': 2, 'F 65-69 A2': 1, 'F 65-69 A3': 1, 'F 65-69 A4': 0, 'F 65-69 B0': 0, 'F 65-69 B1': 4, 'F 65-69 B2': 0, 'F 65-69 O0': 1, 'F 65-69 O1': 0, 'F 70-74 W0': 69, 'F 70-74 W1': 2, 'F 70-74 W2': 0, 'F 70-74 W3': 7, 'F 70-74 M0': 0, 'F 70-74 M1': 0, 'F 70-74 M2': 0, 'F 70-74 M3': 0, 'F 70-74 A0': 0, 'F 70-74 A1': 1, 'F 70-74 A2': 1, 'F 70-74 A3': 2, 'F 70-74 A4': 0, 'F 70-74 B0': 0, 'F 70-74 B1': 2, 'F 70-74 B2': 0, 'F 70-74 O0': 0, 'F 70-74 O1': 1, 'F 75-79 W0': 69, 'F 75-79 W1': 4, 'F 75-79 W2': 0, 'F 75-79 W3': 3, 'F 75-79 M0': 0, 'F 75-79 M1': 0, 'F 75-79 M2': 0, 'F 75-79 M3': 0, 'F 75-79 A0': 0, 'F 75-79 A1': 0, 'F 75-79 A2': 0, 'F 75-79 A3': 0, 'F 75-79 A4': 1, 'F 75-79 B0': 0, 'F 75-79 B1': 0, 'F 75-79 B2': 1, 'F 75-79 O0': 0, 'F 75-79 O1': 0, 'F 80-84 W0': 90, 'F 80-84 W1': 0, 'F 80-84 W2': 0, 'F 80-84 W3': 3, 'F 80-84 M0': 0, 'F 80-84 M1': 0, 'F 80-84 M2': 0, 'F 80-84 M3': 1, 'F 80-84 A0': 0, 'F 80-84 A1': 0, 'F 80-84 A2': 0, 'F 80-84 A3': 0, 'F 80-84 A4': 0, 'F 80-84 B0': 0, 'F 80-84 B1': 0, 'F 80-84 B2': 1, 'F 80-84 O0': 0, 'F 80-84 O1': 0, 'F 85+ W0': 85, 'F 85+ W1': 2, 'F 85+ W2': 0, 'F 85+ W3': 5, 'F 85+ M0': 0, 'F 85+ M1': 0, 'F 85+ M2': 0, 'F 85+ M3': 0, 'F 85+ A0': 0, 'F 85+ A1': 0, 'F 85+ A2': 0, 'F 85+ A3': 0, 'F 85+ A4': 0, 'F 85+ B0': 1, 'F 85+ B1': 1, 'F 85+ B2': 0, 'F 85+ O0': 0, 'F 85+ O1': 0}


def temp():
    ethnicity = random.choices(list(CROSS_TABLES['sex_age_ethnicity'].keys()), list(CROSS_TABLES['sex_age_ethnicity'].values()), k=Total)
    # comb = [(age[i], sex[i], ethnicity[i]) for i in range(0, Total)]
    print(ethnicity)
    # individual = [{'age': c[0], 'sex': c[1], 'ethnicity': c[2]} for c in comb]

# Total = 7303
Total = round(7303*0.2)
ages = reduce(ages, 0.2, Total)
sexes = reduce(sexes, 0.2, Total)
ethnicities = reduce(ethnicities, 0.2, Total)
CROSS_TABLES['sex_age'] = reduce(CROSS_TABLES['sex_age'], 0.2, Total)
CROSS_TABLES['sex_age_ethnicity'] = reduce(CROSS_TABLES['sex_age_ethnicity'], 0.2, Total)

def getStats(individual, crosstable):
    attributes = crosstable.split('_')
    counter = Counter()
    for entry in individual:
        counter[entry[attributes[0]] + " " + entry[attributes[1]] + " " + entry[attributes[2]]] += 1
        # if len(attributes) < 3:
        #     counter[entry[attributes[0]] + " " + entry[attributes[1]]]  += 1
        # else:
        #     counter[entry[attributes[0]] + " " + entry[attributes[1]] + " " + entry[attributes[2]]] += 1
    sorted_counter = dict(OrderedDict((key, counter[key]) for key in CROSS_TABLES[crosstable].keys()))
    return  sorted_counter

def fitnessfunction(individual):
    # fitness for age_sex
    # a = np.array(list(CROSS_TABLES['sex_age'].values()))
    # p = np.array(list(getStats(individual, 'sex_age').values()))
    # rmse_age_sex = np.sqrt(((p - a) ** 2).mean())
    # fitness for age_sex_ethnicity
    a = np.array(list(CROSS_TABLES['sex_age_ethnicity'].values()))
    p = np.array(list(getStats(individual, 'sex_age_ethnicity').values()))
    rmse_age_sex_ethnicity = np.sqrt(((p - a) ** 2).mean())
    return 0, rmse_age_sex_ethnicity

def evaluate(population):
    fitness = []
    # Create a ThreadPoolExecutor instance and use the map method to execute the function in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = executor.map(fitnessfunction, population)
        # Collect and print the results
        for result in results:
            fitness.append(result)
    return fitness

def random_person():
    # age = random.choice(list(ages.keys()))
    # sex = random.choice(list(sexes.keys()))
    age = random.choices(list(ages.keys()), list(ages.values()), k=1)[0]
    sex = random.choices(list(sexes.keys()), list(sexes.values()), k=1)[0]
    ethnicity = random.choices(list(ethnicities.keys()), list(ethnicities.values()), k=1)[0]
    return {'age': age, 'sex': sex, 'ethnicity': ethnicity}

def create_individual():
    # Create a random individual
    Total = 3
    age = random.choices(list(ages.keys()), list(ages.values()), k=Total)
    sex = random.choices(list(sexes.keys()), list(sexes.values()), k=Total)
    ethnicity = random.choices(list(ethnicities.keys()), list(ethnicities.values()), k=Total)
    comb = [(age[i], sex[i], ethnicity[i]) for i in range(0,Total)]
    individual1 = [{'age':c[0], 'sex':c[1], 'ethnicity':c[2]} for c in comb]
    individual2 = random.choices(list(CROSS_TABLES['sex_age_ethnicity'].keys()), list(CROSS_TABLES['sex_age_ethnicity'].values()), k=Total)

    print(individual1)
    print(individual2)
    # return creator.Individual(individual)

def mutation(individual, mutation_probability):
    # Apply the mutation operator to the individual
    for i in range(len(individual)):
        if random.random() < mutation_probability:
            individual[i] = random_person()
    return individual,

def main():
    # Define the problem dimensions
    creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
    creator.create("Individual", list, fitness=creator.Fitness)
    toolbox = base.Toolbox()
    # toolbox.register("person", random_person)
    # toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.person, n=Total)
    toolbox.register("individual", create_individual)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # Define the genetic operators
    toolbox.register("evaluate", evaluate)
    toolbox.register("mate", tools.cxTwoPoint)
    # toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.5)
    toolbox.register("mutate", mutation, mutation_probability=0.1)
    toolbox.register("select", tools.selNSGA2)

    ind = create_individual()
    # Set the initial parameters
    POP_SIZE = 100
    NGEN = 100
    MU = 10
    LAMBDA = POP_SIZE
    CXPB = 0.9
    MUTPB = 0.1

    # Create the initial population
    pop = toolbox.population(n=POP_SIZE)
    # Evaluate the initial population
    fitnesses = toolbox.evaluate(pop)
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # Set up a statistics object to keep track of the progress
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", statistics.mean)
    stats.register("min", tools.selBest, k=1, fit_attr='fitness')
    stats.register("max", tools.selWorst, k=1, fit_attr='fitness')

    # Main loop for the genetic algorithm
    for gen in range(NGEN):
        # Generate offspring through variation (crossover and mutation)
        offspring = algorithms.varOr(pop, toolbox, lambda_=LAMBDA, cxpb=CXPB, mutpb=MUTPB)
        # Evaluate offspring
        fitnesses = toolbox.evaluate(offspring)
        for ind, fit in zip(offspring, fitnesses):
            ind.fitness.values = fit
        # Select the next generation individuals
        pop = toolbox.select(offspring, k=MU)
        print(gen, min(fitnesses))

if __name__ == '__main__':
    main()
    # temp()