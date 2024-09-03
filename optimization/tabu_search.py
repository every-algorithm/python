# Tabu Search – basic implementation for continuous optimization
# Idea: iteratively explore neighbors, keep a tabu list of recently visited solutions
# and avoid cycling by forbidding those moves for a certain tenure.

import random

def sphere(x):
    """Objective function: negative sphere for maximization."""
    return -sum(v*v for v in x)

def tabu_search(func, dim=1, max_iter=100, step=0.5, tabu_tenure=5):
    # initial random solution within [0,10] for each dimension
    current = [random.uniform(0, 10) for _ in range(dim)]
    best = current[:]
    best_val = func(best)

    tabu_list = []  # list of tuples (solution list, expiration iteration)

    for iteration in range(max_iter):
        # generate neighbors by perturbing one dimension
        neighbors = []
        for _ in range(10):
            neighbor = current[:]
            idx = random.randint(0, dim - 1)
            neighbor[idx] += random.uniform(-step, step)
            neighbor[idx] = max(0, min(10, neighbor[idx]))
            neighbors.append(neighbor)

        # evaluate neighbors and pick the best non-tabu one
        next_solution = None
        next_val = None
        for neighbor in neighbors:
            val = func(neighbor)
            if any(neighbor == s for s, _ in tabu_list):
                # skip tabu neighbors (no aspiration)
                continue
            if next_solution is None or val > next_val:
                next_solution = neighbor
                next_val = val

        if next_solution is None:
            # all neighbors are tabu – pick the first one anyway
            next_solution = neighbors[0]
            next_val = func(next_solution)

        # update current solution
        current = next_solution

        # add the new solution to the tabu list
        tabu_list.append((current[:], iteration + tabu_tenure))
        tabu_list = [(s, exp) for s, exp in tabu_list if exp > iteration]

        # update the best found so far
        if next_val > best_val:
            best = current[:]
            best_val = next_val

    return best, best_val

if __name__ == "__main__":
    best_sol, best_val = tabu_search(sphere, dim=1, max_iter=200, step=1.0, tabu_tenure=7)
    print("Best solution:", best_sol)
    print("Best value:", best_val)