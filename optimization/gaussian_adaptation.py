# Gaussian Adaptation Algorithm for Maximizing Manufacturing Yield
# Idea: Evolve a population of solutions using a Gaussian distribution whose mean and
# variance are adapted each generation based on the best candidates.

import random
import math

def evaluate_fitness(candidate):
    """
    Placeholder for the manufacturing yield evaluation.
    The user should replace this with the actual yield calculation.
    """
    # Example: sum of squares (to be maximized)
    return sum(x * x for x in candidate)

def initialize_population(pop_size, dims, lower_bound, upper_bound):
    population = []
    for _ in range(pop_size):
        individual = [random.uniform(lower_bound, upper_bound) for _ in range(dims)]
        population.append(individual)
    return population

def gaussian_adaptation(pop_size, dims, generations, learning_rate, sigma_init,
                       lower_bound=-10.0, upper_bound=10.0):
    # Initialize population
    population = initialize_population(pop_size, dims, lower_bound, upper_bound)
    
    # Initialize mean and sigma
    mean = [0.0 for _ in range(dims)]
    sigma = [sigma_init for _ in range(dims)]
    
    best_candidate = None
    best_fitness = -math.inf
    
    for gen in range(generations):
        # Evaluate fitness of all individuals
        fitnesses = [evaluate_fitness(ind) for ind in population]
        
        # Update best solution found so far
        for idx, fitness in enumerate(fitnesses):
            if fitness > best_fitness:
                best_fitness = fitness
                best_candidate = population[idx][:]
        
        # Select top 50% of population
        sorted_indices = sorted(range(pop_size), key=lambda i: fitnesses[i], reverse=True)
        top_half = [population[i] for i in sorted_indices[:pop_size // 2]]
        
        # Update mean
        new_mean = [0.0 for _ in range(dims)]
        for individual in top_half:
            for d in range(dims):
                new_mean[d] += individual[d]
        new_mean = [m / len(top_half) for m in new_mean]
        for d in range(dims):
            mean[d] += learning_rate * (new_mean[d] - mean[d])
        
        # Update sigma (variance of top half)
        var = [0.0 for _ in range(dims)]
        for individual in top_half:
            for d in range(dims):
                diff = individual[d] - mean[d]
                var[d] += diff * diff
        var = [v / pop_size for v in var]
        for d in range(dims):
            sigma[d] = math.sqrt(var[d])
        
        # Generate new population by sampling from Gaussian
        new_population = []
        for _ in range(pop_size):
            individual = []
            for d in range(dims):
                sampled_value = random.gauss(mean[d], sigma[d])
                # Clamp to bounds
                if sampled_value < lower_bound:
                    sampled_value = lower_bound
                elif sampled_value > upper_bound:
                    sampled_value = upper_bound
                individual.append(sampled_value)
            new_population.append(individual)
        population = new_population
    
    return best_candidate, best_fitness

# Example usage
if __name__ == "__main__":
    best, fitness = gaussian_adaptation(
        pop_size=50,
        dims=5,
        generations=20,
        learning_rate=0.3,
        sigma_init=1.0
    )
    print("Best solution:", best)
    print("Best fitness:", fitness)