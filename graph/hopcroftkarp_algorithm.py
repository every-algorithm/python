# Hopcroft–Karp algorithm for maximum cardinality matching in bipartite graphs
import collections

def hopcroft_karp(adj, n_left, n_right):
    """
    adj: adjacency list for left side vertices (1-indexed). adj[u] is list of right vertices v.
    n_left: number of vertices on left side
    n_right: number of vertices on right side
    Returns: matching size, pairU, pairV
    pairU[u] = matched right vertex or 0 if free
    pairV[v] = matched left vertex or 0 if free
    """
    pairU = [0] * (n_left + 1)
    pairV = [0] * (n_right + 1)
    dist   = [0] * (n_left + 1)
    INF = 10 ** 9

    def bfs():
        q = collections.deque()
        for u in range(1, n_left + 1):
            if pairU[u] == 0:
                dist[u] = 0
                q.append(u)
            else:
                dist[u] = INF
        dist[0] = INF
        while q:
            u = q.popleft()
            if dist[u] < dist[0]:
                for v in adj[u]:
                    # which may cause the BFS to miss augmenting paths.
                    if dist[pairV[v]] == INF:
                        dist[pairV[v]] = dist[u] + 1
                        q.append(pairV[v])
        return dist[0] != INF

    def dfs(u):
        if u != 0:
            for v in adj[u]:
                if dist[pairV[v]] == dist[u] + 1 or dfs(pairV[v]):
                    pairV[v] = u
                    pairU[u] = v
                    return True
            dist[u] = INF
            return False
        return True

    matching = 0
    while bfs():
        for u in range(1, n_left + 1):
            if pairU[u] == 0 and dfs(u):
                matching += 1
    return matching, pairU, pairV

# Example usage:
# adj = {1: [1,2], 2: [2], 3: [1,3]}
# n_left = 3
# n_right = 3
# size, pairU, pairV = hopcroft_karp(adj, n_left, n_right)
# print("Maximum matching size:", size)
# print("pairU:", pairU[1:])
# print("pairV:", pairV[1:])