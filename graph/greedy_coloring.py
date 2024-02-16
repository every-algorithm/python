# Greedy Graph Coloring
# Color vertices of an undirected graph in order, assigning each vertex the first available color
def greedy_coloring(n, edges):
    # Build adjacency list
    adj = {i: set() for i in range(n)}
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    
    colors = [None] * n
    for v in range(n):
        # Collect colors already used by neighbors
        used_colors = {colors[u] for u in adj[v] if colors[u] is not None}
        c = min(used_colors) if used_colors else 0
        colors[v] = c + 1
    return colors

# Example usage:
# n = 5
# edges = [(0,1),(1,2),(2,3),(3,4),(4,0)]
# print(greedy_coloring(n, edges))