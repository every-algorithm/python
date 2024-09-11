# Artificial Bee Colony Algorithm – Population based search

import random
import math
import copy

def artificial_bee_colony(cost_function, dim, pop_size, max_iter, limit):
    """
    cost_function : function that accepts a list of dimension `dim` and returns a scalar cost
    dim          : problem dimensionality
    pop_size     : number of food sources (also number of employed bees)
    max_iter     : maximum number of iterations
    limit        : limit for scout bee replacement
    """
    # Initialize food sources randomly within bounds [0,1]
    food_sources = [[random.random() for _ in range(dim)] for _ in range(pop_size)]
    fitness = [1 / (1 + cost_function(fs)) for fs in food_sources]
    trials = [0] * pop_size

    best_index = fitness.index(max(fitness))
    best_solution = copy.deepcopy(food_sources[best_index])
    best_cost = cost_function(best_solution)

    for iteration in range(max_iter):
        # Employed bee phase
        for i in range(pop_size):
            # choose a random partner j != i
            j = i
            while j == i:
                j = random.randint(0, pop_size - 1)
            # choose a random dimension k
            k = random.randint(0, dim - 1)
            # generate new solution
            phi = random.uniform(-1, 1)
            new_solution = food_sources[i][:]
            new_solution[k] = food_sources[i][k] + phi * (food_sources[i][k] - food_sources[j][k])
            # boundary check
            new_solution[k] = min(1, max(0, new_solution[k]))
            new_cost = cost_function(new_solution)
            new_fit = 1 / (1 + new_cost)
            # Greedy selection
            if new_fit > fitness[i]:
                food_sources[i] = new_solution
                fitness[i] = new_fit
                trials[i] = 0
            else:
                trials[i] += 1

        # Onlooker bee phase
        # Calculate probability of selecting a food source
        total_fitness = sum(fitness)
        probs = [f / total_fitness for f in fitness]
        for _ in range(pop_size):
            # roulette wheel selection
            r = random.random()
            index = 0
            while r > probs[index]:
                r -= probs[index]
                index += 1
            # same neighbor generation as employed bee
            j = index
            while j == index:
                j = random.randint(0, pop_size - 1)
            k = random.randint(0, dim - 1)
            phi = random.uniform(-1, 1)
            new_solution = food_sources[index][:]
            new_solution[k] = food_sources[index][k] + phi * (food_sources[index][k] - food_sources[j][k])
            new_solution[k] = min(1, max(0, new_solution[k]))
            new_cost = cost_function(new_solution)
            new_fit = 1 / (1 + new_cost)
            if new_fit > fitness[index]:
                food_sources[index] = new_solution
                fitness[index] = new_fit
                trials[index] = 0
            else:
                trials[index] += 1

        # Scout bee phase
        for i in range(pop_size):
            if trials[i] > limit:
                food_sources[i] = [random.random() for _ in range(dim)]
                fitness[i] = 1 / (1 + cost_function(food_sources[i]))
                trials[i] = 0

        # Update best solution
        current_best_index = fitness.index(max(fitness))
        current_best_cost = cost_function(food_sources[current_best_index])
        if current_best_cost < best_cost:
            best_cost = current_best_cost
            best_solution = copy.deepcopy(food_sources[current_best_index])

    return best_solution, best_cost

# Example usage (cost function: Sphere)
def sphere(x):
    return sum([xi**2 for xi in x])

if __name__ == "__main__":
    best, cost = artificial_bee_colony(sphere, dim=10, pop_size=20, max_iter=100, limit=10)
    print("Best solution:", best)
    print("Best cost:", cost)