import random
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt

age = {'0-4': 447, '5-7': 182, '8-9': 132, '10-14': 295, '15': 44, '16-17': 106, '18-19': 651, '20-24': 1460, '25-29': 759, '30-34': 617, '35-39': 464, '40-44': 345, '45-49': 300, '50-54': 248, '55-59': 248, '60-64': 232, '65-69': 177, '70-74': 162, '75-79': 127, '80-84': 165, '85+': 142}
sex = {'M': 3473, 'F': 3830}
sex_age = {'0-4 M': 227, '5-7 M': 102, '8-9 M': 67, '10-14 M': 141, '15 M': 20, '16-17 M': 60, '18-19 M': 270, '20-24 M': 669, '25-29 M': 365, '30-34 M': 311, '35-39 M': 221, '40-44 M': 196, '45-49 M': 147, '50-54 M': 115, '55-59 M': 118, '60-64 M': 109, '65-69 M': 91, '70-74 M': 77, '75-79 M': 49, '80-84 M': 70, '85+ M': 48, '0-4 F': 220, '5-7 F': 80, '8-9 F': 65, '10-14 F': 154, '15 F': 24, '16-17 F': 46, '18-19 F': 381, '20-24 F': 791, '25-29 F': 394, '30-34 F': 306, '35-39 F': 243, '40-44 F': 149, '45-49 F': 153, '50-54 F': 133, '55-59 F': 130, '60-64 F': 123, '65-69 F': 86, '70-74 F': 85, '75-79 F': 78, '80-84 F': 95, '85+ F': 94}

# Define the number of individuals in the population
POPULATION_SIZE = 1000

AKEYS = list(age.keys())
AVALUES = list(age.values())
SKEYS = list(sex.keys())
SVALUES = list(sex.values())

ASKEYS = list(sex_age.keys())
ASVALUES = list(sex_age.values())

# Create fitness function (the closer to the target, the better)
def fitness(individual):
    age_error = 0
    sex_error = 0
    age_count = {key: 0 for key in AKEYS}
    sex_count = {key: 0 for key in SKEYS}

    for person in individual:
        age_count[person['age']] += 1
        sex_count[person['sex']] += 1

    for key in AKEYS:
        age_error += abs(age_count[key] - age[key])

    for key in SKEYS:
        sex_error += abs(sex_count[key] - sex[key])

    return ((1 / (1 + age_error)) + (1 / (1 + sex_error)))

# Create the DEAP tools
creator.create("Fitness", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.Fitness)

toolbox = base.Toolbox()

# Functions to create a random individual
def random_age():
    return random.choices(AKEYS, AVALUES, k=1)[0]

def random_sex():
    return random.choices(SKEYS, SVALUES, k=1)[0]

def random_person():
    return {'age': random_age(), 'sex': random_sex()}

# Create individual and population creation methods
toolbox.register("person", random_person)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.person, n=POPULATION_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Genetic operators
toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selBest)
toolbox.register("evaluate", fitness)

# Create the initial population
population = toolbox.population(n=50)
plot = []
# Evolve the population
NGEN = 100
for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
        print(fit)
    population = toolbox.select(offspring, k=len(population))

# Get the best individual from the final population
best_ind = tools.selBest(population, 1)[0]
synthetic_population = best_ind

plt.plot(plot, color='green')
plt.xlabel('Generation')
plt.ylabel('Fitness')
plt.show()


