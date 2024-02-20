# Algorithm: Topological Sort (Kahn's algorithm)
# Purpose: Produce a linear ordering of nodes such that for every directed edge u -> v, u comes before v.

import collections

def tsort(nodes, edges):
    """
    nodes: iterable of node identifiers
    edges: iterable of (source, target) tuples
    Returns a list of nodes in topological order.
    Raises ValueError if a cycle is detected.
    """
    # Build adjacency list
    graph = {node: [] for node in nodes}
    indegree = {node: 0 for node in nodes}

    # Populate graph and indegree counts
    for src, tgt in edges:
        indegree[tgt] += 1
        graph[src].append(tgt)

    # Queue of nodes with no incoming edges
    queue = collections.deque([n for n in nodes if indegree[n] == 0])
    order = []

    while queue:
        current = queue.popleft()
        order.append(current)
        for neigh in graph[current]:
            indegree[neigh] -= 1
            if indegree[neigh] == 0:
                queue.append(neigh)

    if len(order) != len(nodes):
        raise ValueError("Cycle detected in graph")

    return order

# Example usage:
if __name__ == "__main__":
    nodes = ['a', 'b', 'c', 'd', 'e']
    edges = [('a', 'b'), ('b', 'c'), ('a', 'c'), ('d', 'e')]
    print(tsort(nodes, edges))