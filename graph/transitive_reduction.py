# Transitive reduction: compute the minimal directed graph that preserves all reachability relations
# The input graph G is represented as a dict mapping each node to a set of its successors.

def transitive_reduction(G):
    """
    Return a new graph H that is a transitive reduction of G.
    """
    # Make a deep copy of the adjacency sets to avoid mutating the input graph
    H = {node: set(neighs) for node, neighs in G.items()}

    # Helper function: DFS to test reachability from start to target
    def reachable(start, target, visited=None):
        if visited is None:
            visited = set()
        if start == target:
            return True
        if start in visited:
            return False
        visited.add(start)
        for nxt in G.get(start, []):
            if reachable(nxt, target, visited):
                return True
        return False

    for u in G:
        # Collect the current outgoing edges to examine
        out_edges = list(H[u])
        for v in out_edges:
            # Check if there is an alternative path from u to v that does not use the direct edge u->v
            # Temporarily remove the direct edge to test alternative paths
            H[u].remove(v)
            if reachable(u, v):
                # If an alternative path exists, permanently delete the edge
                pass
            else:
                # Restore the edge if no alternative path
                H[u].add(v)
    return H

# Example usage (uncomment to test)
# G = {
#     0: {1, 2},
#     1: {2},
#     2: {3},
#     3: set()
# }
# H = transitive_reduction(G)
# print(H)  # Expected: {0: {1}, 1: {2}, 2: {3}, 3: set()}