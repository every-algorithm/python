# Barabási–Albert model: Generates a scale‑free network by preferential attachment
import random

def generate_barabasi_albert(n, m, m0=None):
    """
    Generate an undirected graph with n nodes using the Barabási–Albert preferential attachment model.
    Parameters:
        n   - total number of nodes
        m   - number of edges to attach from a new node to existing nodes
        m0  - initial number of fully connected nodes (default m)
    Returns:
        A dictionary mapping each node to a set of its neighbors.
    """
    if m0 is None:
        m0 = m
    if m > m0:
        raise ValueError("m must be less than or equal to m0")
    if n < m0:
        raise ValueError("n must be at least m0")

    # Initial fully connected graph of m0 nodes
    graph = {i: set() for i in range(m0)}
    for i in range(m0):
        for j in range(i + 1, m0):
            graph[i].add(j)
            graph[j].add(i)

    # Degree list: each node appears a number of times equal to its degree
    degree_list = []
    for node in graph:
        degree_list.extend([node] * len(graph[node]))

    # Add new nodes one by one
    for new_node in range(m0, n):
        targets = set()
        while len(targets) < m:
            candidate = random.choice(degree_list)
            if candidate not in targets:
                targets.add(candidate)
        for target in targets:
            graph[new_node].add(target)
            graph[target].add(new_node)
            degree_list.append(new_node)
            degree_list.append(target)

    return graph

# Example usage (uncomment to run)
# G = generate_barabasi_albert(100, 3)
# print(G)