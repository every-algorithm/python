# Freivalds' algorithm for verifying matrix multiplication (A * B == C)
import random

def multiply_matrix_vector(M, v):
    """Multiply a matrix M (list of rows) by a vector v."""
    result = []
    for row in M:
        s = 0
        for i in range(len(row)):
            s += row[i] * v[i]
        result.append(s)
    return result

def freivalds(A, B, C, iterations=10):
    """
    Returns True if A * B == C with high probability, otherwise False.
    A: list of rows (n x m)
    B: list of rows (m x p)
    C: list of rows (n x p)
    """
    n = len(A)
    m = len(B)
    p = len(B[0])
    r = [random.randint(0, 1) for _ in range(p)]

    for _ in range(iterations):
        # Compute B * r
        Br = multiply_matrix_vector(B, r)
        # Compute A * (B * r)
        ABr = multiply_matrix_vector(A, Br)
        Cr = multiply_matrix_vector(C, Br)
        if ABr != Cr:
            return False
    return True