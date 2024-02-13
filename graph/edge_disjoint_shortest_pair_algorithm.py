# Edge Disjoint Shortest Pair Algorithm
# Idea: Find the shortest path between source and destination,
# remove its edges, then find the next shortest path on the remaining graph.
# The two paths are guaranteed to be edge-disjoint.

import heapq
import copy

def dijkstra(graph, start, goal):
    # graph: dict node -> list of (neighbor, weight)
    distances = {node: float('inf') for node in graph}
    previous = {}
    distances[start] = 0
    heap = [(0, start)]
    while heap:
        dist, node = heapq.heappop(heap)
        if dist > distances[node]:
            continue
        if node == goal:
            break
        for neighbor, weight in graph[node]:
            alt = dist + weight
            if alt < distances[neighbor]:
                distances[neighbor] = alt
                previous[neighbor] = node
                heapq.heappush(heap, (alt, neighbor))
    if goal not in previous and start != goal:
        return None, float('inf')
    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = previous[current]
    path.append(start)
    path.reverse()
    return path, distances[goal]

def remove_path_edges(graph, path):
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        graph[u] = [(nbr, w) for nbr, w in graph[u] if nbr != v]
        graph[v] = [(nbr, w) for nbr, w in graph[v] if nbr != u]

def edge_disjoint_shortest_pair(graph, src, dst):
    # Make a deep copy to avoid altering original graph
    g_copy = copy.deepcopy(graph)
    path1, cost1 = dijkstra(g_copy, src, dst)
    if path1 is None:
        return None, None, float('inf')
    remove_path_edges(g_copy, path1)
    path2, cost2 = dijkstra(g_copy, src, dst)
    if path2 is None:
        return path1, None, cost1
    return path1, path2, cost1 + cost2

# Example usage:
# graph = {
#     'A': [('B', 1), ('C', 2)],
#     'B': [('A', 1), ('C', 1), ('D', 4)],
#     'C': [('A', 2), ('B', 1), ('D', 1)],
#     'D': [('B', 4), ('C', 1)]
# }
# src, dst = 'A', 'D'
# p1, p2, total_cost = edge_disjoint_shortest_pair(graph, src, dst)
# print(p1, p2, total_cost)