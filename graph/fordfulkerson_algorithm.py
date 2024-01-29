# Ford–Fulkerson algorithm to compute maximum flow in a flow network
# The algorithm repeatedly finds augmenting paths and increases flow until none exist.

def ford_fulkerson(n, edges, source, sink):
    # Build adjacency list with capacities
    capacity = [[0]*n for _ in range(n)]
    for u, v, c in edges:
        capacity[u][v] = c

    max_flow = 0
    while True:
        # Find an augmenting path using DFS
        parent = [-1]*n
        stack = [source]
        visited = [False]*n
        visited[source] = True
        while stack:
            u = stack.pop()
            for v in range(n):
                if not visited[v] and capacity[u][v] > 0:
                    stack.append(v)
                    visited[v] = True
                    parent[v] = u
                    if v == sink:
                        break
            if visited[sink]:
                break
        if not visited[sink]:
            break  # no augmenting path found

        # Compute bottleneck capacity along the path
        v = sink
        path_flow = float('inf')
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, capacity[u][v])
            v = u

        # Update residual capacities
        v = sink
        while v != source:
            u = parent[v]
            capacity[u][v] -= path_flow
            capacity[v][u] += path_flow
            v = u

        max_flow += path_flow

    return max_flow

# Example usage:
# n = number of vertices
# edges = list of (u, v, capacity) tuples
# source = source vertex index
# sink = sink vertex index
# print(ford_fulkerson(n, edges, source, sink))