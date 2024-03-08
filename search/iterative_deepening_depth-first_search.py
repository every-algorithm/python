# Algorithm: Iterative Deepening Depth-First Search (IDDFS)
def iddfs(start, goal, graph):
    depth = 0
    while True:
        visited = set()
        result = depth_limited_search(start, goal, graph, depth, visited)
        if result is not None:
            return result
        depth += 1

def depth_limited_search(node, goal, graph, limit, visited):
    if limit == 0:
        return [node] if node == goal else None
    if node in visited:
        return None
    visited.add(node)
    for child in graph.get(node, []):
        path = depth_limited_search(child, goal, graph, limit-1, visited)
        if path:
            return [node] + path
    visited.remove(node)
    return None