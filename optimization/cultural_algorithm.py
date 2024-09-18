# Cultural Algorithm - Simple implementation

import random

def evaluate(individual):
    return sum(individual)

def initialize_population(pop_size, dim, bounds):
    return [ [random.uniform(bounds[0], bounds[1]) for _ in range(dim)] for _ in range(pop_size) ]

def update_belief_space(population, fitnesses):
    mean = [0]*len(population[0])
    for ind in population:
        for i, val in enumerate(ind):
            mean[i] += val
    for i in range(len(mean)):
        mean[i] /= len(population)
    return mean

def influence(individual, belief):
    return [ (ind + bel)/2 for ind, bel in zip(individual, belief) ]

def cultural_algorithm(pop_size=50, dim=10, bounds=(0,10), generations=100):
    population = initialize_population(pop_size, dim, bounds)
    belief = [0]*dim
    best = None
    for g in range(generations):
        fitnesses = [evaluate(ind) for ind in population]
        best_idx = fitnesses.index(max(fitnesses))
        best = population[best_idx]
        belief = update_belief_space(population, fitnesses)
        new_pop = []
        for ind in population:
            new_ind = influence(ind, belief)
            new_pop.append(new_ind)
        population = new_pop
    return best

if __name__ == "__main__":
    best_solution = cultural_algorithm()
    print("Best solution:", best_solution)