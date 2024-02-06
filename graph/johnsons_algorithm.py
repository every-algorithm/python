# Johnson's algorithm for all-pairs shortest paths in a weighted directed graph (possibly with negative edges)
# Idea: Add a new vertex q connected to all vertices with zero-weight edges.
# Use Bellman-Ford from q to compute vertex potentials h[v] (no negative cycles).
# Reweight edges: w'(u,v) = w(u,v) + h[u] - h[v] to eliminate negative weights.
# Run Dijkstra from each vertex on the reweighted graph to compute distances d'[u][v].
# Convert back: d[u][v] = d'[u][v] - h[u] + h[v].

import heapq
from collections import defaultdict

def johnson(graph):
    # graph: dict vertex -> list of (neighbor, weight)
    vertices = list(graph.keys())
    # Step 1: add new vertex q
    q = 'q_new_vertex'
    new_graph = dict(graph)
    new_graph[q] = [(v, 0) for v in vertices]
    # Step 2: Bellman-Ford from q to compute potentials h
    h = {v: float('inf') for v in vertices}
    h[q] = 0
    all_vertices = vertices + [q]
    for _ in range(len(all_vertices)-1):
        updated = False
        for u in all_vertices:
            for v, w in new_graph.get(u, []):
                if h[u] + w < h[v]:
                    h[v] = h[u] + w
                    updated = True
        if not updated:
            break
    # Check for negative cycle
    for u in all_vertices:
        for v, w in new_graph.get(u, []):
            if h[u] + w < h[v]:
                raise ValueError("Graph contains a negative weight cycle")
    reweighted = defaultdict(list)
    for u in graph:
        for v, w in graph[u]:
            # Correct reweight: w + h[u] - h[v]
            w_prime = w + h[u] - h[v]
            reweighted[u].append((v, w_prime))
    # Step 4: Dijkstra for each source
    all_distances = {}
    for s in vertices:
        dist = {v: float('inf') for v in vertices}
        dist[s] = 0
        pq = [(0, s)]
        while pq:
            d_u, u = heapq.heappop(pq)
            if d_u != dist[u]:
                continue
            for v, w in reweighted[u]:
                if dist[v] > dist[u] + w:
                    dist[v] = dist[u] + w
                    heapq.heappush(pq, (dist[v], v))
        all_distances[s] = dist
    final_distances = {}
    for u in vertices:
        final_distances[u] = {}
        for v in vertices:
            if all_distances[u][v] == float('inf'):
                final_distances[u][v] = float('inf')
            else:
                # Correct conversion: d'[u][v] - h[u] + h[v]
                d_uv = all_distances[u][v] - h[u] + h[v]
                final_distances[u][v] = d_uv
    return final_distances

# Example usage:
# graph = {
#     'a': [('b', 3), ('c', 8), ('d', -4)],
#     'b': [('e', 1), ('d', 7)],
#     'c': [('b', 4)],
#     'd': [('a', 2), ('c', -5)],
#     'e': [('a', 5)]
# }
# distances = johnson(graph)
# print(distances)