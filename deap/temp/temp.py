from collections import Counter

data = [{'age': '25-29', 'sex': 'F', 'ethnicity': 'A1'}, {'age': '40-44', 'sex': 'F', 'ethnicity': 'W1'}, {'age': '25-29', 'sex': 'F', 'ethnicity': 'W4'}, {'age': '40-44', 'sex': 'M', 'ethnicity': 'W4'}, {'age': '55-59', 'sex': 'M', 'ethnicity': 'B2'}, {'age': '60-64', 'sex': 'M', 'ethnicity': 'W1'}, {'age': '8-9', 'sex': 'M', 'ethnicity': 'W1'}, {'age': '5-7', 'sex': 'F', 'ethnicity': 'W1'}, {'age': '0-4', 'sex': 'F', 'ethnicity': 'B2'}, {'age': '20-24', 'sex': 'F', 'ethnicity': 'B1'}, {'age': '80-84', 'sex': 'M', 'ethnicity': 'W1'}, {'age': '0-4', 'sex': 'M', 'ethnicity': 'W1'}, {'age': '45-49', 'sex': 'F', 'ethnicity': 'W1'}, {'age': '40-44', 'sex': 'M', 'ethnicity': 'B1'}, {'age': '18-19', 'sex': 'M', 'ethnicity': 'W1'}, {'age': '70-74', 'sex': 'F', 'ethnicity': 'W1'}, {'age': '10-14', 'sex': 'F', 'ethnicity': 'A5'}, {'age': '20-24', 'sex': 'M', 'ethnicity': 'W1'}, {'age': '18-19', 'sex': 'M', 'ethnicity': 'W4'}, {'age': '10-14', 'sex': 'F', 'ethnicity': 'W1'}, {'age': '20-24', 'sex': 'M', 'ethnicity': 'A5'}, {'age': '40-44', 'sex': 'M', 'ethnicity': 'W1'}, {'age': '18-19', 'sex': 'M', 'ethnicity': 'W1'}, {'age': '50-54', 'sex': 'M', 'ethnicity': 'A5'}, {'age': '20-24', 'sex': 'F', 'ethnicity': 'W1'}, {'age': '25-29', 'sex': 'F', 'ethnicity': 'W1'}, {'age': '35-39', 'sex': 'F', 'ethnicity': 'W1'}, {'age': '15', 'sex': 'M', 'ethnicity': 'M1'}, {'age': '65-69', 'sex': 'F', 'ethnicity': 'W1'}, {'age': '35-39', 'sex': 'M', 'ethnicity': 'A5'}, {'age': '20-24', 'sex': 'F', 'ethnicity': 'W1'}, {'age': '35-39', 'sex': 'M', 'ethnicity': 'W1'}, {'age': '20-24', 'sex': 'M', 'ethnicity': 'W1'}, {'age': '18-19', 'sex': 'M', 'ethnicity': 'W1'}, {'age': '10-14', 'sex': 'F', 'ethnicity': 'A5'}, {'age': '20-24', 'sex': 'F', 'ethnicity': 'W1'}, {'age': '70-74', 'sex': 'M', 'ethnicity': 'W1'}, {'age': '75-79', 'sex': 'F', 'ethnicity': 'W1'}, {'age': '16-17', 'sex': 'M', 'ethnicity': 'W4'}, {'age': '55-59', 'sex': 'M', 'ethnicity': 'W1'}]


# Initialize counters
age_counter = Counter()
sex_counter = Counter()
ethnicity_counter = Counter()
age_sex_counter = Counter()

# Iterate through the list and update the counters
for entry in data:
    age_sex_counter[entry['sex'] + " " + entry['age']]+=1
    age_counter[entry['age']] += 1
    sex_counter[entry['sex']] += 1
    ethnicity_counter[entry['ethnicity']] += 1

# Print the totals
print("Agesex totals:", age_sex_counter)
print("Age totals:", age_counter)
print("Sex totals:", sex_counter)
print("Ethnicity totals:", ethnicity_counter)