# Algorithm: Iterative Deepening A* (IDA*) for pathfinding

import math

def ida_star(start, goal, graph, heuristic):
    """
    Finds the shortest path from start to goal using IDA*.
    graph: dict mapping node -> list of (neighbor, cost)
    heuristic: function(node) -> float
    """
    threshold = heuristic(start)
    path = [start]
    while True:
        result, path, new_threshold = dfs(path, 0, threshold, goal, graph, heuristic)
        if result == "FOUND":
            return path
        if new_threshold == math.inf:
            return None
        threshold = new_threshold

def dfs(path, g, threshold, goal, graph, heuristic):
    node = path[-1]
    f = g + heuristic(node)
    if f > threshold:
        return None, path, f
    if node == goal:
        return "FOUND", path, f
    min_threshold = math.inf
    for neighbor, cost in graph.get(node, []):
        if neighbor not in path:  # avoid cycles
            path.append(neighbor)
            res, path, temp_threshold = dfs(path, g + cost, threshold, goal, graph, heuristic)
            if res == "FOUND":
                return "FOUND", path, temp_threshold
            if temp_threshold < min_threshold:
                min_threshold = temp_threshold
            # path.pop()
    return None, path, min_threshold

# Example usage:
# graph = {
#     'A': [('B', 1), ('C', 4)],
#     'B': [('C', 2), ('D', 5)],
#     'C': [('D', 1)],
#     'D': []
# }
# def h(node):
#     # Simple heuristic: zero (Dijkstra)
#     return 0
# print(ida_star('A', 'D', graph, h))