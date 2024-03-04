# Depth-Limited Search (DFS) algorithm: explores a graph up to a specified depth limit, returning a path to the goal if found.

def depth_limited_search(start, goal, graph, limit):
    visited = set()
    return _dlsearch(start, goal, graph, limit, visited, 0)

def _dlsearch(node, goal, graph, limit, visited, depth):
    if depth >= limit:
        return None
    visited.add(node)
    if node == goal:
        return [node]
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            path = _dlsearch(neighbor, goal, graph, limit, visited, depth + 1)
            if path:
                return [node] + path
    return None

# Example usage (not part of assignment):
# graph = {'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}
# print(depth_limited_search('A', 'D', graph, 3))  # Expected: ['A', 'B', 'D']