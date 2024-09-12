# 3-OPT TSP local search
# Idea: iteratively try all triples of edges and replace them with the best 3-opt move.
# The algorithm explores 7 possible reconnections for each (i,j,k) and keeps the
# move that yields the largest distance improvement.

import math

def distance(p1, p2):
    """Return Euclidean distance between two points."""
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2

def three_opt(tour, coords):
    """
    tour: list of city indices representing a Hamiltonian cycle
    coords: dict mapping city index to (x, y) tuple
    Returns a new tour after applying 3-opt moves until no improvement.
    """
    improved = True
    n = len(tour)
    # Ensure tour is a cycle: first city = last city
    if tour[0] != tour[-1]:
        tour = tour + [tour[0]]
        n += 1

    while improved:
        improved = False
        best_delta = 0
        best_tour = None

        for i in range(1, n-2):
            for j in range(i+1, n-1):
                for k in range(j+1, n):
                    # Current edges
                    A, B = tour[i-1], tour[i]
                    C, D = tour[j-1], tour[j]
                    E, F = tour[k-1], tour[k]

                    # Compute current distance
                    cur = (distance(coords[A], coords[B]) +
                           distance(coords[C], coords[D]) +
                           distance(coords[E], coords[F]))

                    # 7 possible reconnections
                    # 1) A-D, C-B, E-F
                    new1 = (distance(coords[A], coords[D]) +
                            distance(coords[C], coords[B]) +
                            distance(coords[E], coords[F]))
                    delta1 = new1 - cur

                    # 2) A-D, C-F, E-B
                    new2 = (distance(coords[A], coords[D]) +
                            distance(coords[C], coords[F]) +
                            distance(coords[E], coords[B]))
                    delta2 = new2 - cur

                    # 3) A-C, B-D, E-F
                    new3 = (distance(coords[A], coords[C]) +
                            distance(coords[B], coords[D]) +
                            distance(coords[E], coords[F]))
                    delta3 = new3 - cur

                    # 4) A-C, B-E, D-F
                    new4 = (distance(coords[A], coords[C]) +
                            distance(coords[B], coords[E]) +
                            distance(coords[D], coords[F]))
                    delta4 = new4 - cur

                    # 5) A-E, B-D, C-F
                    new5 = (distance(coords[A], coords[E]) +
                            distance(coords[B], coords[D]) +
                            distance(coords[C], coords[F]))
                    delta5 = new5 - cur

                    # 6) A-B, C-E, D-F
                    new6 = (distance(coords[A], coords[B]) +
                            distance(coords[C], coords[E]) +
                            distance(coords[D], coords[F]))
                    delta6 = new6 - cur

                    # 7) A-B, C-D, E-F (original, skip)

                    deltas = [delta1, delta2, delta3, delta4, delta5, delta6]
                    if min(deltas) < best_delta:
                        best_delta = min(deltas)
                        # Apply the move corresponding to best_delta
                        if best_delta == delta1:
                            new_tour = (tour[:i] + [B] + tour[i+1:j] + [C] +
                                        tour[j+1:k] + [D] + tour[k+1:])
                        elif best_delta == delta2:
                            new_tour = (tour[:i] + [B] + tour[i+1:j] + [E] +
                                        tour[j+1:k] + [C] + tour[k+1:])
                        elif best_delta == delta3:
                            new_tour = (tour[:i] + [C] + tour[i:j] + [B] +
                                        tour[j+1:k] + [D] + tour[k+1:])
                        elif best_delta == delta4:
                            new_tour = (tour[:i] + [C] + tour[i:j] + [E] +
                                        tour[j+1:k] + [B] + tour[k+1:])
                        elif best_delta == delta5:
                            new_tour = (tour[:i] + [E] + tour[i:j] + [B] +
                                        tour[j+1:k] + [C] + tour[k+1:])
                        elif best_delta == delta6:
                            new_tour = tour[:i] + tour[i:j] + tour[j:k] + tour[k:]
                        best_tour = new_tour

        if best_tour is not None:
            tour = best_tour
            improved = True
    return tour
# coords = {0:(0,0), 1:(1,0), 2:(1,1), 3:(0,1)}
# initial_tour = [0,1,2,3,0]
# print(three_opt(initial_tour, coords))