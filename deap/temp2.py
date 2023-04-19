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
import os
import random
from collections import Counter
from deap import base, creator, tools

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
    rmse = np.sqrt(((p - a) ** 2).mean())
    fig = go.Figure()
    fig.add_trace(go.Scatter(x0='data', x=list(actual.keys()), name='actual', y=list(actual.values()), line_color='#636EFA'))
    fig.add_trace(go.Scatter(x0='data', x=list(predicted.keys()), name='pred', y=list(predicted.values()), line_color='#EF553B'))
    fig.update_layout(width=width, title=name + "  " + 'RMSE=' + str(rmse))
    py.offline.plot(fig, filename="graphs\\" + name + ".html")
    fig.show()

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

def agegroup(category):
    if category == 'C':
        return ['0-4', '5-7', '8-9', '10-14', '15']
    elif category == 'A':
        return ['16-17', '18-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64']
    elif category == 'E':
        return [ '65-69', '70-74', '75-79', '80-84', '85+']

HH_sizes = {'1': 857, '2': 684, '3': 413, '4': 324, '5': 149, '6': 74, '7': 16, '8': 10}
HH_types = {'person': 857, 'family': 1166, 'other': 504}
#E = Elder, A = Adult, C = Child
HH_compositions = {'1E_0C': 285, '1A_0C': 572, '1A_1C': 205, '2E_0C': 187, '2A_1C': 238, '2A_0C': 389, '2A_3C': 53,
                   '3A_1C': 118, '3A_0C': 480}

sex_age_HH_compositions = {'M 0-15 1E_0C': 0, 'M 0-15 1A_0C': 1, 'M 0-15 2E_0C': 0, 'M 0-15 3A_1C': 72, 'M 0-15 3A_0C': 0, 'M 16-24 1E_0C': 0, 'M 16-24 1A_0C': 19, 'M 16-24 2E_0C': 0, 'M 16-24 3A_1C': 31, 'M 16-24 3A_0C': 353, 'M 25-34 1E_0C': 0, 'M 25-34 1A_0C': 84, 'M 25-34 2E_0C': 0, 'M 25-34 3A_1C': 42, 'M 25-34 3A_0C': 255, 'M 35-49 1E_0C': 0, 'M 35-49 1A_0C': 123, 'M 35-49 2E_0C': 0, 'M 35-49 3A_1C': 52, 'M 35-49 3A_0C': 74, 'M 50+ 1E_0C': 92, 'M 50+ 1A_0C': 71, 'M 50+ 2E_0C': 113, 'M 50+ 3A_1C': 26, 'M 50+ 3A_0C': 50, 'F 0-15 1E_0C': 0, 'F 0-15 1A_0C': 0, 'F 0-15 2E_0C': 0, 'F 0-15 3A_1C': 78, 'F 0-15 3A_0C': 0, 'F 16-24 1E_0C': 0, 'F 16-24 1A_0C': 37, 'F 16-24 2E_0C': 0, 'F 16-24 3A_1C': 24, 'F 16-24 3A_0C': 387, 'F 25-34 1E_0C': 0, 'F 25-34 1A_0C': 72, 'F 25-34 2E_0C': 0, 'F 25-34 3A_1C': 62, 'F 25-34 3A_0C': 184, 'F 35-49 1E_0C': 0, 'F 35-49 1A_0C': 82, 'F 35-49 2E_0C': 0, 'F 35-49 3A_1C': 59, 'F 35-49 3A_0C': 64, 'F 50+ 1E_0C': 193, 'F 50+ 1A_0C': 83, 'F 50+ 2E_0C': 120, 'F 50+ 3A_1C': 26, 'F 50+ 3A_0C': 69, 'M 0-15 2A_0C': 0, 'M 0-15 2A_1C': 283, 'M 0-15 2A_3C': 0, 'M 0-15 1A_1C': 201, 'M 16-24 2A_0C': 12, 'M 16-24 2A_1C': 59, 'M 16-24 2A_3C': 44, 'M 16-24 1A_1C': 55, 'M 25-34 2A_0C': 96, 'M 25-34 2A_1C': 89, 'M 25-34 2A_3C': 51, 'M 25-34 1A_1C': 20, 'M 35-49 2A_0C': 59, 'M 35-49 2A_1C': 195, 'M 35-49 2A_3C': 35, 'M 35-49 1A_1C': 21, 'M 50+ 2A_0C': 105, 'M 50+ 2A_1C': 35, 'M 50+ 2A_3C': 121, 'M 50+ 1A_1C': 33, 'F 0-15 2A_0C': 0, 'F 0-15 2A_1C': 281, 'F 0-15 2A_3C': 0, 'F 0-15 1A_1C': 183, 'F 16-24 2A_0C': 21, 'F 16-24 2A_1C': 57, 'F 16-24 2A_3C': 35, 'F 16-24 1A_1C': 104, 'F 25-34 2A_0C': 101, 'F 25-34 2A_1C': 128, 'F 25-34 2A_3C': 19, 'F 25-34 1A_1C': 89, 'F 35-49 2A_0C': 39, 'F 35-49 2A_1C': 161, 'F 35-49 2A_3C': 41, 'F 35-49 1A_1C': 95, 'F 50+ 2A_0C': 101, 'F 50+ 2A_1C': 17, 'F 50+ 2A_3C': 103, 'F 50+ 1A_1C': 74}

