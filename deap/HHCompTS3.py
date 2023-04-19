from deap import base, creator, tools
import random
import numpy as np
import matplotlib.pyplot as plt
from deap import algorithms, base, creator, tools
from Person import Person
from collections import Counter
import plotly.graph_objs as go
import  plotly as py
import plotly.express as px
import multiprocessing
import concurrent.futures
from scipy.integrate import trapz
import os
import pandas as pd
import itertools
from itertools import permutations
from joblib import Parallel, delayed, parallel_backend

def getdictionary(df):
    records = []
    for index, row in df.iterrows():
        dic = {}
        for index, column in enumerate(df.columns):
            dic[column] = row[column]
        records.append((dic))
    return records

def plot(actual, predicted, name, width=1000):
    a = np.array(list(actual.values()))
    p = np.array(list(predicted.values()))
    y_pred = list(predicted.values())
    rmse = np.sqrt(((p - a) ** 2).mean())

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x0='data', x=list(actual.keys()), name='actual', y=list(actual.values()), line_color='#636EFA'))
    fig.add_trace(go.Scatter(x0='data', x=list(predicted.keys()), name='pred', y=y_pred, line_color='#EF553B'))
    fig.update_layout(width=width, title=name + "  " + 'RMSE=' + str(rmse))
    py.offline.plot(fig, filename="graphs\\" + name + ".html")
    fig.show()

path = os.path.join(os.path.dirname(os.getcwd()))
popdf = pd.read_csv(os.path.join(path, 'deap', 'graphs', 'population.csv')).reset_index()
popdf = popdf.rename({'index': 'id'}, axis=1)
households = pd.read_csv(os.path.join(path, 'deap', 'graphs', 'households2.csv'))
households = getdictionary(households)
sex_age_HH_compositions = {'M 0-15 1E_0C': 0, 'M 0-15 1A_0C': 1, 'M 0-15 2E_0C': 0, 'M 0-15 3A_1C': 72, 'M 0-15 3A_0C': 0, 'M 16-24 1E_0C': 0, 'M 16-24 1A_0C': 19, 'M 16-24 2E_0C': 0, 'M 16-24 3A_1C': 31, 'M 16-24 3A_0C': 353, 'M 25-34 1E_0C': 0, 'M 25-34 1A_0C': 84, 'M 25-34 2E_0C': 0, 'M 25-34 3A_1C': 42, 'M 25-34 3A_0C': 255, 'M 35-49 1E_0C': 0, 'M 35-49 1A_0C': 123, 'M 35-49 2E_0C': 0, 'M 35-49 3A_1C': 52, 'M 35-49 3A_0C': 74, 'M 50+ 1E_0C': 92, 'M 50+ 1A_0C': 71, 'M 50+ 2E_0C': 113, 'M 50+ 3A_1C': 26, 'M 50+ 3A_0C': 50, 'F 0-15 1E_0C': 0, 'F 0-15 1A_0C': 0, 'F 0-15 2E_0C': 0, 'F 0-15 3A_1C': 78, 'F 0-15 3A_0C': 0, 'F 16-24 1E_0C': 0, 'F 16-24 1A_0C': 37, 'F 16-24 2E_0C': 0, 'F 16-24 3A_1C': 24, 'F 16-24 3A_0C': 387, 'F 25-34 1E_0C': 0, 'F 25-34 1A_0C': 72, 'F 25-34 2E_0C': 0, 'F 25-34 3A_1C': 62, 'F 25-34 3A_0C': 184, 'F 35-49 1E_0C': 0, 'F 35-49 1A_0C': 82, 'F 35-49 2E_0C': 0, 'F 35-49 3A_1C': 59, 'F 35-49 3A_0C': 64, 'F 50+ 1E_0C': 193, 'F 50+ 1A_0C': 83, 'F 50+ 2E_0C': 120, 'F 50+ 3A_1C': 26, 'F 50+ 3A_0C': 69, 'M 0-15 2A_0C': 0, 'M 0-15 2A_1C': 283, 'M 0-15 2A_3C': 0, 'M 0-15 1A_1C': 201, 'M 16-24 2A_0C': 12, 'M 16-24 2A_1C': 59, 'M 16-24 2A_3C': 44, 'M 16-24 1A_1C': 55, 'M 25-34 2A_0C': 96, 'M 25-34 2A_1C': 89, 'M 25-34 2A_3C': 51, 'M 25-34 1A_1C': 20, 'M 35-49 2A_0C': 59, 'M 35-49 2A_1C': 195, 'M 35-49 2A_3C': 35, 'M 35-49 1A_1C': 21, 'M 50+ 2A_0C': 105, 'M 50+ 2A_1C': 35, 'M 50+ 2A_3C': 121, 'M 50+ 1A_1C': 33, 'F 0-15 2A_0C': 0, 'F 0-15 2A_1C': 281, 'F 0-15 2A_3C': 0, 'F 0-15 1A_1C': 183, 'F 16-24 2A_0C': 21, 'F 16-24 2A_1C': 57, 'F 16-24 2A_3C': 35, 'F 16-24 1A_1C': 104, 'F 25-34 2A_0C': 101, 'F 25-34 2A_1C': 128, 'F 25-34 2A_3C': 19, 'F 25-34 1A_1C': 89, 'F 35-49 2A_0C': 39, 'F 35-49 2A_1C': 161, 'F 35-49 2A_3C': 41, 'F 35-49 1A_1C': 95, 'F 50+ 2A_0C': 101, 'F 50+ 2A_1C': 17, 'F 50+ 2A_3C': 103, 'F 50+ 1A_1C': 74}

