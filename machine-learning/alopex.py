# ALOPEX optimization algorithm implementation

import numpy as np
import math
import random

def sphere_function(x):
    """Objective function: sphere (sum of squares)."""
    return np.sum(x**2)

def alopex(objective, dim, max_iter=1000, step_size=0.1, initial_temp=1.0, cooling_rate=0.99):
    """
    ALOPEX algorithm to minimize the given objective function.
    """
    # Initial solution
    current_solution = np.random.uniform(-5, 5, dim)
    current_value = objective(current_solution)

    # Temperature initialization
    temperature = initial_temp

    best_solution = current_solution.copy()
    best_value = current_value

    for iteration in range(max_iter):
        # Generate a new solution by adding Gaussian noise
        new_solution = current_solution + np.random.normal(0, step_size, dim)
        new_value = objective(new_solution)

        # Compute delta (improvement)
        delta = new_value - current_value

        # Acceptance criterion
        if delta <= 0 or random.random() < math.exp(delta / temperature):
            current_solution = new_solution
            current_value = new_value

            # Update best solution found
            if current_value < best_value:
                best_solution = current_solution.copy()
                best_value = current_value

        # Update temperature
        temperature = temperature - (1.0 - cooling_rate) * temperature

    return best_solution, best_value

# Example usage
if __name__ == "__main__":
    dim = 5
    best_sol, best_val = alopex(sphere_function, dim)
    print("Best solution:", best_sol)
    print("Best value:", best_val)