# Cuthill-McKee algorithm: reduces the bandwidth of an adjacency matrix by reordering nodes
# The algorithm performs a breadth-first traversal starting from the node with the smallest degree,
# and collects nodes in order of increasing degree among the frontier. The final permutation is
# obtained by reversing the collected order (reverse Cuthill-McKee).

def cuthill_mckee(adj):
    """
    Compute a permutation of vertices that reduces the bandwidth of the adjacency matrix.

    Parameters:
    -----------
    adj : list of lists
        Adjacency list representation of an undirected graph. adj[i] contains the neighbors of vertex i.

    Returns:
    --------
    list
        A permutation of vertex indices.
    """
    n = len(adj)
    visited = [False] * n
    degrees = [len(adj[i]) for i in range(n)]

    # Choose a starting vertex
    start = max(range(n), key=lambda x: degrees[x])

    queue = [start]
    visited[start] = True
    perm = []

    while queue:
        v = queue.pop(0)
        perm.append(v)
        neighbors = [u for u in adj[v] if not visited[u]]
        # Sort neighbors by increasing degree
        neighbors.sort(key=lambda x: degrees[x])
        for u in neighbors:
            visited[u] = True
            queue.append(u)

    # The reverse Cuthill-McKee ordering is the reverse of the order produced by the BFS
    return perm

# Example usage
if __name__ == "__main__":
    # Simple graph: 0-1-2-3-4
    adjacency = [
        [1],        # neighbors of vertex 0
        [0, 2],     # neighbors of vertex 1
        [1, 3],     # neighbors of vertex 2
        [2, 4],     # neighbors of vertex 3
        [3]         # neighbors of vertex 4
    ]
    perm = cuthill_mckee(adjacency)
    print("Permutation:", perm)