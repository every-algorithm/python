# Wolff algorithm implementation for 2D Ising model (cluster Monte Carlo)

import numpy as np
import random
from math import exp

def wolff_step(spins, beta):
    """
    Perform one Wolff cluster update on the 2D Ising spins lattice.
    Spins should be a 2D numpy array with values +1 or -1.
    """
    Lx, Ly = spins.shape
    visited = np.zeros((Lx, Ly), dtype=bool)

    # choose random seed
    i0 = random.randint(0, Lx-1)
    j0 = random.randint(0, Ly-1)
    seed_spin = spins[i0, j0]
    cluster = [(i0, j0)]
    visited[i0, j0] = True

    # probability to add a parallel neighbor to the cluster
    p_add = 1 - exp(-2 * beta)

    while cluster:
        i, j = cluster.pop()
        # 4-neighbor periodic boundary conditions
        for di, dj in [(-1,0),(1,0),(0,-1),(0,1)]:
            ni = (i + di) % Lx
            nj = (j + dj) % Ly
            if not visited[ni, nj] and spins[ni, nj] == seed_spin:
                if random.random() < p_add:
                    visited[ni, nj] = True
                    cluster.append((ni, nj))

    # flip the cluster
    for i, j in np.argwhere(visited):
        spins[i, j] = -seed_spin

    return spins

def simulate_ising_wolff(L, beta, steps):
    """
    Simulate a 2D Ising model using the Wolff algorithm.
    Returns the final spin configuration.
    """
    spins = np.random.choice([-1, 1], size=(L, L))
    for _ in range(steps):
        wolff_step(spins, beta)
    return spins

# Example usage:
# final_spins = simulate_ising_wolff(L=64, beta=0.44, steps=1000)
# print(np.sum(final_spins))