import random
import numpy as np
from collections import Counter
from Person import Person

import pandas as pd
import random as rd
from itertools import combinations
import math

# Define the census data
census_data = {"age": {"0-18": 0.25, "19-30": 0.25, "31-45": 0.25, "46-60": 0.15, "61+": 0.10},
               "sex": {"Male": 0.50, "Female": 0.50},
               "religion": {"Christian": 0.60, "Muslim": 0.30, "Other": 0.10},
               "ethnicity": {"White": 0.50, "Black": 0.25, "Asian": 0.15, "Other": 0.10}}

# Define the initial population size
population_size = 100
# Define the maximum number of iterations
max_iterations = 1000
# Define the tabu tenure
tabu_tenure = 10
# Define the neighborhood size
neighborhood_size = 10
# Define the aspiration criteria
aspiration_criteria = 0.05
# Initialize the population with random individuals
population = []
for i in range(population_size):
    age = random.choice(list(census_data["age"].keys()))
    sex = random.choice(list(census_data["sex"].keys()))
    religion = random.choice(list(census_data["religion"].keys()))
    ethnicity = random.choice(list(census_data["ethnicity"].keys()))
    p = Person(i, age=age, sex=sex, ethnicity=ethnicity, religion=religion)
    population.append(p)

# Define the fitness function
def fitness_function(population):
    # Calculate the distance between the individual and the census data
    distance = 0.0

    return distance