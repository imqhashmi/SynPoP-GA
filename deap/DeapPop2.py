import random
from Person import Person
from deap import base
from deap import creator
from deap import tools
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
import plotly.graph_objs as go
import pandas as pd
import  plotly as py
import plotly.express as px

ages = {'0-4': 447, '5-7': 182, '8-9': 132, '10-14': 295, '15': 44, '16-17': 106, '18-19': 651, '20-24': 1460, '25-29': 759, '30-34': 617, '35-39': 464, '40-44': 345, '45-49': 300, '50-54': 248, '55-59': 248, '60-64': 232, '65-69': 177, '70-74': 162, '75-79': 127, '80-84': 165, '85+': 142}
sexes = {'M': 3473, 'F': 3830}
CROSS_TABLES = {}
CROSS_TABLES['age_sex'] = {'0-4 M': 227, '5-7 M': 102, '8-9 M': 67, '10-14 M': 141, '15 M': 20, '16-17 M': 60, '18-19 M': 270, '20-24 M': 669, '25-29 M': 365, '30-34 M': 311, '35-39 M': 221, '40-44 M': 196, '45-49 M': 147, '50-54 M': 115, '55-59 M': 118, '60-64 M': 109, '65-69 M': 91, '70-74 M': 77, '75-79 M': 49, '80-84 M': 70, '85+ M': 48, '0-4 F': 220, '5-7 F': 80, '8-9 F': 65, '10-14 F': 154, '15 F': 24, '16-17 F': 46, '18-19 F': 381, '20-24 F': 791, '25-29 F': 394, '30-34 F': 306, '35-39 F': 243, '40-44 F': 149, '45-49 F': 153, '50-54 F': 133, '55-59 F': 130, '60-64 F': 123, '65-69 F': 86, '70-74 F': 85, '75-79 F': 78, '80-84 F': 95, '85+ F': 94}
# ethnicities = {'W1': 4225, 'W2': 73, 'W3': 1, 'W4': 797, 'M1': 76, 'M2': 40, 'M3': 71, 'M4': 78, 'A1': 365, 'A2': 282, 'A3': 112, 'A4': 201, 'A5': 379, 'B1': 322, 'B2': 98, 'B3': 53, 'O1': 75, 'O2': 55}


def getStats(persons, crosstable):
    actual = CROSS_TABLES[crosstable]
    temp = []
    for person in persons:
        temp.append(person[crosstable.split('_')[0]] + " " + person[crosstable.split('_')[1]])
    predicted = Counter(temp)
    return dict([(k, predicted[k]) for k in list(actual.keys())])

# Create fitness function (the closer to the target, the better)
def fitness(individual):
    predicted = getStats(individual, 'age_sex')
    a = np.array(list(CROSS_TABLES['age_sex'].values()))
    p = np.array(list(predicted.values()))
    rmse = np.sqrt(((p - a) ** 2).mean())
    return rmse,

# Create the DEAP tools
creator.create("Fitness", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()

def random_person():
    age = random.choices(list(ages.keys()), list(ages.values()), k=1)[0]
    sex = random.choices(list(sexes.keys()), list(sexes.values()), k=1)[0]
    # age = random.choice(list(ages.keys()))
    # sex = random.choice(list(sexes.keys()))
    return {'age': age, 'sex': sex}

# Define the number of individuals in the population
Total = 7303


# Create individual and population creation methods
toolbox.register("person", random_person)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.person, n=Total)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Genetic operators
toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=25)
toolbox.register("evaluate", fitness)

def main():
    random.seed(64)
    pop = toolbox.population(n=100)
    CXPB, MUTPB = 0.5, 0.5

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))

    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0
    max_values = []
    avg_values = []
    min_values = []
    # Begin the evolution
    while min(fits) > 0 and g < 30:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g, min(fits))

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        min_values.append(min(fits))

    print("-- End of (successful) evolution --")

    plt.plot(min_values, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.show()

    best_ind = tools.selBest(pop, 1)[0]
    predicted = getStats(best_ind, 'age_sex')
    a = np.array(list(CROSS_TABLES['age_sex'].values()))
    p = np.array(list(predicted.values()))
    rmse = np.sqrt(((p - a) ** 2).mean())
    n_actual = [float(i) / max(a) for i in a]
    n_pred = [float(i) / max(p) for i in p]
    print(predicted)
    # n_actual.sort()
    # n_pred.sort()
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x0='data', name='actual', y=n_actual, line_color='#636EFA'))
    fig.add_trace(
        go.Scatter(x0='data', name='pred', y=n_pred, line_color='#EF553B'))
    fig.update_layout(width=1000, title='RMSE=' + str(rmse))
    py.offline.plot(fig, filename="line.html")
    fig.show()

if __name__ == "__main__":
    main()