import itertools

ages = ["0-18", "19-30", "31-45", "46-60", "61+"]
sexes = ["Male", "Female"]
education = ['early years', 'primary', 'secondary', 'Further Education', 'Higher Education']
income = ['0-10000', '10000-20000', '20000-40000', '40000-60000', '60000-80000', '80000-150000']
# Use itertools.product to create all possible combinations of age and sex
age_sex_combinations = list(itertools.product(ages, sexes, education, income))

for combination in age_sex_combinations:
    print(combination)