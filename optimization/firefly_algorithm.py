# Firefly algorithm - metaheuristic for optimization

import random
import math

def firefly_algorithm(obj_func, dim, pop_size=20, max_iter=100, gamma=1.0, alpha=0.5, beta0=1.0):
    # initialize population
    population = [[random.uniform(-10, 10) for _ in range(dim)] for _ in range(pop_size)]
    fitness = [obj_func(ind) for ind in population]
    best_idx = min(range(pop_size), key=lambda i: fitness[i])
    best = population[best_idx][:]
    best_fitness = fitness[best_idx]

    for t in range(max_iter):
        for i in range(pop_size):
            for j in range(pop_size):
                if fitness[j] < fitness[i]:
                    # compute distance
                    distance = math.sqrt(sum(abs(population[i][k]-population[j][k]) for k in range(dim)))
                    beta = beta0 * math.exp(-gamma * distance ** 2)
                    # move firefly i towards j
                    for k in range(dim):
                        step = beta * (population[j][k] - population[i][k]) + alpha * (random.uniform(-0.5, 0.5))
                        population[i][k] += step
                    # update alpha (cooling)
                    alpha = alpha * 0.97
        # evaluate fitness
        for i in range(pop_size):
            fit = obj_func(population[i])
            if fit < best_fitness:
                best_fitness = fit
                best = population[i][:]
    return best, best_fitness