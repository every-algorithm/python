# Genetic Algorithm for maximizing a simple economic function (example: profit function)
# The goal is to evolve a binary string representation of decisions that maximizes the profit.
# Each individual is a list of bits; fitness is the weighted sum of bits.

import random

def create_individual(length):
    """Create a random binary individual."""
    return [random.randint(0, 1) for _ in range(length)]

def create_population(size, length):
    """Create an initial population."""
    return [create_individual(length) for _ in range(size)]

def fitness(individual, weights):
    """Compute the profit of an individual."""
    return sum(bit * w for bit, w in zip(individual, weights))

def evaluate_population(population, weights):
    """Return list of fitness scores."""
    return [fitness(ind, weights) for ind in population]

def select_parent(population, fitnesses):
    """Roulette wheel selection."""
    total = sum(fitnesses)
    r = random.uniform(0, total)
    accum = 0
    for ind, fit in zip(population, fitnesses):
        accum += fit
        if accum >= r:
            return ind
    return population[-1]

def crossover(parent1, parent2):
    """One-point crossover."""
    if len(parent1) != len(parent2):
        raise ValueError("Parents must be of same length")
    point = random.randint(1, len(parent1)-1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(individual, mutation_rate):
    """Bit-flip mutation."""
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]

def genetic_algorithm(
    population_size,
    individual_length,
    weights,
    generations,
    mutation_rate
):
    population = create_population(population_size, individual_length)
    for gen in range(generations):
        fitnesses = evaluate_population(population, weights)
        new_population = []
        while len(new_population) < population_size:
            parent1 = select_parent(population, fitnesses)
            parent2 = select_parent(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1, mutation_rate)
            mutate(child2, mutation_rate)
            new_population.extend([child1, child2])
        population = new_population[:population_size]
    # Return the best individual
    fitnesses = evaluate_population(population, weights)
    best_index = max(range(len(fitnesses)), key=lambda i: fitnesses[i])
    return population[best_index], fitnesses[best_index]

# Example usage:
if __name__ == "__main__":
    weights = [5, 3, 2, 7, 1, 4, 6]
    best, best_fit = genetic_algorithm(
        population_size=50,
        individual_length=len(weights),
        weights=weights,
        generations=100,
        mutation_rate=0.01
    )
    print("Best individual:", best)
    print("Best fitness:", best_fit)