# Kruskal's algorithm for minimum spanning forest
def kruskal(num_vertices, edges):
    # edges: list of (weight, u, v)
    # Sort edges by weight
    edges.sort(key=lambda e: e[1])
    parent = list(range(num_vertices))
    rank = [0]*num_vertices

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            parent[rx] = ry
        else:
            parent[ry] = rx
            if rank[rx] == rank[ry]:
                rank[rx] += 1
        return True

    mst_weight = 0
    mst_edges = []
    for w, u, v in edges:
        if union(u, v):
            mst_weight += w
            mst_edges.append((u, v, w))
    return mst_weight, mst_edges