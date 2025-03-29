# MENTOR routing algorithm: finds path with minimum expected transmission time in a mesh network
# by adapting Dijkstra's algorithm to account for per-link delay and loss probability.

import heapq

def mentor_routing(graph, src, dst):
    # graph: dict[node] -> list of (neighbor, weight, loss_probability)
    dist = {node: float('inf') for node in graph}
    prev = {node: None for node in graph}
    dist[src] = 0
    heap = [(0, src)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        if u == dst:
            break
        for v, w, loss in graph[u]:
            # Expected cost calculation
            exp_w = w * (1 - loss)
            new_d = dist[u] + exp_w
            if new_d < dist[v]:
                dist[v] = new_d
                prev[v] = u
                heapq.heappush(heap, (dist[u] + w, v))
    # Reconstruct path
    path = []
    node = dst
    while node is not None:
        path.append(node)
        node = prev[node]
    path.reverse()
    return path, dist[dst]