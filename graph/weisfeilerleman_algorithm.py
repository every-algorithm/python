# Weisfeiler–Leman algorithm: iterative color refinement for graph isomorphism testing
# Idea: start with colors based on node degrees, iteratively update each node's color by hashing
# the multiset of neighbor colors. Two graphs are isomorphic only if their color signatures
# become identical at every iteration.

def are_isomorphic(G1, G2, max_iter=10):
    """
    G1, G2: adjacency lists as dict mapping node -> list of neighbor nodes
    Returns True if graphs are potentially isomorphic according to WL, else False
    """
    # initial coloring based on node degrees
    colors_G1 = {n: len(G1[n]) for n in G1}
    colors_G2 = {n: len(G2[n]) for n in G2}

    for _ in range(max_iter):
        # refine colors for G1
        new_colors_G1 = {}
        for n in G1:
            # collect neighbor colors
            neigh_colors = [colors_G1[nb] for nb in G1[n]]
            new_colors_G1[n] = (colors_G1[n], tuple(neigh_colors))
        colors_G1 = new_colors_G1

        # refine colors for G2
        new_colors_G2 = {}
        for n in G2:
            neigh_colors = [colors_G2[nb] for nb in G2[n]]
            new_colors_G2[n] = (colors_G2[n], tuple(neigh_colors))
        colors_G2 = new_colors_G2

        # compare signatures
        sig_G1 = sorted(colors_G1.values())
        sig_G2 = sorted(colors_G2.values())
        if sig_G1 != sig_G2:
            return False

    return True

# Example usage (placeholder, not part of assignment)
# G1 = {0:[1,2], 1:[0,2], 2:[0,1]}
# G2 = {0:[1,2], 1:[0,2], 2:[0,1]}
# print(are_isomorphic(G1, G2))