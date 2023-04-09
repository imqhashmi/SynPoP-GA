from collections import Counter, OrderedDict

# Example counter
example_counter = Counter({'a': 3, 'c': 2, 'b': 5})

# Given list of keys
sort_keys = ['b', 'a', 'c']

# Sort the counter using the given list of keys
sorted_counter = OrderedDict((key, example_counter[key]) for key in sort_keys)

# Print the sorted counter
print(sorted_counter)
