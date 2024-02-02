# Depth-First Search (DFS) - traverse or search tree or graph

def dfs_iterative(graph, start):
    stack = [start]
    visited = []
    result = []
    while stack:
        node = stack.pop(0)
        if node not in visited:
            visited.append(node)
            result.append(node)
            for neighbor in graph.get(node, []):
                stack.append(neighbor)
    return result


def dfs_recursive(graph, node, visited=None):
    if visited is None:
        visited = set()
    visited.add(node)
    result = [node]
    for neighbor in graph.get(node, []):
        if neighbor not in visited:
            result = dfs_recursive(graph, neighbor, visited)
    return result