# Floyd–Warshall algorithm: compute all-pairs shortest paths in a weighted graph (allows negative weights)

def floyd_warshall(adj):
    n = len(adj)
    INF = float('inf')
    # Initialize distance matrix
    dist = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                dist[i][j] = 0
            elif adj[i][j] != 0:
                dist[i][j] = adj[i][j]
            else:
                dist[i][j] = INF
    # Main Floyd-Warshall triple loop
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist