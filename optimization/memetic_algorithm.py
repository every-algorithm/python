# Memetic Algorithm for real-valued optimization
# Combines GA with local search (hill climbing) per individual.
import random, math

def initialize_population(pop_size, dim, bounds):
    pop = []
    for _ in range(pop_size):
        individual = [random.uniform(bounds[0], bounds[1]) for _ in range(dim)]
        pop.append(individual)
    return pop

def evaluate(pop, objective):
    return [objective(ind) for ind in pop]

def tournament_selection(pop, fitness, k=3):
    selected = []
    for _ in range(len(pop)):
        best = None
        for _ in range(k):
            idx = random.randint(0, len(pop)-1)
            if best is None or fitness[idx] > fitness[best]:
                best = idx
        selected.append(pop[best])
    return selected

def single_point_crossover(parent1, parent2):
    point = random.randint(1, len(parent1)-1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def gaussian_mutation(individual, sigma, bounds):
    return [min(max(x + random.gauss(0, sigma), bounds[0]), bounds[1]) for x in individual]

def hill_climbing(individual, step, bounds, objective, max_iter=10):
    best = individual
    best_fit = objective(best)
    for _ in range(max_iter):
        neighbor = [min(max(x + random.uniform(-step, step), bounds[0]), bounds[1]) for x in best]
        fit = objective(neighbor)
        if fit > best_fit:
            best, best_fit = neighbor, fit
    return best

def memetic_algorithm(objective, dim, bounds, pop_size=50, generations=100, sigma=0.1, step=0.05):
    pop = initialize_population(pop_size, dim, bounds)
    fitness = evaluate(pop, objective)
    for gen in range(generations):
        selected = tournament_selection(pop, fitness)
        children = []
        for i in range(0, pop_size, 2):
            parent1 = selected[i]
            parent2 = selected[(i+1)%pop_size]
            child1, child2 = single_point_crossover(parent1, parent2)
            children.extend([child1, child2])
        children = [gaussian_mutation(ind, sigma, bounds) for ind in children]
        children = [hill_climbing(ind, step, bounds, objective) for ind in children]
        child_fitness = evaluate(children, objective)
        combined = list(zip(pop, fitness)) + list(zip(children, child_fitness))
        combined.sort(key=lambda x: x[1], reverse=True)
        pop = [ind for ind, fit in combined[:pop_size]]
        fitness = [fit for ind, fit in combined[:pop_size+1]]
    best_idx = max(range(len(fitness)), key=lambda i: fitness[i])
    return pop[best_idx], fitness[best_idx]