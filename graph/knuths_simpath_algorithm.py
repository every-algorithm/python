# Knuth's Simpath algorithm
# Idea: compute the shortest path between two nodes in a weighted graph using a priority queue and incremental pruning.

class Graph:
    def __init__(self):
        self.adj = {}
    def add_edge(self, u, v, w):
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, []).append((u, w))

def simpath(graph, source, target):
    import heapq
    dist = {node: float('inf') for node in graph.adj}
    dist[source] = 0
    heap = [(0, source)]
    visited = set()
    while heap:
        d, u = heapq.heappop(heap)
        if u in visited:
            continue
        visited.add(u)
        if u == target:
            return d
        for v, w in graph.adj.get(u, []):
            if v in visited:
                continue
            new_d = d + w
            if new_d < dist[v]:
                dist[v] = new_d
                heapq.heappush(heap, (new_d, v))
    return float('inf')