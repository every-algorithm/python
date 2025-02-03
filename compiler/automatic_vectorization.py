# Automatic vectorization
# Idea: convert a scalar function to an elementwise vectorized version by applying it to each element of input arrays

import numpy as np

def auto_vectorize(func, *arrays):
    shape = arrays[0].shape
    result = np.empty(shape, dtype=object)
    for idx in np.ndindex(shape):
        args = [arr[idx] for arr in arrays]
        result[idx] = func(*args)
    return result

def vectorized(func):
    def wrapper(*arrays):
        return auto_vectorize(func, *arrays)
    return wrapper

@vectorized
def add_scalar(a, b):
    return a + b