path = os.path.join(os.path.dirname(os.getcwd()))
popdf = pd.read_csv(os.path.join(path, 'deap', 'graphs', 'population.csv')).reset_index()
popdf = popdf.rename({'index': 'id'}, axis=1)
popdf = popdf.sample(frac=0.9) #filter communals
population = getdictionary(popdf)
PERSONS = population.copy()
PoP_Total = len(population)
Total = sum(list(HH_types.values()))

def get_sex_age_HH_compositions_Stats(individual):
    temp = []
    for ind in individual:
        persons = ind['persons']
        for pid in persons:
            person = [k for k in PERSONS if k['id'] == pid][0]
            temp.append(person['sex'] + " " + agemap(person['age']) + " " +  ind['composition'])

    predicted = Counter(temp)
    return dict([(k, predicted[k]) for k in list(sex_age_HH_compositions.keys())])

def getStats(individual):
    hh_sizes = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0}
    hh_types = {'person': 0, 'family': 0, 'other': 0}
    hh_compositions = {'1E_0C': 0, '1A_0C': 0, '1A_1C': 0, '2E_0C': 0, '2A_1C': 0, '2A_0C': 0, '2A_3C': 0, '3A_1C': 0,
                       '3A_0C': 0}

    for ind in individual:
        hh_sizes[str(ind['size'])]+=1
        hh_types[ind['type']] += 1
        hh_compositions[ind['composition']] += 1
    return hh_sizes, hh_types, hh_compositions

# Define the fitness function
def evaluate(individual):
    pred_HH_sizes, pred_HH_types, pred_HH_compositions = getStats(individual)

    a = np.array(list(HH_sizes.values()))
    p = np.array(list(pred_HH_sizes.values()))
    rmse_HH_sizes = np.sqrt(((p - a) ** 2).mean())

    a = np.array(list(HH_types.values()))
    p = np.array(list(pred_HH_types.values()))
    rmse_HH_types = np.sqrt(((p - a) ** 2).mean())

    a = np.array(list(HH_compositions.values()))
    p = np.array(list(pred_HH_compositions.values()))
    rmse_HH_compositions = np.sqrt(((p - a) ** 2).mean())

    a = np.array(list(sex_age_HH_compositions.values()))
    p = np.array(list(get_sex_age_HH_compositions_Stats(individual).values()))
    rmse_sex_age_HH_compositions = np.sqrt(((p - a) ** 2).mean())

    return rmse_HH_sizes, rmse_HH_types,  rmse_HH_compositions, rmse_sex_age_HH_compositions

def validate(household):
    #validation rule#1:
    return household

def get_random_persons(households):
    pop = population.copy()
    print(len(pop))
    subpop = {'E': [k for k in pop if k['age'] in agegroup('E')],
              'A': [k for k in pop if k['age'] in agegroup('A')],
              'C': [k for k in pop if k['age'] in agegroup('C')]}
    HH = []
    for house in households:
        persons_list = []
        comp = house['composition'].split('_')
        size = house['size']
        type_A = comp[0][1:2]
        size_A = int(comp[0][0:1])
        if len(subpop[type_A]) > 0:
            persons = random.choices(subpop[type_A], k=size_A)
            for person in persons:
                [pop.remove(x) for x in pop if x['id'] == person['id']]
                persons_list.append(person['id'])

        type_B = comp[1][1:2]
        size_B = int(comp[1][0:1])
        kB = size
        if len(subpop[type_B]) > 0:
            persons = random.choices(subpop[type_B], k=kB)
            for person in persons:
                [pop.remove(x) for x in pop if x['id'] == person['id']]
                persons_list.append(person['id'])
        house['persons']= persons_list
        HH.append(house)
    print(len(pop))
    return HH


