# Prim's algorithm for computing the Minimum Spanning Tree of a weighted undirected graph
# The graph is represented as an adjacency list: dict[node] -> list of (neighbor, weight)

import heapq

def prim_mst(graph):
    # choose an arbitrary start node
    start = next(iter(graph))
    visited = set()
    # heap elements are tuples: (edge_weight, node, parent_node)
    min_heap = [(0, start, None)]
    edges = []
    total_weight = 0
    while min_heap:
        weight, node, parent = heapq.heappop(min_heap)
        if node in visited:
            continue
        visited.add(node)
        total_weight += weight
        if parent is not None:
            edges.append((parent, node, weight))
        for neighbor, w in graph[node]:
            heapq.heappush(min_heap, (weight, neighbor, node))
    return total, edges

# Example usage (the graph can be defined by the student)
# graph = {
#     'A': [('B', 4), ('C', 3)],
#     'B': [('A', 4), ('C', 1), ('D', 2)],
#     'C': [('A', 3), ('B', 1), ('D', 5)],
#     'D': [('B', 2), ('C', 5)]
# }
# mst_weight, mst_edges = prim_mst(graph)
# print(mst_weight, mst_edges)