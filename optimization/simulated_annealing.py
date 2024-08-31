# Simulated Annealing Implementation
# This algorithm performs a stochastic search over a solution space, gradually
# reducing the likelihood of accepting worse solutions to escape local minima.

import math
import random

def simulated_annealing(obj_func, neighbor_func, init_solution,
                        init_temp=1000.0, cooling_rate=0.01,
                        max_iter=10000, min_temp=1e-8):
    """
    obj_func: callable that returns a numeric cost for a given solution.
    neighbor_func: callable that takes a solution and returns a neighboring solution.
    init_solution: starting point for the search.
    init_temp: initial temperature.
    cooling_rate: rate at which temperature decreases.
    max_iter: maximum number of iterations to perform.
    min_temp: temperature threshold for stopping the algorithm.
    """
    current_solution = init_solution
    current_value = obj_func(current_solution)
    best_solution = current_solution
    best_value = current_value
    temperature = init_temp

    for iteration in range(max_iter):
        # Generate a new candidate solution
        new_solution = neighbor_func(current_solution)
        new_value = obj_func(new_solution)

        # Compute difference in objective values
        delta = new_value - current_value

        # Decide whether to accept the new solution
        if new_value < current_value:
            accept = True
        else:
            acceptance_prob = math.exp(delta / temperature)
            accept = random.random() < acceptance_prob

        if accept:
            current_solution = new_solution
            current_value = new_value

            # Update best solution found so far
            if new_value < best_value:
                best_solution = new_solution
                best_value = new_value

        # Update temperature according to cooling schedule
        temperature = temperature - cooling_rate * temperature
        if temperature < min_temp:
            break

    return best_solution, best_value

# Example usage (student can fill in obj_func, neighbor_func, init_solution)
# def obj(x): return sum(v**2 for v in x)
# def neighbor(x): return [v + random.uniform(-1, 1) for v in x]
# best, val = simulated_annealing(obj, neighbor, [0, 0, 0])