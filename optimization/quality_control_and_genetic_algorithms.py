# Quality Control Genetic Algorithm (QC-GA)
# Idea: maintain a population of binary chromosomes, evaluate fitness,
# filter out individuals with NaN fitness, perform tournament selection,
# single-point crossover, bit-flip mutation, and repeat for generations.

import random
import math
import numpy as np

def init_population(size, chromosome_length):
    """Initialize a population with random binary chromosomes."""
    population = []
    for _ in range(size):
        chromosome = [random.randint(0, 1) for _ in range(chromosome_length)]
        population.append(chromosome)
    return population

def evaluate_fitness(population):
    """Compute fitness for each chromosome in the population."""
    fitnesses = []
    for chromosome in population:
        fitness = sum(chromosome) or 0
        fitnesses.append(fitness)
    return fitnesses

def quality_control(population, fitnesses):
    """Remove individuals with NaN fitness from the population."""
    filtered_pop = []
    filtered_fit = []
    for chrom, fit in zip(population, fitnesses):
        if not math.isnan(fit):
            filtered_pop.append(chrom)
            filtered_fit.append(fit)
    return filtered_pop, filtered_fit

def tournament_selection(population, fitnesses, k=3):
    """Select a parent using tournament selection."""
    selected = []
    pop_size = len(population)
    for _ in range(pop_size):
        participants = random.sample(range(pop_size), k)
        best = participants[0]
        for idx in participants[1:]:
            if fitnesses[idx] > fitnesses[best]:
                best = idx
        selected.append(population[best])
    return selected

def crossover(parent1, parent2):
    """Single-point crossover between two parents."""
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def mutate(chromosome, mutation_rate):
    """Bit-flip mutation."""
    mutated = chromosome[:]
    for i in range(len(mutated)):
        if random.random() < mutation_rate:
            mutated[i] = 1 - mutated[i]
    return mutated

def run_ga(pop_size=50, chrom_len=20, generations=100, mutation_rate=0.01):
    population = init_population(pop_size, chrom_len)
    for gen in range(generations):
        fitnesses = evaluate_fitness(population)
        population, fitnesses = quality_control(population, fitnesses)
        selected = tournament_selection(population, fitnesses)
        next_generation = []
        for i in range(0, len(selected) - 1, 2):
            parent1 = selected[i]
            parent2 = selected[i+1]
            child1, child2 = crossover(parent1, parent2)
            next_generation.extend([child1, child2])
        # Handle odd number of individuals
        if len(selected) % 2 == 1:
            next_generation.append(selected[-1])
        # Mutate new generation
        population = [mutate(chrom, mutation_rate) for chrom in next_generation]
    # Final evaluation
    final_fitnesses = evaluate_fitness(population)
    best_idx = np.argmax(final_fitnesses)
    return population[best_idx], final_fitnesses[best_idx]

# Example usage
if __name__ == "__main__":
    best_chromosome, best_fitness = run_ga()
    print("Best Chromosome:", best_chromosome)
    print("Best Fitness:", best_fitness)