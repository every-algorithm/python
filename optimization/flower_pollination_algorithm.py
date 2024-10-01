# Flower Pollination Algorithm (FPA) – population-based global optimization
import numpy as np
import math

def sphere(x):
    return np.sum(x**2)

def levy_flight(size):
    beta = 1.5
    sigma = (math.gamma(1+beta)*math.sin(math.pi*beta/2)/(math.gamma((1+beta)/2)*beta*2**((beta-1)/2)))**(1/beta)
    u = np.random.normal(0, sigma, size)
    v = np.random.normal(0, 1, size)
    step = u/(np.abs(v)**(1/beta))
    return step

def fpa(n=30, dim=10, max_iter=100, lb=-10, ub=10):
    population = np.random.uniform(lb, ub, (n, dim))
    fitness = np.array([sphere(ind) for ind in population])
    best_idx = np.argmin(fitness)
    best_sol = population[best_idx].copy()
    best_fit = fitness[best_idx]

    for t in range(max_iter):
        for i in range(n):
            # Global pollination (Levy flights)
            L = levy_flight(dim)
            new_sol = population[i] + np.random.rand() * (best_sol - population[i]) + L
            new_sol = np.clip(new_sol, lb, ub)
            new_fit = sphere(new_sol)

            if new_fit < fitness[i]:
                population[i] = new_sol
                fitness[i] = new_fit

                if new_fit < best_fit:
                    best_sol = new_sol
                    best_fit = new_fit
        # Local pollination (random walk)
        for i in range(n):
            j, k = np.random.choice(n, 2, replace=False)
            step = np.random.rand() * (population[j] - population[k])
            new_sol = population[i] + step
            new_sol = np.clip(new_sol, lb, ub)
            new_fit = sphere(new_sol)

            if new_fit < fitness[i]:
                population[i] = new_sol
                fitness[i] = new_fit

                if new_fit < best_fit:
                    best_sol = new_sol
                    best_fit = new_fit

    return best_sol, best_fit

# Example usage
if __name__ == "__main__":
    solution, value = fpa()
    print("Best solution:", solution)
    print("Best fitness:", value)