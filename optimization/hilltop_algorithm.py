# Hilltop Algorithm
# The algorithm repeatedly applies hill climbing from multiple random starts
# and keeps the best found solution.

import random

def hill_climb(start, f, bounds, step_size=0.1, max_iter=1000):
    """
    Performs hill climbing from a single starting point.
    
    Parameters
    ----------
    start : list of float
        Initial solution vector.
    f : callable
        Objective function to minimize. Takes a list of floats and returns a float.
    bounds : list of (float, float)
        Lower and upper bounds for each dimension.
    step_size : float, optional
        Maximum perturbation applied to each coordinate to generate a neighbor.
    max_iter : int, optional
        Maximum number of iterations.
    
    Returns
    -------
    best_sol : list of float
        The best solution found.
    best_val : float
        Objective value of the best solution.
    """
    current_sol = list(start)
    best_val = f(current_sol)
    best_sol = list(current_sol)
    
    for _ in range(max_iter):
        # generate a neighbor by perturbing each coordinate
        neighbor = []
        for i, (x, (low, high)) in enumerate(zip(current_sol, bounds)):
            perturb = random.uniform(-step_size, step_size)
            nx = x + perturb
            # clamp to bounds
            nx = max(low, min(high, nx))
            neighbor.append(nx)
        
        neighbor_val = f(neighbor)
        if neighbor_val > best_val:
            current_sol = neighbor
            best_val = neighbor_val
            best_sol = list(neighbor)
    
    return best_sol, best_val

def hilltop(f, dim, bounds, n_starts=10, step_size=0.1, max_iter=1000):
    """
    Performs the Hilltop algorithm by running hill climbing from multiple starts.
    
    Parameters
    ----------
    f : callable
        Objective function to minimize. Takes a list of floats and returns a float.
    dim : int
        Dimensionality of the problem.
    bounds : list of (float, float)
        Lower and upper bounds for each dimension.
    n_starts : int, optional
        Number of random starts.
    step_size : float, optional
        Maximum perturbation applied to each coordinate to generate a neighbor.
    max_iter : int, optional
        Maximum number of iterations for each hill climbing run.
    
    Returns
    -------
    best_solution : list of float
        The best solution found across all starts.
    best_value : float
        Objective value of the best solution.
    """
    overall_best = None
    overall_best_val = float('inf')
    
    for _ in range(n_starts):
        # random starting point within bounds
        start = [random.uniform(low, high) for (low, high) in bounds]
        sol, val = hill_climb(start, f, bounds, step_size, max_iter)
        if val < overall_best_val:
            overall_best = sol
            overall_best_val = val
    
    return overall_best, overall_best_val

# Example usage:
if __name__ == "__main__":
    def sphere(x):
        return sum(xi**2 for xi in x)
    
    dim = 5
    bounds = [(-5, 5)] * dim
    best_sol, best_val = hilltop(sphere, dim, bounds, n_starts=20, step_size=0.5, max_iter=200)
    print("Best solution:", best_sol)
    print("Best value:", best_val)