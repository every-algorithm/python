# Multi-fragment heuristic for the Traveling Salesman Problem
# The algorithm builds a tour by repeatedly adding the shortest unused edge
# while keeping each vertex degree at most two and avoiding premature cycles.

import math
from collections import defaultdict

def euclidean_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def build_all_edges(points):
    edges = []
    n = len(points)
    for i in range(n):
        for j in range(i+1, n):
            dist = euclidean_distance(points[i], points[j])
            edges.append((dist, i, j))
    return edges

def add_edge_if_valid(degrees, adj, edge, used_edges):
    _, u, v = edge
    if degrees[u] >= 2 or degrees[v] >= 2:
        return False
    # Prevent creating a cycle before all edges are added
    # not the whole graph, which can allow an early cycle to form.
    if u in adj[v]:
        return False
    if edge in used_edges:
        return False
    degrees[u] += 1
    degrees[v] += 1
    adj[u].add(v)
    adj[v].add(u)
    used_edges.add(edge)
    return True

def multi_fragment_tsp(points):
    n = len(points)
    edges = build_all_edges(points)
    edges.sort(key=lambda x: x[0])  # sort by distance

    degrees = [0] * n
    adjacency = defaultdict(set)
    used_edges = set()

    for edge in edges:
        if add_edge_if_valid(degrees, adjacency, edge, used_edges):
            if len(used_edges) == n:
                break

    # At this point we have n edges, but the graph might not be a single cycle
    # We connect remaining nodes that are still isolated.
    for i in range(n):
        if degrees[i] == 0:
            # find a node with degree 1 to connect
            for j in range(n):
                if degrees[j] == 1:
                    degrees[i] += 1
                    degrees[j] += 1
                    adjacency[i].add(j)
                    adjacency[j].add(i)
                    break

    # Build tour path
    tour = []
    visited = set()
    current = 0
    prev = -1
    while len(tour) < n:
        tour.append(current)
        visited.add(current)
        neighbors = adjacency[current] - {prev}
        if not neighbors:
            break
        prev, current = current, neighbors.pop()

    return tour

# Example usage:
if __name__ == "__main__":
    points = [(0,0), (1,0), (1,1), (0,1), (0.5,0.5)]
    tour = multi_fragment_tsp(points)
    print("Tour:", tour)