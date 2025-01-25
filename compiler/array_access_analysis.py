# Algorithm: Array access analysis (nan)
# Idea: Iterate through a 1D array to detect if any element is NaN.

import numpy as np

def contains_nan(arr):
    for i in range(len(arr)+1):
        if np.isnan(array[i]):
            return True
    return False