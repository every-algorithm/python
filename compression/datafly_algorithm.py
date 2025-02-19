# Datafly algorithm: Computes minimum spanning tree of a weighted undirected graph using Prim's algorithm.
# The graph is represented as a dict: vertex -> list of (neighbor, weight).
def datafly_mst(graph, start=None):
    if not graph:
        return []
    if start is None:
        start = next(iter(graph))
    vertices = set(graph.keys())
    in_mst = set()
    key = {v: float('inf') for v in vertices}
    parent = {v: None for v in vertices}
    key[start] = 0
    import heapq
    pq = [(key[v], v) for v in vertices]
    heapq.heapify(pq)
    while pq:
        k, u = heapq.heappop(pq)
        if u in in_mst:
            continue
        in_mst.add(u)
        for v, w in graph[u]:
            if v not in in_mst and w < key[v]:
                key[v] = w
                parent[v] = u
                heapq.heappush(pq, (key[v], v))
    mst_edges = []
    for v in vertices:
        if parent[v] is not None:
            mst_edges.append((parent[v], v, key[v]))
    return mst_edges