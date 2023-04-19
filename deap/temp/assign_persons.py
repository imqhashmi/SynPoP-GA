Households = [{'size': '5', 'type': 'family', 'composition': '2A_3C'},{'size': '1', 'type': 'person', 'composition': '1A_0C'},{'size': '2', 'type': 'family', 'composition': '1A_1C'}]
Persons = [{'id': 7299, 'age': '55-59', 'sex': 'M', 'ethnicity': 'W1', 'religion': 'C', 'status': 'Married', 'qualification': 'no'},{'id': 7300, 'age': '18-19', 'sex': 'F', 'ethnicity': 'W4', 'religion': 'C', 'status': 'Single', 'qualification': 'level2'},{'id': 7301, 'age': '50-54', 'sex': 'M', 'ethnicity': 'W4', 'religion': 'C', 'status': 'Single', 'qualification': 'no'},{'id': 7302, 'age': '25-29', 'sex': 'F', 'ethnicity': 'W1', 'religion': 'NS', 'status': 'Single', 'qualification': 'level4+'}]

def is_adult(person):
    age = int(person['age'].split('-')[0])
    return age >= 18

def assign_persons_to_households(households, persons):
    assigned_households = [h.copy() for h in households]
    for h in assigned_households:
        h['persons'] = []

    persons_copy = persons.copy()

    for person in persons_copy:
        adult_count = sum([1 for p in persons_copy if is_adult(p)])
        child_count = len(persons_copy) - adult_count

        for household in assigned_households:
            required_adults, required_children = [int(x) for x in household['composition'].split('_')]
            assigned_adults = sum([1 for p in household['persons'] if is_adult(p)])
            assigned_children = len(household['persons']) - assigned_adults

            if is_adult(person) and assigned_adults < required_adults:
                household['persons'].append(person)
                persons_copy.remove(person)
                break
            elif not is_adult(person) and assigned_children < required_children:
                household['persons'].append(person)
                persons_copy.remove(person)
                break

    return assigned_households

assigned_households = assign_persons_to_households(Households, Persons)
print(assigned_households)