def random_household(households):
    # hh_size = random.choices(list(HH_sizes.keys()), list(HH_sizes.values()), k=1)[0]
    # if hh_size == '8+':
    #     hh_size = 8
    # else:
    #     hh_size = int(hh_size)
    # hh_compositions = random.choices(list(HH_compositions.keys()), list(HH_compositions.values()), k=1)[0]
    # hh_type = random.choices(list(HH_types.keys()), list(HH_types.values()), k=1)[0]

    A = random.randrange(0, len(households)-1)
    B = random.randrange(0, len(households) - 1)
    if A != B:
        hh_A = households[A]
        hh_B = households[B]
        temp = hh_A['persons']
        hh_A['persons'] = hh_B['persons']
        hh_B['persons'] = temp
    households[A] = hh_A
    households[B] = hh_B
    return households

def random_households():
    hh_size = random.choices(list(HH_sizes.keys()), list(HH_sizes.values()), k=Total)
    hh_size = [int(i) for i in hh_size]
    hh_type = random.choices(list(HH_types.keys()), list(HH_types.values()), k=Total)
    hh_compositions = random.choices(list(HH_compositions.keys()), list(HH_compositions.values()), k=Total)

    comb = [(hh_size[i], hh_type[i], hh_compositions[i]) for i in range(0, Total)]
    HH = [validate({'size': c[0], 'type': c[1], 'composition': c[2]}) for c in comb]

    HH = get_random_persons(HH)
    return HH
random_households()
def mutation(individual, mutation_probability):
    # Apply the mutation operator to the individual
    # for i in range(len(individual)):
    #     if random.random() < mutation_probability:
    #         individual[i] = random_household()
    individual = random_household(individual)
    return individual,
#
# # Create a toolbox for the genetic algorithm
# creator.create('FitnessMin', base.Fitness, weights=(-1.0, -1.0, -1.0, -1.0))
# creator.create('Individual', list, fitness=creator.FitnessMin)
# toolbox = base.Toolbox()
# toolbox.register("household", random_household)
# # toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.household, n=Total)
# toolbox.register("individual", random_households)
# toolbox.register("population", tools.initRepeat, list, toolbox.individual)
#
#
# # Register genetic operators
# toolbox.register('evaluate', evaluate)
# toolbox.register('mate', tools.cxTwoPoint)
# toolbox.register("mutate", mutation, mutation_probability=0.2)
# # toolbox.register('select', tools.selTournament, tournsize=25)
# toolbox.register("select", tools.selNSGA2)
#
# # Generate households
# POP_SIZE = 10
# NGEN = 2
# mu = 25
# lambda_ = POP_SIZE
# cxpb = 0.8
# mutpb = 0.2
# pop = toolbox.population(n=POP_SIZE)
# hof = tools.ParetoFront()
# stats = tools.Statistics(lambda ind: ind.fitness.values)
# stats.register("min", np.min, axis=0)
#
# pop, log = algorithms.eaMuPlusLambda(pop, toolbox, mu, lambda_, cxpb, mutpb, ngen=NGEN, stats=stats, verbose=True, halloffame=hof)
# # Calculate the weighted sum for each individual in the Pareto front (Hall of Fame)
# # Print the best individual
# best_individual = tools.selBest(pop, k=1)[0]
# records = []
# for ind in best_individual:
#     records.append(ind)
# df = pd.DataFrame(records)
# # df.to_csv('graphs\households.csv', index=False)
# pred_HH_sizes, pred_HH_types, pred_HH_compositions = getStats(best_individual)
# plot(HH_sizes, pred_HH_sizes, 'HH_sizes2')
# plot(HH_types, pred_HH_types, 'HH_types2')
# plot(HH_compositions, pred_HH_compositions, 'HH_compositions2')
