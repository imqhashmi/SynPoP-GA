import numpy as np
from scipy.integrate import trapz
import matplotlib.pyplot as plt

def shift_left(lst, n):
    """Shifts the elements of the list to the left by n positions."""
    return lst[n:] + lst[:n]

# Actual and predicted vectors
# actual = [45, 20, 13, 28, 4, 12, 54, 134, 73, 62, 44, 39, 29, 23, 24, 22, 18, 15, 10, 14, 10, 44, 16, 13, 31, 5, 9, 76, 158, 79, 61, 49, 30, 31, 27, 26, 25, 17, 17, 16, 19, 19]
# predicted = [46, 19, 14, 23, 4, 9, 56, 127, 71, 62, 38, 31, 28, 26, 27, 24, 19, 20, 10, 15, 13, 47, 18, 18, 32, 6, 10, 73, 145, 76, 60, 48, 37, 35, 30, 28, 22, 16, 20, 18, 21, 19]

actual = [19, 0, 0, 3, 1, 1, 2, 3, 3, 3, 2, 0, 5, 4, 0, 0, 0, 1, 8, 0, 0, 1, 0, 2, 1, 0, 2, 1, 1, 0, 2, 2, 0, 1, 1, 0, 7, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 14, 0, 0, 1, 0, 0, 0, 1, 1, 3, 2, 0, 3, 1, 0, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 34, 0, 0, 6, 0, 0, 1, 0, 1, 1, 1, 3, 1, 2, 1, 0, 1, 0, 81, 2, 0, 18, 2, 2, 1, 1, 4, 3, 1, 9, 3, 6, 1, 0, 2, 1, 31, 1, 0, 17, 0, 0, 0, 0, 4, 6, 1, 4, 2, 2, 0, 1, 2, 2, 27, 0, 0, 14, 1, 0, 0, 0, 4, 3, 1, 2, 5, 3, 0, 0, 0, 1, 19, 0, 0, 6, 0, 0, 0, 0, 4, 2, 0, 1, 6, 2, 0, 0, 1, 1, 21, 0, 0, 4, 0, 0, 0, 0, 4, 2, 1, 1, 2, 3, 2, 0, 0, 0, 18, 0, 0, 2, 0, 0, 0, 0, 1, 3, 1, 0, 1, 1, 1, 1, 1, 0, 15, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 20, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 15, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 14, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 20, 0, 0, 2, 1, 0, 2, 1, 4, 4, 1, 1, 5, 2, 0, 0, 2, 0, 7, 0, 0, 0, 1, 0, 1, 0, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 4, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 2, 0, 1, 0, 0, 15, 0, 0, 2, 1, 0, 0, 1, 1, 3, 2, 0, 2, 2, 1, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 5, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 55, 0, 0, 8, 1, 0, 1, 0, 2, 2, 0, 2, 2, 3, 1, 0, 1, 1, 91, 2, 0, 21, 3, 0, 1, 2, 7, 2, 1, 7, 8, 8, 2, 0, 1, 1, 32, 1, 0, 16, 2, 0, 1, 1, 6, 3, 2, 4, 5, 3, 2, 1, 1, 1, 26, 1, 0, 12, 0, 1, 0, 0, 5, 3, 1, 2, 5, 3, 1, 0, 0, 1, 18, 0, 0, 8, 0, 0, 0, 1, 4, 2, 2, 1, 7, 4, 1, 0, 1, 1, 16, 0, 0, 4, 1, 1, 0, 1, 2, 1, 0, 1, 3, 2, 0, 0, 0, 0, 18, 0, 0, 3, 0, 1, 0, 0, 2, 1, 1, 0, 2, 1, 1, 0, 1, 0, 18, 0, 0, 2, 0, 0, 0, 1, 1, 1, 0, 0, 0, 2, 0, 0, 0, 1, 21, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 19, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 14, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 14, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 18, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
predicted = [0, 18, 0, 0, 0, 1, 1, 0, 0, 4, 3, 1, 5, 0, 1, 1, 0, 0, 0, 12, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 16, 1, 0, 0, 1, 0, 0, 0, 3, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 28, 0, 0, 0, 0, 0, 1, 0, 6, 5, 2, 1, 0, 2, 0, 0, 0, 0, 71, 1, 0, 0, 4, 0, 4, 0, 5, 3, 4, 3, 0, 3, 1, 0, 1, 0, 33, 0, 0, 0, 0, 0, 1, 0, 6, 4, 4, 2, 0, 1, 1, 0, 1, 0, 24, 1, 0, 0, 0, 0, 0, 0, 5, 3, 1, 3, 0, 4, 0, 0, 1, 0, 23, 0, 0, 0, 0, 0, 0, 0, 1, 1, 3, 2, 0, 3, 0, 0, 1, 0, 21, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 1, 0, 3, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 2, 0, 1, 0, 0, 0, 0, 14, 0, 0, 0, 1, 0, 0, 0, 3, 2, 0, 2, 0, 1, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 11, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 7, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 17, 0, 0, 0, 1, 0, 0, 0, 3, 2, 1, 3, 0, 2, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 3, 1, 1, 0, 0, 0, 0, 0, 1, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 17, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 35, 2, 0, 0, 0, 1, 1, 0, 2, 1, 1, 3, 0, 3, 1, 0, 1, 0, 78, 5, 0, 0, 1, 2, 2, 0, 7, 4, 9, 7, 0, 4, 3, 0, 1, 0, 38, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 7, 0, 2, 1, 0, 1, 0, 25, 0, 0, 0, 0, 0, 0, 0, 3, 2, 0, 2, 0, 4, 0, 0, 1, 0, 24, 0, 0, 0, 0, 0, 1, 0, 3, 3, 1, 2, 0, 1, 2, 0, 1, 0, 12, 0, 0, 0, 1, 0, 1, 0, 2, 0, 1, 1, 0, 1, 1, 0, 1, 0, 14, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 2, 0, 0, 2, 0, 19, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 1, 0, 0, 1, 0, 11, 0, 0, 0, 0, 0, 0, 0, 2, 1, 1, 0, 0, 1, 0, 0, 1, 0, 12, 1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 0, 0, 1, 1, 0, 0, 0, 10, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 3, 0, 0, 0, 0, 8, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 1, 0, 1, 0, 0, 1, 0, 8, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
predicted = shift_left(predicted, 1)
# Create x-axis values
x = np.arange(len(actual))

# Plot the actual and predicted curves
plt.plot(x, actual, label='Actual')
plt.plot(x, predicted, label='Predicted')

# Calculate the difference and plot it as a shaded area
diff = np.abs(np.array(actual) - np.array(predicted))
# plt.fill_between(x, diff, color='gray', alpha=1, label='Difference')
plt.plot(x, diff, color='gray', alpha=1, label='Difference')

# Compute and print the area of difference
area = trapz(diff, x)
print('The area of difference between the curves is:', area)

# Add legend and show the plot
plt.legend()
plt.show()
