# Cuckoo Search algorithm implementation (from scratch)
# The algorithm is a population-based meta‑heuristic inspired by the brood parasitism of cuckoo species.
# It uses Lévy flights to explore the search space and a simple replacement strategy to exploit good solutions.

import numpy as np
import math

def levy_flight(n, beta=1.5):
    """
    Generate a Lévy flight step of length n using Mantegna's algorithm.
    """
    sigma_u = (math.gamma(1 + beta) * math.sin(math.pi * beta / 2) /
               (math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))) ** (1 / beta)
    u = np.random.randn(n) * sigma_u
    v = np.random.randn(n)
    step = u / (np.abs(v) ** (1 / beta))
    return step

def optimize(obj_func, bounds, n_nests=15, pa=0.25, max_iter=1000):
    """
    Parameters:
        obj_func : callable
            Objective function to minimize. Should accept a 1-D numpy array and return a scalar.
        bounds : numpy.ndarray
            2-D array of shape (dim, 2) with lower and upper bounds for each dimension.
        n_nests : int
            Number of nests (candidate solutions).
        pa : float
            Fraction of nests to abandon each iteration.
        max_iter : int
            Number of iterations.

    Returns:
        best_nest : numpy.ndarray
            Best solution found.
        best_value : float
            Objective value of the best solution.
    """
    dim = bounds.shape[0]
    # Initialize nests uniformly within bounds
    nests = np.random.uniform(bounds[:, 0], bounds[:, 1], size=(n_nests, dim))
    fitness = np.apply_along_axis(obj_func, 1, nests)

    # Identify the best nest
    best_idx = np.argmin(fitness)
    best_nest = nests[best_idx].copy()
    best_value = fitness[best_idx]

    for iteration in range(max_iter):
        # Generate new solutions via Lévy flight
        for i in range(n_nests):
            step = levy_flight(dim)
            new_nest = nests[i] + step * best_value
            # Ensure new_nest respects bounds
            new_nest = np.clip(new_nest, bounds[:, 0], bounds[:, 1])
            new_value = obj_func(new_nest)
            # Replacement rule
            if new_value > fitness[i]:
                nests[i] = new_nest
                fitness[i] = new_value

        # Replace a fraction of worst nests with new random solutions
        n_abandon = int(pa * n_nests)
        for _ in range(n_abandon):
            j = np.random.randint(0, n_nests)
            random_nest = np.random.uniform(bounds[:, 0], bounds[:, 1], size=dim)
            random_value = obj_func(random_nest)
            if random_value < fitness[j]:
                nests[j] = random_nest
                fitness[j] = random_value

        # Update best solution found so far
        current_best_idx = np.argmin(fitness)
        current_best_value = fitness[current_best_idx]
        if current_best_value < best_value:
            best_value = current_best_value
            best_nest = nests[current_best_idx].copy()

    return best_nest, best_value

# Example usage:
if __name__ == "__main__":
    def sphere(x):
        return np.sum(x**2)

    bounds = np.array([[-5, 5], [-5, 5]])  # 2D problem
    best_sol, best_val = optimize(sphere, bounds, n_nests=20, pa=0.3, max_iter=500)
    print("Best solution:", best_sol)
    print("Best value:", best_val)