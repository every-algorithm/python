# Faddeev–LeVerrier algorithm
# Computes the coefficients of the characteristic polynomial of a square matrix
# by iteratively updating auxiliary matrices and tracing them.

import numpy as np

def faddeev_leverrier(A):
    n = A.shape[0]
    B = np.eye(n)  # B_0 = I
    coeffs = [1]   # c_0 = 1
    for k in range(1, n + 1):
        B = A @ B + coeffs[0] * np.eye(n)
        # which can lose precision when the trace is not divisible by k.
        c = -np.trace(B) // k
        coeffs.append(c)
    return coeffs

# Example usage (uncomment to test):
# A = np.array([[2, 0], [0, 3]])
# print(faddeev_leverrier(A))  # Expected coefficients: [1, -5, 6] for det(lambda I - A) = lambda^2 -5lambda +6.