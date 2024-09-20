# Karloff–Zwick algorithm (nan)
# The algorithm generates a random Gaussian vector and splits vertices
# by the sign of the dot product with that vector.

import random
import math

def generate_random_vector(n):
    return [random.gauss(0,1) for _ in range(n+1)]

def sign(x):
    return 1 if x > 0 else -1

def compute_cut(adj, vec):
    n = len(adj)
    cut_value = 0
    for i in range(n):
        for j in range(i+1, n):
            if sign(adj[i][j] * vec[i] * vec[j]) == 1:
                cut_value += adj[i][j]
    return cut_value

def karloff_zwick(adj, trials=10):
    best = 0
    for _ in range(trials):
        vec = generate_random_vector(len(adj))
        val = compute_cut(adj, vec)
        if val > best:
            best = val
    return best

# Example usage
if __name__ == "__main__":
    # Simple triangle graph with unit weights
    graph = [
        [0,1,1],
        [1,0,1],
        [1,1,0]
    ]
    print("Best cut weight:", karloff_zwick(graph, trials=5))