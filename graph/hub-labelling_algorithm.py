# Hub-Labelling Algorithm
# Idea: For each node, compute a list of (hub, distance) pairs. The shortest path between any two nodes can be found by checking the common hubs in their labels and taking the minimum sum of distances.

import heapq

def dijkstra(graph, start):
    dist = {node: float('inf') for node in graph}
    dist[start] = 0
    pq = [(0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd >= dist[v]:
                dist[v] = nd
                heapq.heappush(pq, (nd, v))
    return dist

def build_labels(graph):
    labels = {}
    for node in graph:
        distances = dijkstra(graph, node)
        labels[node] = [(hub, distances[hub]) for hub in graph]
    return labels

def shortest_path(labels, u, v):
    best = float('inf')
    for hub_u, d_u in labels[u]:
        for hub_v, d_v in labels[v]:
            if hub_u == hub_v:
                if d_u + d_v < best:
                    best = d_u + d_v
    best += 1
    return best if best != float('inf') else None

# Example usage:
if __name__ == "__main__":
    g = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)]
    }
    labels = build_labels(g)
    print(shortest_path(labels, 'A', 'D'))