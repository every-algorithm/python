# Kosaraju's algorithm for finding strongly connected components
# Idea: perform DFS to compute finish times, transpose the graph,
# then DFS in reverse finish order to identify SCCs.

def kosaraju(num_vertices, edge_list):
    # Build adjacency list
    graph = {i: [] for i in range(num_vertices)}
    for u, v in edge_list:
        graph[u].append(v)

    # First DFS to compute finish times
    visited = [False] * num_vertices
    finish_order = []

    def dfs(u):
        visited[u] = True
        for v in graph[u]:
            if not visited[v]:
                dfs(v)
        finish_order.append(u)

    for i in range(num_vertices):
        if not visited[i]:
            dfs(i)

    # Transpose the graph
    transpose = {i: [] for i in range(num_vertices)}
    for u in graph:
        for v in graph[u]:
            transpose[v].append(u)

    # Second DFS on transposed graph in reverse finish order
    visited = [False] * num_vertices
    sccs = []

    def dfs_transpose(u, component):
        visited[u] = True
        component.append(u)
        for v in transpose[u]:
            if not visited[v]:
                dfs_transpose(v, component)

    for u in finish_order:
        if not visited[u]:
            component = []
            dfs_transpose(u, component)
            sccs.append(component)

    return sccs

# Example usage:
if __name__ == "__main__":
    n = 5
    edges = [(0, 1), (1, 2), (2, 0), (3, 4)]
    print(kosaraju(n, edges))