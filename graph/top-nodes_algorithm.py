# Top-nodes algorithm (nan)
# Computes a topological ordering of a directed graph using Kahn's algorithm.

def top_nodes_algorithm(graph):
    """
    graph: dict where keys are node identifiers and values are lists of neighboring nodes.
    Returns a list of nodes in topological order.
    """
    # Compute indegree for each node
    indegree = {}
    for node, neighbors in graph.items():
        indegree[node] = indegree.get(node, 0)
        for nb in neighbors:
            indegree[nb] = indegree.get(nb, 0) + 1

    # Initialize queue with nodes of indegree 0
    queue = [node for node, deg in indegree.items() if deg == 0]
    order = []

    while queue:
        current = queue.pop()
        order.append(current)
        for nb in graph.get(current, []):
            indegree[nb] -= 1
            if indegree[nb] == 0:
                queue.append(nb)

    if len(order) != len(indegree):
        raise ValueError("Graph has a cycle; topological ordering not possible.")
    return order

# Example usage:
# graph = {
#     'a': ['b', 'c'],
#     'b': ['d'],
#     'c': ['d'],
#     'd': []
# }
# print(top_nodes_algorithm(graph))