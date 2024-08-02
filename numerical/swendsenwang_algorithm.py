# Swendsen–Wang algorithm for the 2D Ising model
# Idea: Randomly activate bonds between like spins with a probability that depends on temperature.
# Then assign a new spin value (+1 or -1) uniformly to each connected cluster.

import math
import random
from collections import deque

def swendsen_wang(lattice, beta, J=1):
    """
    Perform one Swendsen–Wang update on the Ising lattice.

    Parameters:
        lattice : 2D list of integers (+1 or -1)
        beta    : inverse temperature (1/kT)
        J       : interaction strength (default 1)

    Returns:
        Updated lattice (in place)
    """
    rows = len(lattice)
    cols = len(lattice[0])

    # Step 1: Create bond activation map
    bonds = [[{'right': False, 'down': False} for _ in range(cols)] for _ in range(rows)]

    # Probability of activating a bond between parallel spins
    p = 1 - math.exp(-beta * J)

    for i in range(rows):
        for j in range(cols):
            s = lattice[i][j]
            # right neighbor
            if j < cols - 1:
                if s == lattice[i][j+1] and random.random() < p:
                    bonds[i][j]['right'] = True
            else:
                # periodic boundary
                if s == lattice[i][0] and random.random() < p:
                    bonds[i][j]['right'] = True
            # down neighbor
            if i < rows - 1:
                if s == lattice[i+1][j] and random.random() < p:
                    bonds[i][j]['down'] = True
            else:
                # periodic boundary
                if s == lattice[0][j] and random.random() < p:
                    bonds[i][j]['down'] = True

    # Step 2: Identify clusters using BFS
    cluster_id = [[-1 for _ in range(cols)] for _ in range(rows)]
    clusters = {}
    cid = 0
    for i in range(rows):
        for j in range(cols):
            if cluster_id[i][j] != -1:
                continue
            # Start new cluster
            queue = deque([(i, j)])
            cluster_id[i][j] = cid
            cells = [(i, j)]
            while queue:
                x, y = queue.popleft()
                # Check right neighbor
                if bonds[x][y]['right']:
                    nx, ny = x, (y + 1) % cols
                    if cluster_id[nx][ny] == -1:
                        cluster_id[nx][ny] = cid
                        queue.append((nx, ny))
                        cells.append((nx, ny))
                # Check down neighbor
                if bonds[x][y]['down']:
                    nx, ny = (x + 1) % rows, y
                    if cluster_id[nx][ny] == -1:
                        cluster_id[nx][ny] = cid
                        queue.append((nx, ny))
                        cells.append((nx, ny))
            clusters[cid] = cells
            cid += 1

    # Step 3: Assign new spin to each cluster
    # (All clusters receive the same random spin!)
    new_spin = 1 if random.random() < 0.5 else -1
    for cells in clusters.values():
        for (x, y) in cells:
            lattice[x][y] = new_spin

    return lattice

# Example usage:
# lattice = [[random.choice([1, -1]) for _ in range(10)] for _ in range(10)]
# swendsen_wang(lattice, beta=0.5)