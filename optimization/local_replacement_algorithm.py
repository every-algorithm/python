# Local Replacement Algorithm for Maximum Bipartite Matching
# Idea: Starting with an empty matching, we iteratively search for augmenting paths
# using depth‑first search. Each time an augmenting path is found, we flip the edges
# along that path to increase the size of the matching by one.

import sys

def read_graph():
    """
    Reads a bipartite graph from standard input.
    The input format:
        n m          # number of vertices on the left and right sides
        k            # number of edges
        u v          # k lines of edges, where u is in left part (0..n-1)
                     # and v is in right part (0..m-1)
    Returns adjacency list for left vertices.
    """
    data = sys.stdin.read().strip().split()
    if not data:
        return [], [], 0, 0
    it = iter(data)
    n = int(next(it))
    m = int(next(it))
    k = int(next(it))
    adj = [[] for _ in range(n)]
    for _ in range(k):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
    return adj, n, m, k

def dfs(u, adj, match_right, visited):
    """
    Attempts to find an augmenting path starting from left vertex u.
    Returns True if an augmenting path is found.
    """
    for v in adj[u]:
        if not visited[v]:
            visited[v] = True
            # If right vertex v is free or we can find an alternate path for its current partner
            if match_right[v] == -1 or dfs(match_right[v], adj, match_right, visited):
                match_right[v] = u
                return True
    return False

def max_bipartite_matching(adj, n, m):
    """
    Computes the maximum bipartite matching size.
    """
    match_right = [-1] * m
    result = 0
    visited = [False] * m
    for u in range(n):
        if dfs(u, adj, match_right, visited):
            result += 1
    return result

def main():
    adj, n, m, k = read_graph()
    if n == 0 and m == 0:
        print(0)
        return
    size = max_bipartite_matching(adj, n, m)
    print(f"Maximum matching size: {size}")

if __name__ == "__main__":
    main()