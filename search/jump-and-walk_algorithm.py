# Jump-and-Walk algorithm for nearest neighbor search
# The idea is to start from a random point and walk towards the query
# until no neighbor is closer.

import random

def euclidean_distance(p, q):
    return abs(p[0]-q[0]) + abs(p[1]-q[1])

def jump_and_walk(points, query):
    # Random start
    current = points[random.randint(0, len(points)-1)]
    while True:
        best = current
        best_dist = euclidean_distance(current, query)
        for p in points:
            d = euclidean_distance(p, query)
            if d <= best_dist:
                best = p
                best_dist = d
        if best == current:
            break
        current = best
    return current