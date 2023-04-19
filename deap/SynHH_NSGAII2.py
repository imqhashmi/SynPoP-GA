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

def agegroup(category):
    if category == 'C':
        return ['0-4', '5-7', '8-9', '10-14', '15']
    elif category == 'A':
        return ['16-17', '18-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54', '55-59', '60-64']
    elif category == 'E':
        return [ '65-69', '70-74', '75-79', '80-84', '85+']

path = os.path.join(os.path.dirname(os.getcwd()))
population = pd.read_csv(os.path.join(path, 'deap', 'graphs', 'population.csv'))

HH_sizes = {'1': 857, '2': 684, '3': 413, '4': 324, '5': 149, '6': 74, '7': 16, '8+': 10}
HH_types = {'person': 857, 'family': 1166, 'other': 504}

#E = Elder, A = Adult, C = Child
HH_compositions = {'1E_0C': 285, '1A_0C': 572, '1A_1C': 205, '2E_0C': 187, '2A_1C': 238, '2A_0C': 389, '2A_3C': 53,
                   '3A_1C': 118, '3A_0C': 480}

popdf = pd.read_csv(os.path.join(path, 'deap', 'graphs', 'population.csv')).reset_index()
popdf = popdf.rename({'index': 'id'}, axis=1)
population = getdictionary(popdf)
sex_age_HH_compositions = {'M 0-15 1E_0C': 0, 'M 0-15 1A_0C': 1, 'M 0-15 2E_0C': 0, 'M 0-15 3A_1C': 72, 'M 0-15 3A_0C': 0, 'M 16-24 1E_0C': 0, 'M 16-24 1A_0C': 19, 'M 16-24 2E_0C': 0, 'M 16-24 3A_1C': 31, 'M 16-24 3A_0C': 353, 'M 25-34 1E_0C': 0, 'M 25-34 1A_0C': 84, 'M 25-34 2E_0C': 0, 'M 25-34 3A_1C': 42, 'M 25-34 3A_0C': 255, 'M 35-49 1E_0C': 0, 'M 35-49 1A_0C': 123, 'M 35-49 2E_0C': 0, 'M 35-49 3A_1C': 52, 'M 35-49 3A_0C': 74, 'M 50+ 1E_0C': 92, 'M 50+ 1A_0C': 71, 'M 50+ 2E_0C': 113, 'M 50+ 3A_1C': 26, 'M 50+ 3A_0C': 50, 'F 0-15 1E_0C': 0, 'F 0-15 1A_0C': 0, 'F 0-15 2E_0C': 0, 'F 0-15 3A_1C': 78, 'F 0-15 3A_0C': 0, 'F 16-24 1E_0C': 0, 'F 16-24 1A_0C': 37, 'F 16-24 2E_0C': 0, 'F 16-24 3A_1C': 24, 'F 16-24 3A_0C': 387, 'F 25-34 1E_0C': 0, 'F 25-34 1A_0C': 72, 'F 25-34 2E_0C': 0, 'F 25-34 3A_1C': 62, 'F 25-34 3A_0C': 184, 'F 35-49 1E_0C': 0, 'F 35-49 1A_0C': 82, 'F 35-49 2E_0C': 0, 'F 35-49 3A_1C': 59, 'F 35-49 3A_0C': 64, 'F 50+ 1E_0C': 193, 'F 50+ 1A_0C': 83, 'F 50+ 2E_0C': 120, 'F 50+ 3A_1C': 26, 'F 50+ 3A_0C': 69, 'M 0-15 2A_0C': 0, 'M 0-15 2A_1C': 283, 'M 0-15 2A_3C': 0, 'M 0-15 1A_1C': 201, 'M 16-24 2A_0C': 12, 'M 16-24 2A_1C': 59, 'M 16-24 2A_3C': 44, 'M 16-24 1A_1C': 55, 'M 25-34 2A_0C': 96, 'M 25-34 2A_1C': 89, 'M 25-34 2A_3C': 51, 'M 25-34 1A_1C': 20, 'M 35-49 2A_0C': 59, 'M 35-49 2A_1C': 195, 'M 35-49 2A_3C': 35, 'M 35-49 1A_1C': 21, 'M 50+ 2A_0C': 105, 'M 50+ 2A_1C': 35, 'M 50+ 2A_3C': 121, 'M 50+ 1A_1C': 33, 'F 0-15 2A_0C': 0, 'F 0-15 2A_1C': 281, 'F 0-15 2A_3C': 0, 'F 0-15 1A_1C': 183, 'F 16-24 2A_0C': 21, 'F 16-24 2A_1C': 57, 'F 16-24 2A_3C': 35, 'F 16-24 1A_1C': 104, 'F 25-34 2A_0C': 101, 'F 25-34 2A_1C': 128, 'F 25-34 2A_3C': 19, 'F 25-34 1A_1C': 89, 'F 35-49 2A_0C': 39, 'F 35-49 2A_1C': 161, 'F 35-49 2A_3C': 41, 'F 35-49 1A_1C': 95, 'F 50+ 2A_0C': 101, 'F 50+ 2A_1C': 17, 'F 50+ 2A_3C': 103, 'F 50+ 1A_1C': 74}
Total = 2527

def getStats(individual):
    hh_sizes = {'1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8+': 0}
    hh_types = {'person': 0, 'family': 0, 'other': 0}
    hh_compositions = {'1E_0C': 0, '1A_0C': 0, '1A_1C': 0, '2E_0C': 0, '2A_1C': 0, '2A_0C': 0, '2A_3C': 0, '3A_1C': 0,
                       '3A_0C': 0}

    for ind in individual:
        hh_sizes[ind['size']]+=1
        hh_types[ind['type']] += 1
        hh_compositions[ind['composition']] += 1
    return hh_sizes, hh_types, hh_compositions

