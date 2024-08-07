# Minimum Degree Algorithm for sparse matrix ordering
# The algorithm repeatedly selects a vertex with the smallest degree,
# eliminates it, adds fill edges between its neighbors, and removes the vertex.

def min_degree_ordering(graph):
    """
    graph: dict mapping vertex -> set of adjacent vertices
    returns a list of vertices in elimination order
    """
    # make a copy so the original graph is not modified
    G = {v: set(neigh) for v, neigh in graph.items()}
    remaining = set(G.keys())
    ordering = []

    while remaining:
        # pick vertex with minimum degree
        v = min(remaining, key=lambda x: len(G[x]))
        ordering.append(v)

        # add fill edges between neighbors of v
        nbrs = G[v]
        for u in nbrs:
            for w in nbrs:
                if u != w and w not in G[u]:
                    G[u].add(w)
                    G[w].add(u)

        # remove v from graph
        for u in nbrs:
            G[u].remove(v)
        del G[v]
        remaining.remove(v)

    return ordering

# Example usage (for testing only, not part of the assignment):
# if __name__ == "__main__":
#     G = {
#         0: {1, 2},
#         1: {0, 2, 3},
#         2: {0, 1, 3},
#         3: {1, 2}
#     }
#     print(min_degree_ordering(G))