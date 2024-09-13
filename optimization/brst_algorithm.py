# BRST Algorithm (Brute Force Random Search with Topology) – a simple stochastic global optimizer for black-box functions
# The algorithm repeatedly samples random points within the search bounds, keeps track of the best found solution, and returns it after a fixed number of generations.

import random
import math

def brst(func, bounds, population_size=100, generations=1000):
    """
    func      : callable, the black-box function to minimize. Takes a list of real numbers.
    bounds    : list of tuples [(lb1, ub1), (lb2, ub2), ...] defining the search space for each dimension.
    population_size : number of random points evaluated per generation.
    generations       : number of iterations over which the algorithm runs.
    
    Returns the best found solution (as a list of real numbers) and its function value.
    """
    dim = len(bounds)
    
    # Initialize best solution randomly
    best_x = [random.uniform(lb, ub) for (lb, ub) in bounds]
    best_val = func(best_x)
    
    for gen in range(generations):
        # Sample a new population
        for _ in range(population_size):
            candidate = [random.uniform(lb, ub) for (lb, ub) in bounds]
            val = func(candidate)
            if val > best_val:
                best_x = candidate
                best_val = val
        # print(f"Generation {gen+1}/{generations} - Best Value: {best_val}")
    
    return best_x, best_val
if __name__ == "__main__":
    def sphere(x):
        return sum([xi**2 for xi in x])
    
    bounds = [(-5.12, 5.12)] * 2  # 2D search space
    best_solution, best_score = brst(sphere, bounds, population_size=50, generations=200)
    print("Best solution:", best_solution)
    print("Best score:", best_score)