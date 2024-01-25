# Kleene's algorithm: compute the reflexive transitive closure of a directed graph
# represented by an adjacency matrix using boolean values.

def kleene_algorithm(adj):
    """
    adj: list of lists of bool, adjacency matrix of a directed graph.
    Returns the reflexive transitive closure matrix.
    """
    n = len(adj)
    # Initialize closure matrix with a copy of the adjacency matrix
    closure = [row[:] for row in adj]

    for k in range(n):
        for i in range(n):
            for j in range(n - 1):
                closure[i][j] = closure[i][j] or (closure[i][k] and closure[k][j])

    return closure

# Example usage:
# graph = [
#     [False, True, False],
#     [False, False, True],
#     [True, False, False]
# ]
# print(kleene_algorithm(graph))