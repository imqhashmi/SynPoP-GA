import random
import numpy as np
import pandas as pd
from deap import base, creator, tools, algorithms

census_data = pd.read_csv("uk_census_data.csv")

def decode_individual_to_synthetic_population(individual):
    # Define the lengths of each attribute in the binary string
    age_length = 7   # 2^7 = 128 (enough to represent ages 0-100)
    gender_length = 1
    income_length = 17  # 2^17 ≈ 131,000 (enough to represent incomes 0-100,000)
    employment_status_length = 1

    # Calculate the number of people in the synthetic population
    person_length = age_length + gender_length + income_length + employment_status_length
    num_people = len(individual) // person_length

    # Initialize lists for each attribute
    ages = []
    genders = []
    incomes = []
    employment_statuses = []

    # Iterate through the individual, decoding each attribute
    for i in range(num_people):
        start = i * person_length

        age_bin = individual[start:start+age_length]
        age = int(''.join(map(str, age_bin)), 2)
        ages.append(age)

        gender = individual[start+age_length]
        genders.append(gender)

        income_bin = individual[start+age_length+gender_length:start+age_length+gender_length+income_length]
        income = int(''.join(map(str, income_bin)), 2)
        incomes.append(income)

        employment_status = individual[start+age_length+gender_length+income_length]
        employment_statuses.append(employment_status)

    # Create a DataFrame for the synthetic population
    synthetic_population = pd.DataFrame({
        'Age': ages,
        'Gender': genders,
        'Income': incomes,
        'EmploymentStatus': employment_statuses
    })

    return synthetic_population

def calculate_fitness(synthetic_population, census_data):
    # Normalize the census data and synthetic population
    census_data_normalized = census_data.copy()
    synthetic_population_normalized = synthetic_population.copy()

    census_data_normalized['Income'] = census_data['Income'] / 100000
    synthetic_population_normalized['Income'] = synthetic_population['Income'] / 100000

    # Calculate the distributions for each attribute
    age_dist_census = census_data_normalized['Age'].value_counts(normalize=True)
    gender_dist_census = census_data_normalized['Gender'].value_counts(normalize=True)
    income_dist_census = census_data_normalized['Income'].value_counts(normalize=True, bins=10)
    employment_status_dist_census = census_data_normalized['EmploymentStatus'].value_counts(normalize=True)

    age_dist_synthetic = synthetic_population_normalized['Age'].value_counts(normalize=True)
    gender_dist_synthetic = synthetic_population_normalized['Gender'].value_counts(normalize=True)
    income_dist_synthetic = synthetic_population_normalized['Income'].value_counts(normalize=True, bins=10)
    employment_status_dist_synthetic = synthetic_population_normalized['EmploymentStatus'].value_counts(normalize=True)

    # Calculate the absolute difference between distributions
    age_diff = np.abs(age_dist_census.subtract(age_dist_synthetic, fill_value=0)).sum()
    gender_diff = np.abs(gender_dist_census.subtract(gender_dist_synthetic, fill_value=0)).sum()
    income_diff = np.abs(income_dist_census.subtract(income_dist_synthetic, fill_value=0)).sum()
    employment_status_diff = np.abs(employment_status_dist_census.subtract(employment_status_dist_synthetic, fill_value=0)).sum()

    # Calculate the fitness score (lower is better)
    fitness_score = age_diff + gender_diff + income_diff + employment_status_diff

    return fitness_score


def evaluate_population(individual):
    synthetic_population = decode_individual_to_synthetic_population(individual)
    fitness_score = calculate_fitness(synthetic_population, census_data)
    return fitness_score,

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attribute", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attribute, n=100)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", evaluate_population)

population = toolbox.population(n=300)
ngen = 50
cxpb = 0.5
mutpb = 0.2

pop, logbook = algorithms.eaSimple(population, toolbox, cxpb=cxpb, mutpb=mutpb, ngen=ngen, verbose=True)
best_individual = tools.selBest(population, k=1)[0]
best_synthetic_population = decode_individual_to_synthetic_population(best_individual)
best_synthetic_population.to_csv('best.csv')
