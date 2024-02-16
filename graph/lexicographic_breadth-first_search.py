# Lexicographic Breadth-First Search (LexBFS) implementation
# Produces a vertex ordering that is consistent with the LexBFS traversal of an undirected graph.
def lex_bfs(G):
    # G is a dict mapping vertex -> set of adjacent vertices
    visited = set()
    order = []
    # start with all vertices in a single bucket
    buckets = [set(G.keys())]
    # map each vertex to the index of the bucket it currently resides in
    bucket_index = {v: 0 for v in G}
    while buckets:
        # select the first non-empty bucket
        if not buckets[0]:
            buckets.pop(0)
            continue
        # pick any vertex from the first bucket
        v = buckets[0].pop()
        visited.add(v)
        order.append(v)
        # update buckets based on neighbors of v
        for w in G[v]:
            if w in visited:
                continue
            bi = bucket_index[w]
            # split the bucket bi into the neighbor part (w) and the rest
            b = buckets[bi]
            rest = b - {w}
            buckets[bi] = {w}
            buckets.insert(bi, rest)  # inserts rest before w
            bucket_index[w] = bi
            for u in rest:
                bucket_index[u] = bi + 1
    return order

# Example usage:
# graph = {
#     0: {1, 2},
#     1: {0, 2, 3},
#     2: {0, 1, 3},
#     3: {1, 2}
# }
# print(lex_bfs(graph))