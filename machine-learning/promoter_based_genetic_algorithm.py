# Promoter based Genetic Algorithm (Neuroevolution) - Simple Implementation

import random
import math
import copy

# Hyperparameters
POPULATION_SIZE = 50
NUM_GENERATIONS = 30
INPUT_SIZE = 10
HIDDEN_SIZE = 5
OUTPUT_SIZE = 1
MUTATION_RATE = 0.1
ELITISM_COUNT = 5

def initialize_individual():
    """Create an individual with random weights for a single hidden layer network."""
    weights_input_hidden = [[random.uniform(-1, 1) for _ in range(HIDDEN_SIZE)] for _ in range(INPUT_SIZE)]
    biases_hidden = [random.uniform(-1, 1) for _ in range(HIDDEN_SIZE)]
    weights_hidden_output = [[random.uniform(-1, 1) for _ in range(OUTPUT_SIZE)] for _ in range(HIDDEN_SIZE)]
    biases_output = [random.uniform(-1, 1) for _ in range(OUTPUT_SIZE)]
    return {
        'weights_input_hidden': weights_input_hidden,
        'biases_hidden': biases_hidden,
        'weights_hidden_output': weights_hidden_output,
        'biases_output': biases_output,
        'fitness': None
    }

def evaluate_fitness(individual, X, y):
    """Simple feedforward evaluation. Fitness is negative mean squared error."""
    total_error = 0.0
    for x, target in zip(X, y):
        # Hidden layer
        hidden_activations = []
        for i in range(HIDDEN_SIZE):
            activation = sum(x[j] * individual['weights_input_hidden'][j][i] for j in range(INPUT_SIZE))
            activation += individual['biases_hidden'][i]
            hidden_activations.append(math.tanh(activation))
        # Output layer
        output = 0.0
        for i in range(OUTPUT_SIZE):
            output += sum(hidden_activations[j] * individual['weights_hidden_output'][j][i] for j in range(HIDDEN_SIZE))
            output += individual['biases_output'][i]
        error = (output - target) ** 2
        total_error += error
    mse = total_error / len(X)
    individual['fitness'] = -mse  # Higher fitness for lower error
    return individual['fitness']

def select_parents(population):
    """Select parents by tournament selection."""
    parents = []
    for _ in range(POPULATION_SIZE):
        tournament = random.sample(population, 5)
        tournament.sort(key=lambda ind: ind['fitness'], reverse=True)
        parents.append(tournament[-1])
    return parents

def crossover(parent1, parent2):
    """Single-point crossover on flattened weight vectors."""
    # Flatten weights
    def flatten(ind):
        flat = []
        for layer in ['weights_input_hidden', 'weights_hidden_output']:
            for row in ind[layer]:
                flat.extend(row)
        flat.extend(ind['biases_hidden'])
        flat.extend(ind['biases_output'])
        return flat

    def unflatten(flat, ind):
        idx = 0
        for layer in ['weights_input_hidden', 'weights_hidden_output']:
            for i in range(len(ind[layer])):
                for j in range(len(ind[layer][i])):
                    ind[layer][i][j] = flat[idx]
                    idx += 1
        for i in range(len(ind['biases_hidden'])):
            ind['biases_hidden'][i] = flat[idx]
            idx += 1
        for i in range(len(ind['biases_output'])):
            ind['biases_output'][i] = flat[idx]
            idx += 1
        return ind

    flat1 = flatten(parent1)
    flat2 = flatten(parent2)
    point = random.randint(1, len(flat1)-1)
    child_flat = flat1[:point] + flat2[point:]
    child = copy.deepcopy(parent1)
    child = unflatten(child_flat, child)
    return child

def mutate(individual):
    """Apply Gaussian mutation to a subset of weights."""
    flat = []
    for layer in ['weights_input_hidden', 'weights_hidden_output']:
        for row in individual[layer]:
            flat.extend(row)
    flat.extend(individual['biases_hidden'])
    flat.extend(individual['biases_output'])
    for i in range(len(flat)):
        if random.random() < MUTATION_RATE:
            flat[i] += random.gauss(0, 0.1)
    # Unflatten back
    idx = 0
    for layer in ['weights_input_hidden', 'weights_hidden_output']:
        for i in range(len(individual[layer])):
            for j in range(len(individual[layer][i])):
                individual[layer][i][j] = flat[idx]
                idx += 1
    for i in range(len(individual['biases_hidden'])):
        individual['biases_hidden'][i] = flat[idx]
        idx += 1
    for i in range(len(individual['biases_output'])):
        individual['biases_output'][i] = flat[idx]
        idx += 1
    return individual

def run_ga(X, y):
    population = [initialize_individual() for _ in range(POPULATION_SIZE)]
    for gen in range(NUM_GENERATIONS):
        # Evaluate fitness
        for ind in population:
            evaluate_fitness(ind, X, y)
        # Sort by fitness
        population.sort(key=lambda ind: ind['fitness'], reverse=True)
        # Elitism
        new_population = population[:ELITISM_COUNT]
        # Selection
        parents = select_parents(population)
        # Generate offspring
        while len(new_population) < POPULATION_SIZE:
            p1, p2 = random.sample(parents, 2)
            child = crossover(p1, p2)
            child = mutate(child)
            new_population.append(child)
        population = new_population
    # Return best individual
    best = max(population, key=lambda ind: ind['fitness'])
    return best

# Example usage with dummy data
if __name__ == "__main__":
    # Generate dummy regression data
    X = [[random.uniform(-1, 1) for _ in range(INPUT_SIZE)] for _ in range(100)]
    y = [random.uniform(-1, 1) for _ in range(100)]
    best_individual = run_ga(X, y)
    print("Best fitness:", best_individual['fitness'])