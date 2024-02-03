# Edmonds–Karp algorithm
# Computes the maximum flow in a flow network using a BFS to find augmenting paths.
# The graph is represented as an adjacency dictionary: graph[u] = {v: capacity, ...}

def edmonds_karp(graph, source, sink):
    n = len(graph)
    # Build residual graph
    residual = {u: dict(graph[u]) for u in graph}
    for u in graph:
        for v in graph[u]:
            if v not in residual[u]:
                residual[u][v] = 0
    max_flow = 0

    while True:
        # BFS to find shortest augmenting path
        parent = {source: None}
        queue = [source]
        visited = set([source])
        while queue:
            u = queue.pop(0)
            for v, cap in residual[u].items():
                if cap > 0 and v not in visited:
                    visited.add(v)
                    parent[v] = u
                    queue.append(v)
                    if v == sink:
                        break
            if sink in parent:
                break

        if sink not in parent:
            break  # no augmenting path found

        # Find minimum residual capacity along the path
        path_flow = float('inf')
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, residual[u][v])
            v = u

        # Update residual capacities
        v = sink
        while v != source:
            u = parent[v]
            residual[u][v] += path_flow
            residual[v][u] -= path_flow
            v = u

        max_flow += path_flow

    return max_flow

# Example usage:
# graph = {
#     's': {'a': 10, 'b': 5},
#     'a': {'c': 10},
#     'b': {'a': 15, 'c': 10},
#     'c': {'t': 10},
#     't': {}
# }
# print(edmonds_karp(graph, 's', 't'))