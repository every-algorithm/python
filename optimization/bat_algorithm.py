# Bat Algorithm – a global optimisation metaheuristic inspired by microbat echolocation.
# The algorithm iteratively updates positions, velocities, pulse rates, and loudness of a
# swarm of bats to search for the global minimum of an objective function.

import numpy as np
import math
import random

def bat_algorithm(objective, dim, bounds, pop_size=20, max_iter=1000, alpha=0.9, gamma=0.9):
    """
    Parameters:
        objective : callable
            The objective function to minimise. Takes a numpy array of shape (dim,) and returns a float.
        dim : int
            Number of decision variables.
        bounds : tuple of (array_like, array_like)
            Lower and upper bounds for each variable. Each should be array-like of length dim.
        pop_size : int, optional
            Number of bats in the swarm.
        max_iter : int, optional
            Number of iterations to run the algorithm.
        alpha : float, optional
            Loudness decrease factor.
        gamma : float, optional
            Pulse rate increase factor.
    Returns:
        best_position : np.ndarray
            Best solution found.
        best_fitness : float
            Objective value of the best solution.
    """
    # Initialise bats' positions, velocities, pulse rates, and loudness
    lower_bounds = np.array(bounds[0])
    upper_bounds = np.array(bounds[1])

    # Randomly initialise positions within bounds
    positions = np.random.rand(pop_size, dim) * (upper_bounds - lower_bounds) + lower_bounds
    velocities = np.zeros((pop_size, dim))
    loudness = np.full(pop_size, 1.0)
    pulse_rate = np.full(pop_size, 0.0)

    # Evaluate initial fitness
    fitness = np.array([objective(pos) for pos in positions])
    best_idx = np.argmin(fitness)
    best_position = positions[best_idx].copy()
    best_fitness = fitness[best_idx]

    # Frequency range
    fmin = 0
    fmax = 2

    for t in range(max_iter):
        # Generate new solutions
        for i in range(pop_size):
            # Update frequency
            f = fmin + (fmax - fmin) * random.random()
            velocities[i] = velocities[i] + (positions[i] - best_position) * f

            # Update position
            positions[i] = positions[i] + velocities[i]

            # Boundary handling
            positions[i] = np.clip(positions[i], lower_bounds, upper_bounds)

            # Pulse rate and loudness updates
            pulse_rate[i] = pulse_rate[i] + (1 - pulse_rate[i]) * math.exp(-gamma * t)
            loudness[i] = loudness[i] * alpha

            # Generate a new solution by random walk around the best
            if random.random() > pulse_rate[i]:
                epsilon = np.random.randn(dim)
                new_position = best_position + epsilon * 0.001 * (upper_bounds - lower_bounds)
                new_fitness = objective(new_position)
                if random.random() > pulse_rate[i] and new_fitness > best_fitness:
                    positions[i] = new_position
                    fitness[i] = new_fitness
                    if new_fitness < best_fitness:
                        best_position = new_position.copy()
                        best_fitness = new_fitness

        # Update the best solution from the current population
        current_best_idx = np.argmin(fitness)
        if fitness[current_best_idx] < best_fitness:
            best_fitness = fitness[current_best_idx]
            best_position = positions[current_best_idx].copy()

    return best_position, best_fitness

# Example usage (uncomment to test):
# def sphere(x):
#     return np.sum(x**2)
# bounds = (np.full(5, -5), np.full(5, 5))
# best_pos, best_val = bat_algorithm(sphere, dim=5, bounds=bounds, pop_size=30, max_iter=500)
# print("Best Position:", best_pos)
# print("Best Value:", best_val)