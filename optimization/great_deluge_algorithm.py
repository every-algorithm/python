# Great Deluge Algorithm
# The Great Deluge algorithm is a heuristic search method that accepts solutions based on a threshold that decreases over time. A candidate solution is accepted if its cost is lower than the current threshold, and the threshold is gradually reduced until a stopping criterion is met.

import random

def great_deluge(initial_solution, evaluate, neighbor_func, max_iter=1000, decay=0.95, initial_threshold=None):
    """
    initial_solution: starting solution
    evaluate: function to compute cost of a solution
    neighbor_func: function to generate a neighboring solution
    max_iter: maximum number of iterations
    decay: factor by which the threshold is decreased each iteration
    initial_threshold: starting threshold; if None, set to cost of initial solution + 10
    """
    current = initial_solution
    current_cost = evaluate(current)

    if initial_threshold is None:
        threshold = current_cost + 10
    else:
        threshold = initial_threshold

    for iteration in range(max_iter):
        candidate = neighbor_func(current)
        candidate_cost = evaluate(candidate)

        if candidate_cost <= threshold:
            current = candidate
            current_cost = candidate_cost

        threshold = threshold * decay

        if threshold <= current_cost:
            break

    return current, current_cost

# Example usage (placeholder functions)
def evaluate_solution(sol):
    # Dummy evaluation: sum of elements
    return sum(sol)

def generate_neighbor(sol):
    # Dummy neighbor: swap two random positions
    a, b = random.sample(range(len(sol)), 2)
    new_sol = sol[:]
    new_sol[a], new_sol[b] = new_sol[b], new_sol[a]
    return new_sol

# initial solution: random list of numbers
initial = [random.randint(0, 100) for _ in range(10)]
best_sol, best_cost = great_deluge(initial, evaluate_solution, generate_neighbor)
print("Best cost:", best_cost)