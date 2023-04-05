import random

import pandas as pd
import numpy as np

# Load census data
census_data = pd.read_csv('census_data.csv')
census_data['count'] = census_data.apply(lambda x: random.randrange(0,400), axis=1)

# Define categories
age_categories = ['0-4', '5-9', '10-14', '15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49', '50-54',
                  '55-59', '60-64', '65-69', '70-74', '75-79', '80+']
gender_categories = ['male', 'female']
education_categories = ['early years', 'primary', 'secondary', 'Further Education', 'Higher Education']

# Calculate margins
age_margins = census_data.groupby('age')['count'].sum()
gender_margins = census_data.groupby('gender')['count'].sum()
education_margins = census_data.groupby('education')['count'].sum()

# # Create initial synthetic population
# n = census_data['count'].sum()
# initial_synthetic_population = pd.DataFrame({'age': np.random.choice(age_categories, size=n),
#                                              'gender': np.random.choice(gender_categories, size=n),
#                                              'education': np.random.choice(education_categories, size=n)})
#
# #Iterate proportional fitting
# for i in range(10):  # repeat 10 times
#     # Calculate proportions
#     age_props = initial_synthetic_population.groupby('age').size() / n
#     gender_props = initial_synthetic_population.groupby('gender').size() / n
#     education_props = initial_synthetic_population.groupby('education').size() / n
#
#     # Adjust proportions using IPF
#     age_props *= age_margins / age_props.sum()
#     gender_props *= gender_margins / gender_props.sum()
#     education_props *= education_margins / education_props.sum()
#
#     # Generate new synthetic population
#     new_synthetic_population = pd.DataFrame({'age': np.random.choice(age_categories, size=n),
#                                              'gender': np.random.choice(gender_categories, size=n),
#                                              'education': np.random.choice(education_categories, size=n)})
#
#     # Replace initial synthetic population with new one
#     initial_synthetic_population = new_synthetic_population
#
# # Validate synthetic population
# synthetic_population = initial_synthetic_population
# print('Age distribution:')
# print(synthetic_population['age'].value_counts(normalize=True))
# print('Gender distribution:')
# print(synthetic_population['gender'].value_counts(normalize=True))
# print('Education distribution:')
# print(synthetic_population['education'].value_counts(normalize=True))
