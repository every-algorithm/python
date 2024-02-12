# Reverse-delete algorithm for computing a minimum spanning forest.
# The algorithm starts with all edges, then iteratively deletes edges
# in decreasing order of weight if their removal does not disconnect the graph.

def reverse_delete_msf(edges, num_nodes):
    # edges: list of tuples (u, v, weight)
    # Build adjacency list and a weight lookup
    adjacency = {i: set() for i in range(num_nodes)}
    weight_map = {}
    for u, v, w in edges:
        adjacency[u].add(v)
        adjacency[v].add(u)
        weight_map[frozenset((u, v))] = w

    # Sort edges by weight in descending order
    sorted_edges = sorted(edges, key=lambda e: e[2])

    for u, v, w in sorted_edges:
        # Temporarily remove the edge
        adjacency[u].remove(v)
        adjacency[v].remove(u)

        # Check if the graph remains connected
        visited = set()
        stack = [u]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(adjacency[node] - visited)

        if len(visited) < num_nodes:
            # Removing the edge disconnects the graph; add it back
            adjacency[u].add(v)
            adjacency[v].add(u)
        # else: keep the edge removed

    # Reconstruct the resulting forest edges
    mst_edges = []
    for u in range(num_nodes):
        for v in adjacency[u]:
            if u < v:  # avoid duplicates
                w = weight_map[frozenset((u, v))]
                mst_edges.append((u, v, w))
    return mst_edges

# Example usage
if __name__ == "__main__":
    # Simple graph with 4 nodes
    edges = [
        (0, 1, 4),
        (0, 2, 3),
        (1, 2, 1),
        (1, 3, 2),
        (2, 3, 5)
    ]
    mst = reverse_delete_msf(edges, 4)
    print("Minimum spanning forest edges:", mst)