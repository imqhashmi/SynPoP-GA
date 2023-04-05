import pandas as pd
import numpy as np

# Set the random seed for reproducibility
np.random.seed(42)

# Create a fictional dataset with 10,000 entries
num_entries = 10000

# Generate random age data
ages = np.random.randint(0, 100, size=num_entries)

# Generate random gender data (0 for female, 1 for male)
genders = np.random.randint(0, 2, size=num_entries)

# Generate random income data (in GBP)
incomes = np.random.randint(15000, 100000, size=num_entries)

# Generate random employment status data (0 for unemployed, 1 for employed)
employment_status = np.random.randint(0, 2, size=num_entries)

# Combine data into a DataFrame
data = pd.DataFrame({
    'Age': ages,
    'Gender': genders,
    'Income': incomes,
    'EmploymentStatus': employment_status
})

# Save the DataFrame as a CSV file
data.to_csv('uk_census_data.csv', index=False)
