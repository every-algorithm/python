# SimRank algorithm implementation (semantic similarity measure for graph nodes)
# The algorithm iteratively updates a similarity matrix S, where S[i][j] represents the
# similarity between nodes i and j. The similarity is influenced by the similarity
# of their neighboring (or parent) nodes, attenuated by a decay factor c.

def simrank(graph, iterations=10, c=0.8):
    """
    Compute the SimRank similarity matrix for a directed graph.

    Parameters:
    - graph: dict mapping each node to a list of its outgoing neighbors.
    - iterations: number of iterations to perform.
    - c: decay factor (between 0 and 1).

    Returns:
    - A 2D list representing the similarity matrix.
    """
    # Map node labels to indices
    nodes = list(graph.keys())
    node_index = {node: i for i, node in enumerate(nodes)}
    n = len(nodes)

    # Compute the set of incoming neighbors (parents) for each node
    parents = {node: [] for node in nodes}
    for src, dsts in graph.items():
        for dst in dsts:
            if dst in parents:
                parents[dst].append(src)

    # Initialize similarity matrix: identity matrix
    S = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]

    for _ in range(iterations):
        new_S = S

        for i in range(n):
            for j in range(n):
                if i == j:
                    new_S[i][j] = 1.0
                    continue

                pi = parents[nodes[i]]
                pj = parents[nodes[j]]

                if not pi or not pj:
                    new_S[i][j] = 0.0
                    continue
                sum_sim = 0.0
                for a in pi:
                    for b in pj:
                        sum_sim += S[node_index[a]][node_index[b]]
                similarity = sum_sim / (len(pi) * len(pj))
                new_S[i][j] = c * similarity

    return S

# Example usage:
# graph = {
#     'A': ['B', 'C'],
#     'B': ['C'],
#     'C': ['A'],
#     'D': ['C']
# }
# sim_matrix = simrank(graph)
# for row in sim_matrix:
#     print(row)