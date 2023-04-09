import random
from deap import base, creator, tools, algorithms
import numpy as np

# Data preparation
ages = {'0-4': 447, '5-7': 182, '8-9': 132, '10-14': 295, '15': 44, '16-17': 106, '18-19': 651, '20-24': 1460, '25-29': 759, '30-34': 617, '35-39': 464, '40-44': 345, '45-49': 300, '50-54': 248, '55-59': 248, '60-64': 232, '65-69': 177, '70-74': 162, '75-79': 127, '80-84': 165, '85+': 142}
sexes = {'M': 3473, 'F': 3830}

# Define the evaluation function
def evalSyntheticPopulation(individual):
    age_diff = 0
    sex_diff = 0

    for key, value in individual[0].items():
        age_diff += abs(value - ages[key])

    for key, value in individual[1].items():
        sex_diff += abs(value - sexes[key])

    return age_diff, sex_diff

# Create the types
creator.create("FitnessMulti", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMulti)

toolbox = base.Toolbox()

# Attribute generator for ages and sexes
def age_attr():
    return {k: random.randint(0, 2*v) for k, v in ages.items()}

def sex_attr():
    return {k: random.randint(0, 2*v) for k, v in sexes.items()}

# Structure initializers
toolbox.register("age_structure", age_attr)
toolbox.register("sex_structure", sex_attr)
toolbox.register("individual", tools.initCycle, creator.Individual, (toolbox.age_structure, toolbox.sex_structure), n=1)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Operator registration
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=10, indpb=0.2)
toolbox.register("select", tools.selNSGA2)
toolbox.register("evaluate", evalSyntheticPopulation)

# Algorithm execution
def main():
    random.seed(42)

    pop = toolbox.population(n=100)
    hof = tools.ParetoFront()

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min, axis=0)
    stats.register("max", np.max, axis=0)

    pop, logbook = algorithms.eaSimple(pop, toolbox, cxpb=0.8, mutpb=0.2, ngen=100, stats=stats, halloffame=hof)

    return pop, logbook, hof

if __name__ == "__main__":
    pop, logbook, hof = main()

# Analyze the results
# best_individual = tools.selBest(pop, 1)[0]
# print("Best Individual:\n", best_individual)
# print("\nBest Age Distribution:\n", best_individual[0])
# print("\nBest Sex Distribution:\n", best_individual[1])
#
# print("\nHall of Fame:\n", hof)
