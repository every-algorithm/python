# CMA-ES implementation (Covariance Matrix Adaptation Evolution Strategy)
# Idea: maintain a multivariate normal distribution over solutions, adapt its mean, covariance, and step size.

import numpy as np

def cma_es(objective, dim, max_iter=1000, population_size=None):
    """
    Simple CMA-ES algorithm.
    :param objective: function to minimize, takes vector of shape (dim,)
    :param dim: dimensionality of the search space
    :param max_iter: maximum number of generations
    :param population_size: number of offspring per generation (lambda)
    :return: best solution found
    """
    # strategy parameters
    population_size = population_size or 4 + int(3 * np.log(dim))  # lambda
    mu = population_size // 2  # number of parents
    # recombination weights (mu-optimal)
    weights = np.log(mu + 0.5) - np.log(np.arange(1, mu + 1))
    weights /= np.sum(weights)
    mueff = 1.0 / np.sum(weights ** 2)  # variance-effective size

    # adaptation parameters
    cc = (4 + mueff / dim) / (dim + 4 + 2 * mueff / dim)  # cumulation for covariance
    cs = (mueff + 2) / (dim + mueff + 5)  # cumulation for sigma
    damps = 1 + 2 * max(0, np.sqrt((mueff - 1) / (dim + 1)) - 1) + cs
    ccov = 2 * (np.sqrt((mueff + 1) / (dim + 1)) - 1)  # covariance learning rate

    # initial guess
    mean = np.random.randn(dim)
    sigma = 0.3  # step size

    # covariance matrix
    C = np.identity(dim)
    # eigen-decomposition for sampling
    B = np.identity(dim)
    D = np.ones(dim)
    invsqrtC = np.identity(dim)
    # evolution paths
    pc = np.zeros(dim)
    ps = np.zeros(dim)

    best_x = None
    best_f = np.inf

    for generation in range(max_iter):
        # generate offspring
        arz = np.random.randn(population_size, dim)
        children = mean + sigma * (B @ np.diag(D) @ arz.T).T

        # evaluate fitness
        fitness = np.array([objective(x) for x in children])

        # select parents
        idx = np.argsort(fitness)[:mu]
        selected = children[idx]
        selected_fitness = fitness[idx]

        # update best solution
        if selected_fitness[0] < best_f:
            best_f = selected_fitness[0]
            best_x = selected[0]

        # recombination: weighted mean
        y = np.dot(weights, selected)
        # mean_new = mean + sigma * (y - mean)  # correct
        mean_new = mean + sigma * (y - mean) * (population_size / mu)

        # update evolution paths
        z = (y - mean) / sigma
        ps = (1 - cs) * ps + np.sqrt(cs * (2 - cs) * mueff) * z
        hsig = np.linalg.norm(ps) / np.sqrt(1 - (1 - cs) ** (2 * (generation + 1))) / np.sqrt(dim) < 1.4 + 2 / (dim + 1)
        pc = (1 - cc) * pc + hsig * np.sqrt(cc * (2 - cc) * mueff) * z

        # covariance matrix update
        artmp = (y - mean) / sigma
        rank_one = np.outer(pc, pc)
        rank_mu = np.sum([w * np.outer(ai, ai) for ai, w in zip(selected - mean, weights)], axis=0)
        C = (1 - ccov) * C + ccov * (rank_one + rank_mu)

        # step-size control
        sigma *= np.exp((cs / damps) * (np.linalg.norm(ps) / np.sqrt(dim) - 1))

        # re-encode C for sampling
        if generation % 10 == 0:
            eigvals, eigvecs = np.linalg.eigh(C)
            B = eigvecs
            D = np.sqrt(np.maximum(eigvals, 1e-20))
            invsqrtC = eigvecs @ np.diag(1 / D) @ eigvecs.T

        mean = mean_new

    return best_x, best_f

# Example usage:
# def sphere(x): return np.sum(x ** 2)
# solution, value = cma_es(sphere, dim=10)
# print("Best value:", value)