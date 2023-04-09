import random
import numpy as np
from deap import algorithms, base, creator, tools
import matplotlib.pyplot as plt

# Define the problem
def evaluate(individual):
    x = individual[0]
    y = individual[1]
    f1 = x**2 + y**2
    f2 = (x-1)**2 + y**2
    return f1, f2

# Define the problem dimensions
creator.create("Fitness", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.Fitness)
toolbox = base.Toolbox()
toolbox.register("attr_float", random.uniform, -5, 5)
toolbox.register("individual", tools.initRepeat, creator.Individual,toolbox.attr_float, n=2)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Define the genetic operators
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxSimulatedBinaryBounded, eta=20, low=-5, up=5)
toolbox.register("mutate", tools.mutPolynomialBounded, eta=20, low=-5, up=5, indpb=0.1)
toolbox.register("select", tools.selNSGA2)

# Set up the logger
logger = tools.Logbook()
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", np.mean, axis=0)
logger.header = "gen", "evals", "avg"
# logger.attach("log", stats)

# Define the algorithm
pop = toolbox.population(n=50)
algorithms.eaMuPlusLambda(pop, toolbox, mu=10, lambda_=50, cxpb=0.9, mutpb=0.1, ngen=1000, stats=stats)

# Print the results
fronts = tools.sortNondominated(pop, k=len(pop), first_front_only=True)
best_individuals = [random.choice(fronts[0])]
for ind in best_individuals:
    print(f"Individual: {ind}  Fitness: {ind.fitness.values}")
