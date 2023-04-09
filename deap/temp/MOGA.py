import random
from deap import base, creator, tools, algorithms

# Step 1: Define the problem
num_products = 10
max_cost = 100
max_weight = 50

# Step 2: Define the genotype and phenotype
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

def create_individual():
    return [random.randint(0, 1) for _ in range(num_products)]

def genotype_to_phenotype(individual):
    products = [i+1 for i, val in enumerate(individual) if val == 1]
    return products

# Step 3: Define the fitness function
costs = [10, 20, 30, 15, 25, 35, 10, 20, 30, 15]
weights = [5, 10, 15, 8, 12, 18, 5, 10, 15, 8]

def evaluate(individual):
    cost = sum(costs[i]*val for i, val in enumerate(individual))
    weight = sum(weights[i]*val for i, val in enumerate(individual))
    return cost, weight


# Step 4: Define the genetic operators
toolbox = base.Toolbox()
toolbox.register("individual", tools.initIterate, creator.Individual, create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selNSGA2)

# Step 5: Define the toolbox
toolbox.register("evaluate", evaluate)

# Step 6: Run the optimization
pop_size = 10000
num_generations = 500
population = toolbox.population(n=pop_size)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("min", lambda x: round(min(x, default=float('inf'))[0], 2))

logbook = tools.Logbook()
logbook.header = "gen", "evals", "min"

# Evaluate the entire population
fitnesses = toolbox.map(toolbox.evaluate, population)
for ind, fit in zip(population, fitnesses):
    ind.fitness.values = fit

# Run the optimization
for gen in range(num_generations):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
    fitnesses = toolbox.map(toolbox.evaluate, offspring)
    for ind, fit in zip(offspring, fitnesses):
        ind.fitness.values = fit
    population = toolbox.select(offspring + population, k=pop_size)
    record = stats.compile(population)
    logbook.record(gen=gen, evals=len(offspring), **record)
    print(logbook.stream)

# Step 7: Analyze the results
pareto_front = tools.ParetoFront()
pareto_front.update(population)
print("Number of non-dominated solutions: ", len(pareto_front))
print("Best non-dominated solutions:")
for ind in pareto_front:
    print("Cost:", ind.fitness.values[0], "Weight:", ind.fitness.values[1], "Products:", genotype_to_phenotype(ind))
