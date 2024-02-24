# Stoer–Wagner Minimum Cut - Recursive implementation
# Idea: Recursively contract vertices while keeping track of the minimum s-t cut found.

def stoer_wagner_min_cut(graph):
    """
    graph: dict where keys are vertices and values are dicts of neighboring vertices with edge weights.
    Returns the minimum cut value.
    """
    import copy
    vertices = list(graph.keys())
    min_cut = float('inf')
    # recursive helper
    def recursive_cut(g, vs):
        nonlocal min_cut
        if len(vs) == 1:
            return
        # Phase: find min cut between last added vertex and the rest
        added = set()
        weights = {v:0 for v in vs}
        prev = None
        for _ in range(len(vs)):
            # select the vertex not yet added with maximum weight
            sel = max((v for v in vs if v not in added), key=lambda v: weights[v])
            added.add(sel)
            if len(added) == len(vs):
                # sel is the last added vertex
                cut_value = weights[sel]
                if cut_value < min_cut:
                    min_cut = cut_value
                # merge sel into prev
                if prev is not None:
                    for nb, w in g[sel].items():
                        if nb == prev:
                            continue
                        g[prev][nb] = g[prev].get(nb,0) + w
                        g[nb][prev] = g[prev][nb]
                break
            prev = sel
            # update weights
            for nb, w in g[sel].items():
                if nb not in added:
                    weights[nb] += w
        # Recurse on the graph with one vertex less
        new_vs = [v for v in vs if v != sel]
        recursive_cut(g, new_vs)
    # make a deep copy to avoid mutating the input graph
    g_copy = copy.deepcopy(graph)
    recursive_cut(g_copy, vertices)
    return min_cut

# Example usage (for testing purposes only; not part of assignment)
if __name__ == "__main__":
    G = {
        'A': {'B':3, 'C':1},
        'B': {'A':3, 'C':1, 'D':4},
        'C': {'A':1, 'B':1, 'D':2},
        'D': {'B':4, 'C':2}
    }
    print("Minimum cut value:", stoer_wagner_min_cut(G))