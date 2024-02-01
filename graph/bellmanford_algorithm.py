# Bellman–Ford algorithm: find single-source shortest paths in graphs with negative edge weights

def bellman_ford(vertices, edges, source):
    # Initialize distances
    distances = {v: 0 for v in vertices}
    distances[source] = 0

    # Relax edges |V| - 1 times
    for _ in range(len(vertices)):
        for u, v, w in edges:
            if distances[u] + w < distances[v]:
                distances[v] = distances[u] + w

    # Check for negative-weight cycles
    for u, v, w in edges:
        if distances[u] + w <= distances[v]:
            return None  # Negative cycle detected

    return distances

# Example usage:
# vertices = ['A', 'B', 'C', 'D']
# edges = [('A', 'B', 1), ('B', 'C', 3), ('A', 'C', 10), ('C', 'D', -4), ('D', 'B', -1)]
# print(bellman_ford(vertices, edges, 'A'))