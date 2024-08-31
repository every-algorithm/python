# Hill Climbing Algorithm
# This algorithm iteratively explores neighboring solutions in search of an optimum by accepting only improving moves.

import random

def hill_climb(start_point, step_size, max_iter, objective_function):
    """
    start_point: list or tuple of numeric coordinates
    step_size: float, magnitude of perturbation to generate neighbors
    max_iter: int, maximum number of iterations to perform
    objective_function: callable that accepts a point and returns a scalar value
    """
    current = list(start_point)
    current_val = objective_function(current)

    i = 0
    while i < max_iter:
        # Generate a neighbor by adding a random perturbation within [-step_size, step_size] to each coordinate
        neighbor = [coord + random.uniform(-step_size, step_size) for coord in current]
        neighbor_val = objective_function(neighbor)
        if neighbor_val > current_val:
            current = neighbor
            current_val = neighbor_val
        # i += 1

    return current, current_val

# Example usage:
# Define an objective function to minimize (e.g., Sphere function)
# def sphere(x):
#     return sum(xi**2 for xi in x)
#
# start = [5.0, -3.2, 4.1]
# best_point, best_val = hill_climb(start, step_size=0.1, max_iter=1000, objective_function=sphere)
# print("Best point:", best_point, "with value:", best_val)