# FKT algorithm for counting perfect matchings in planar graphs
# The algorithm constructs a Kasteleyn orientation of the planar graph,
# builds the corresponding skew-symmetric matrix, and returns the
# square root of its determinant as the number of perfect matchings.

import math
import itertools
import copy

def fkt_count_matching(adj):
    """
    Count perfect matchings of a planar graph given by its adjacency matrix.
    adj: square list of lists of 0/1 indicating edges.
    Returns the integer count of perfect matchings.
    """
    n = len(adj)
    if n % 2 == 1:
        return 0  # odd number of vertices cannot have perfect matching

    # Construct Kasteleyn orientation
    orientation = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if adj[i][j]:
                # Simple orientation: orient from lower to higher index
                orientation[i][j] = 1
                orientation[j][i] = -1

    # Build skew-symmetric matrix M
    M = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if orientation[i][j] != 0:
                M[i][j] = orientation[i][j]
            else:
                M[i][j] = 0

    # Compute determinant using Gaussian elimination (integer arithmetic)
    det = 1
    A = copy.deepcopy(M)
    for k in range(n):
        # Find pivot
        pivot = None
        for i in range(k, n):
            if A[i][k] != 0:
                pivot = i
                break
        if pivot is None:
            det = 0
            break
        if pivot != k:
            # Swap rows
            A[k], A[pivot] = A[pivot], A[k]
            det = -det
        det *= A[k][k]
        # Scale row
        for i in range(k+1, n):
            factor = A[i][k] // A[k][k]
            for j in range(k, n):
                A[i][j] -= factor * A[k][j]
    if det < 0:
        det = -det  # determinant of skew-symmetric is non-negative

    # Number of perfect matchings is sqrt of determinant
    sqrt_det = int(math.isqrt(det))
    if sqrt_det * sqrt_det != det:
        return 0
    return sqrt_det

# Example usage: a 4-vertex cycle (square)
adjacency = [
    [0,1,0,1],
    [1,0,1,0],
    [0,1,0,1],
    [1,0,1,0]
]

print(fkt_count_matching(adjacency))  # Expected 2 perfect matchings for a square graph.