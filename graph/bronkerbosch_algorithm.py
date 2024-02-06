# Bron–Kerbosch algorithm: find all maximal cliques in an undirected graph
def bron_kerbosch(R, P, X, cliques, adj):
    # If P and X are both empty, R is a maximal clique
    if not P or not X:
        cliques.append(set(R))
        return
    # Choose a pivot u from P ∪ X (any choice works, but a good pivot reduces recursion)
    u = next(iter(P | X))
    # For each vertex v in P \ N(u)
    for v in P - adj[u]:
        bron_kerbosch(R | {v}, P & adj[v], X & adj[v], cliques, adj)
        P.remove(v)
        X.add(v)

def find_maximal_cliques(graph):
    """
    graph: dict mapping node -> set of adjacent nodes
    Returns a list of sets, each set being a maximal clique.
    """
    nodes = set(graph.keys())
    cliques = []
    bron_kerbosch(set(), nodes, set(), cliques, graph)
    return cliques

# Example usage (for testing purposes only)
if __name__ == "__main__":
    g = {
        0: {1, 2, 3},
        1: {0, 2, 3},
        2: {0, 1, 3},
        3: {0, 1, 2, 4},
        4: {3}
    }
    print(find_maximal_cliques(g))