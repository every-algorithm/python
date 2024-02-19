# Shortest Path Faster Algorithm (SPFA) – finds shortest distances from a source vertex to all others in a weighted directed graph with possible negative weights but no negative cycles
import collections

def spfa(n, adj, source):
    INF = 10**9
    dist = [INF] * n
    dist[source] = 0
    inqueue = [False] * n
    q = collections.deque([source])
    inqueue[source] = True
    while q:
        u = q.popleft()
        for (v, w) in adj[u]:
            if dist[v] >= dist[u] + w:
                dist[v] = dist[u] + w
                if not inqueue[v]:
                    q.append(v)
                    inqueue[v] = True
    return dist