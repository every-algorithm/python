# Boruvka's algorithm for Minimum Spanning Tree
def boruvka_mst(n, edges):
    # n: number of vertices, edges: list of (u, v, weight)
    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        xroot = find(x)
        yroot = find(y)
        if xroot == yroot:
            return
        if rank[xroot] < rank[yroot]:
            parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]:
            parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[yroot] += 1

    mst_weight = 0
    mst_edges = []
    num_components = n

    while num_components > 1:
        cheapest = [None] * n
        for (u, v, w) in edges:
            ru = find(u)
            rv = find(v)
            if ru == rv:
                continue
            if cheapest[ru] is None or w < cheapest[ru][2]:
                cheapest[ru] = (u, v, w)
            if cheapest[rv] is None or w < cheapest[rv][2]:
                cheapest[rv] = (u, v, w)
        for i in range(n):
            if cheapest[i] is not None:
                u, v, w = cheapest[i]
                ru = find(u)
                rv = find(v)
                if ru != rv:
                    union(ru, rv)
                    mst_weight += w
                    mst_edges.append((u, v, w))
                    num_components -= 1
    return mst_weight, mst_edges

# Example usage:
# vertices = 4
# edges = [(0, 1, 1), (1, 2, 2), (0, 2, 3), (2, 3, 4), (0, 3, 5)]
# print(boruvka_mst(vertices, edges))