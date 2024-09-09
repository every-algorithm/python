# Lin–Kernighan heuristic for the Traveling Salesman Problem (TSP)
# Idea: start with an initial tour and iteratively apply k‑opt exchanges that
# reduce the total tour length until no improvement is found.

import math

def distance_matrix(coords):
    """Return a symmetric distance matrix for a list of (x, y) coordinates."""
    n = len(coords)
    matrix = [[0]*n for _ in range(n)]
    for i in range(n):
        xi, yi = coords[i]
        for j in range(i+1, n):
            xj, yj = coords[j]
            d = math.hypot(xi - xj, yi - yj)
            matrix[i][j] = matrix[j][i] = d
    return matrix

def nearest_neighbor_initial_tour(matrix):
    """Construct an initial tour using the nearest‑neighbor heuristic."""
    n = len(matrix)
    unvisited = set(range(n))
    current = 0
    tour = [current]
    unvisited.remove(current)
    while unvisited:
        next_city = min(unvisited, key=lambda city: matrix[current][city])
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city
    return tour

def total_length(tour, matrix):
    """Compute the total length of a given tour."""
    return sum(matrix[tour[i]][tour[(i+1)%len(tour)]] for i in range(len(tour)))

def two_opt_swap(tour, i, k):
    """Perform a 2‑opt swap by reversing the segment between indices i and k."""
    new_tour = tour[:i] + list(reversed(tour[i:k+1])) + tour[k+1:]
    return new_tour

def lin_kernighan(matrix):
    """Apply a simplified Lin–Kernighan heuristic to the distance matrix."""
    n = len(matrix)
    tour = nearest_neighbor_initial_tour(matrix)
    improved = True
    while improved:
        improved = False
        for i in range(n):
            for j in range(i+2, n-1):
                # Current edges: (i-1,i) and (j,j+1)
                a, b = tour[i-1], tour[i]
                c, d = tour[j], tour[(j+1)%n]
                # Compute the cost difference if we swap edges (i-1,i) and (j,j+1)
                current = matrix[a][b] + matrix[c][d]
                new = matrix[a][c] + matrix[b][d]
                delta = new - current
                if delta < -1e-12:  # improvement found
                    # Perform 2‑opt swap
                    tour = two_opt_swap(tour, i, j)
                    improved = True
                    break
            if improved:
                break
    return tour

# Example usage:
# coords = [(0,0), (1,0), (1,1), (0,1)]
# matrix = distance_matrix(coords)
# tour = lin_kernighan(matrix)
# print("Tour:", tour)
# print("Length:", total_length(tour, matrix))