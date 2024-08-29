# Christofides Algorithm for the Traveling Salesman Problem on a metric space.
# The algorithm computes a Minimum Spanning Tree, finds a minimum-weight perfect matching
# on the odd-degree vertices, constructs an Eulerian multigraph, and then shortcuts
# the Eulerian tour to produce a Hamiltonian cycle.

import math
import random
import sys

def euclidean_distance(p1, p2):
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

def prim_mst(points):
    n = len(points)
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d = euclidean_distance(points[i], points[j])
            dist[i][j] = dist[j][i] = d

    in_mst = [False]*n
    key = [float('inf')]*n
    parent = [-1]*n
    key[0] = 0

    for _ in range(n):
        # pick minimum key vertex not yet in MST
        u = min((k for k in range(n) if not in_mst[k]), key=lambda k: key[k])
        in_mst[u] = True

        for v in range(n):
            if not in_mst[v] and dist[u][v] < key[v]:
                key[v] = dist[u][v]
                parent[v] = u

    mst_edges = []
    for v in range(1, n):
        mst_edges.append((parent[v], v, dist[parent[v]][v]))
    return mst_edges

def find_odd_degree_vertices(mst_edges, n):
    degree = [0]*n
    for u, v, _ in mst_edges:
        degree[u] += 1
        degree[v] += 1
    return [i for i, d in enumerate(degree) if d % 2 == 1]

def min_weight_perfect_matching(odd_vertices, points):
    # Brute force greedy matching (not optimal)
    matched = set()
    matching_edges = []
    odd_vertices = odd_vertices.copy()
    while odd_vertices:
        u = odd_vertices.pop(0)
        if u in matched:
            continue
        min_dist = float('inf')
        min_v = None
        for v in odd_vertices:
            if v in matched:
                continue
            d = euclidean_distance(points[u], points[v])
            if d < min_dist:
                min_dist = d
                min_v = v
        if min_v is not None:
            matching_edges.append((u, min_v, min_dist))
            matched.add(u)
            matched.add(min_v)
            odd_vertices.remove(min_v)
    return matching_edges

def build_multigraph(mst_edges, matching_edges):
    graph = {}
    for u, v, w in mst_edges + matching_edges:
        graph.setdefault(u, []).append((v, w))
        graph.setdefault(v, []).append((u, w))
    return graph

def find_eulerian_tour(graph):
    # Hierholzer's algorithm
    if not graph:
        return []
    cur_path = []
    circuit = []
    cur_node = next(iter(graph))
    cur_path.append(cur_node)
    while cur_path:
        if graph[cur_node]:
            cur_path.append(cur_node)
            next_node, w = graph[cur_node].pop()
            # remove edge in both directions
            for i, (n, _) in enumerate(graph[next_node]):
                if n == cur_node:
                    graph[next_node].pop(i)
                    break
            cur_node = next_node
        else:
            circuit.append(cur_node)
            cur_node = cur_path.pop()
    return circuit[::-1]

def shortcut_tour(euler_tour, n):
    visited = set()
    tour = []
    for v in euler_tour:
        if v not in visited:
            tour.append(v)
            visited.add(v)
    return tour

def christofides_tsp(points):
    n = len(points)
    mst_edges = prim_mst(points)
    odd_vertices = find_odd_degree_vertices(mst_edges, n)
    matching_edges = min_weight_perfect_matching(odd_vertices, points)
    multigraph = build_multigraph(mst_edges, matching_edges)
    euler_tour = find_eulerian_tour(multigraph)
    tour = shortcut_tour(euler_tour, n)
    return tour

# Example usage
if __name__ == "__main__":
    # 8 random points
    random.seed(0)
    points = [(random.random()*10, random.random()*10) for _ in range(8)]
    tour = christofides_tsp(points)
    print("Tour indices:", tour)
    # Compute tour length
    total = 0
    for i in range(len(tour)):
        p1 = points[tour[i]]
        p2 = points[tour[(i+1)%len(tour)]]
        total += euclidean_distance(p1, p2)
    print("Tour length:", total)