def evaluateObj1(individual):
    pred_HH_sizes, pred_HH_types, pred_HH_compositions = getStats(individual)
    a = np.array(list(HH_sizes.values()))
    p = np.array(list(pred_HH_sizes.values()))
    rmse_HH_sizes = np.sqrt(((p - a) ** 2).mean())
    return rmse_HH_sizes

def evaluateObj2(individual):
    pred_HH_sizes, pred_HH_types, pred_HH_compositions = getStats(individual)
    a = np.array(list(HH_types.values()))
    p = np.array(list(pred_HH_types.values()))
    rmse_HH_types = np.sqrt(((p - a) ** 2).mean())
    return rmse_HH_types

def evaluateObj3(individual):
    pred_HH_sizes, pred_HH_types, pred_HH_compositions = getStats(individual)

    a = np.array(list(HH_compositions.values()))
    p = np.array(list(pred_HH_compositions.values()))
    rmse_HH_compositions = np.sqrt(((p - a) ** 2).mean())

    return rmse_HH_compositions

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

    return rmse_HH_sizes, rmse_HH_types,  rmse_HH_compositions

def validate(household):
    #validation rule#1:
    return household

def get_random_person(type, pop, k=1):
    persons_list = []
    if len(pop) > 0:
        persons = random.choices(pop, k=k)
        for person in persons:
            [pop.remove(x) for x in pop if x['id'] == person['id']]
            persons_list.append(person['id'])
    return persons_list, pop

def random_household():
    hh_size = random.choices(list(HH_sizes.keys()), list(HH_sizes.values()), k=1)[0]
    hh_compositions = random.choices(list(HH_compositions.keys()), list(HH_compositions.values()), k=1)[0]
    hh_type = random.choices(list(HH_types.keys()), list(HH_types.values()), k=1)[0]
    # if hh_size == '1':
    #     hh_compositions = random.choice(list(['1E_0C','1A_0C']))
    #     hh_type = 'person'
    # elif hh_size == '2':
    #     hh_compositions = random.choice(list(['1A_1C', '2A_0C', '2E_0C']))
    #     if hh_compositions in ['2A_0C', '2E_0C']:
    #         hh_type = 'person'
    #     else:
    #         hh_type = 'family'
    # elif hh_size in ['3']:
    #     hh_compositions = random.choice(list(['2A_1C','3A_0C']))
    #     if hh_compositions == ['3A_0C']:
    #         hh_type = random.choice(list(['person', 'other']))
    #     else:
    #         hh_type = 'family'
    # elif hh_size in ['4']:
    #     hh_compositions = random.choice(list(['2A_1C', '3A_0C', '3A_1C']))
    #     if hh_compositions == ['3A_0C']:
    #         hh_type = random.choice(list(['person', 'other']))
    #     else:
    #         hh_type = 'family'
    # elif hh_size in ['4', '5', '6', '7', '8+']:
    #     hh_compositions = random.choice(list(['2A_3C', '3A_1C']))
    #     hh_type = 'family'

    HH = validate({'size':hh_size, 'type':hh_type, 'composition':hh_compositions})
    return HH


def mutation(individual, mutation_probability):
    # Apply the mutation operator to the individual
    for i in range(len(individual)):
        if random.random() < mutation_probability:
            individual[i] = random_household()
    return individual,

# Create a toolbox for the genetic algorithm
creator.create('FitnessMin', base.Fitness, weights=(-0.5,-0.5, -1.0))
creator.create('Individual', list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()
toolbox.register("household", random_household)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.household, n=Total)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Register genetic operators
toolbox.register('evaluate', evaluate)
toolbox.register('mate', tools.cxTwoPoint)
toolbox.register("mutate", mutation, mutation_probability=0.2)
# toolbox.register('select', tools.selTournament, tournsize=25)
toolbox.register("select", tools.selNSGA2)

# Generate households
POP_SIZE = 100
NGEN = 2
mu = 25
lambda_ = POP_SIZE
cxpb = 0.8
mutpb = 0.2
pop = toolbox.population(n=POP_SIZE)
hof = tools.ParetoFront()
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("min", np.min, axis=0)

pop, log = algorithms.eaMuPlusLambda(pop, toolbox, mu, lambda_, cxpb, mutpb, ngen=NGEN, stats=stats, verbose=True, halloffame=hof)
# Calculate the weighted sum for each individual in the Pareto front (Hall of Fame)
# Print the best individual
best_individual = tools.selBest(pop, k=1)[0]
# records = []
# for ind in best_individual:
#     records.append(ind)
# df = pd.DataFrame(records)
# df.to_csv('graphs\households.csv', index=False)
# pred_HH_sizes, pred_HH_types, pred_HH_compositions = getStats(best_individual)
# plot(HH_sizes, pred_HH_sizes, 'HH_sizes')
# plot(HH_types, pred_HH_types, 'HH_types')
# plot(HH_compositions, pred_HH_compositions, 'HH_compositions')
import matplotlib.pyplot as plt

# Extract the Pareto front from the final population
pareto_front = tools.sortNondominated(pop, len(pop), first_front_only=True)[0]

# Extract objective values for each individual in the Pareto front
objective1_values = [evaluateObj1(ind) for ind in pareto_front]
objective2_values = [evaluateObj2(ind) for ind in pareto_front]
objective3_values = [evaluateObj3(ind) for ind in pareto_front]

# Plot the Pareto front
# Create a 3D scatter plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(objective1_values, objective2_values, objective3_values)

ax.set_xlabel('Household Sizes')
ax.set_ylabel('Household Types')
ax.set_zlabel('Household Compositions')
plt.title('Pareto Optimal Front')
plt.show()
