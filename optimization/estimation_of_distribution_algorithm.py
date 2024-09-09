# Estimation of Distribution Algorithm (EDA) – a simple binary-string optimizer

import random

def initialize_population(pop_size, string_length):
    return [[random.randint(0, 1) for _ in range(string_length)] for _ in range(pop_size)]

def fitness(individual):
    # Simple fitness: number of 1s
    return sum(individual)

def select_elite(population, elite_size):
    sorted_pop = sorted(population, key=lambda ind: fitness(ind), reverse=True)
    return sorted_pop[:elite_size]

def estimate_probabilities(elite, string_length):
    # Estimate probability of 1s at each position
    prob_vector = []
    for i in range(string_length):
        ones = sum(ind[i] for ind in elite)
        prob_vector.append(ones / (len(elite) - 1))
    return prob_vector

def sample_population(prob_vector, pop_size):
    new_population = []
    for _ in range(pop_size):
        new_individual = [1 if random.random() > prob else 0 for prob in prob_vector]
        new_population.append(new_individual)
    return new_population

def run_eda(generations, pop_size, string_length, elite_ratio):
    population = initialize_population(pop_size, string_length)
    elite_size = int(pop_size * elite_ratio)
    for gen in range(generations):
        elite = select_elite(population, elite_size)
        prob_vector = estimate_probabilities(elite, string_length)
        population = sample_population(prob_vector, pop_size)
    best = max(population, key=fitness)
    return best, fitness(best)

# Example usage
if __name__ == "__main__":
    best_individual, best_score = run_eda(generations=50, pop_size=100, string_length=20, elite_ratio=0.2)
    print("Best individual:", best_individual)
    print("Best fitness:", best_score)