Total = sum([k['size'] for k in households])
popdf = popdf.sample(n=Total)
population = getdictionary(popdf)
PERSONS = population.copy()

HH_Total = len(households)
PoP_Total = len(population)

def getStats(individual):
    temp = []
    for ind in individual:
        persons = ind['persons']
        for pid in persons:
            person = [k for k in PERSONS if k['id'] == pid][0]
            temp.append(person['sex'] + " " + agemap(person['age']) + " " +  ind['composition'])

    predicted = Counter(temp)
    return dict([(k, predicted[k]) for k in list(sex_age_HH_compositions.keys())])

def agegroup(category):
    if category == 'C':
        return ['0-4', '5-7', '8-9', '10-14', '15']
    elif category == 'A':
        return ['16-17', '18-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64']
    elif category == 'E':
        return [ '65-69', '70-74', '75-79', '80-84', '85+']

def agemap(age):
    if age in ['0-4', '5-7', '8-9', '10-14', '15']:
        return "0-15"
    elif age in ['16-17', '18-19', '20-24']:
        return "16-24"
    elif age in ['25-29', '30-34']:
        return "25-34"
    elif age in ['35-39', '40-44', '45-49']:
        return "35-49"
    elif age in ['50-54', '55-59', '60-64', '65-69', '70-74', '75-79', '80-84', '85+']:
        return "50+"

# Define the fitness function
def evaluate(individual):
    a = np.array(list(sex_age_HH_compositions.values()))
    p = np.array(list(getStats(individual).values()))
    rmse = np.sqrt(((p - a) ** 2).mean())
    return rmse

def get_persons_ages(composition, size):
    # '1E_0C', '1A_0C', '1A_1C', '2E_0C', '2A_1C', '2A_0C', '2A_3C', '3A_1C', '3A_0C'
    plist = []
    comp = composition.split('_')
    typeA = comp[0][1:2]
    sizeA = int(comp[0][0:1]) + random.randrange(0,2)
    for s in range(sizeA):
        plist.append(typeA)

    sizeB = int(comp[1][0:1])
    for s in range(sizeB):
        plist.append('C')
    return plist

def random_household():
    pop = population.copy()
    for index, house in enumerate(households):
        persons = []
        size = house['size']
        composition = house['composition']
        ptypes = get_persons_ages(composition, size)
        for ptype in ptypes:
            samples = [k for k in pop if k['age'] in agegroup(ptype)]
            if len(samples)>0:
                person = random.choice(samples)
                pop.remove(person)
                persons.append(person['id'])
        house['persons'] = persons
        households[index] = house
    return households

def generate_neighbors_parallel(solution):
    # Generate neighboring solutions in parallel using multiple threads
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(generate_neighbor, solution, i) for i in range(10)]
        neighbors = [future.result() for future in futures]
    return neighbors

def generate_neighbor(solution, i):
    # Generate a single neighbor by making a small modification to the current solution
    neighbor = solution.copy()
    if random.random() < 0.90:
        A = random.randrange(0, len(neighbor) - 1)
        B = random.randrange(0, len(neighbor) - 1)
        if A != B:
            hh_A = neighbor[A]
            hh_B = neighbor[B]
            temp = hh_A['persons']
            hh_A['persons'] = hh_B['persons']
            hh_B['persons'] = temp
            neighbor[A] = hh_A
            neighbor[B] = hh_B
    else:
        neighbor = random_household()
        print('reproduced')
    return neighbor

def tabu_search(initial_solution, objective_function, tabu_size, max_iterations):
    tabu_list = []  # List of tabu solutions
    current_solution = initial_solution  # Initialize current solution
    current_fitness = objective_function(current_solution)  # Evaluate current solution
    for i in range(max_iterations):
        neighbors = generate_neighbors_parallel(current_solution)  # Generate neighboring solutions
        best_neighbor = None
        best_fitness = current_fitness
        for neighbor in neighbors:
            if neighbor not in tabu_list:
                fitness = objective_function(neighbor)  # Evaluate neighbor solution
                print(i, fitness, best_fitness)
                if fitness < best_fitness:
                    best_neighbor = neighbor
                    best_fitness = fitness

        if best_neighbor is not None:
            current_solution = best_neighbor  # Move to the best neighbor
            current_fitness = best_fitness
            tabu_list.append(current_solution)  # Add current solution to the tabu list
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)  # Remove oldest solution from the tabu list
    return current_solution, current_fitness

creator.create("Fitness", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()
toolbox.register("solution", random_household)
toolbox.register("evaluate", evaluate)
initial_solution = toolbox.solution()
print('Initial solution:' , toolbox.evaluate(initial_solution))

toolbox.register("tabu_search", tabu_search, initial_solution, evaluate,
                 tabu_size=50, max_iterations=10)

# Perform tabu search
result = toolbox.tabu_search()
best_individual = result[0]
records = []
for ind in best_individual:
    records.append(ind)
df = pd.DataFrame(records)
# df.to_csv('graphs\households3.csv', index=False)
plot(sex_age_HH_compositions, getStats(initial_solution), 'sex_age_composition')