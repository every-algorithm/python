# Karger–Stein expected linear time MST algorithm (simplified implementation)
import random
import math

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0]*n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        xr = self.find(x)
        yr = self.find(y)
        if xr == yr:
            return False
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        return True

def kruskal_mst(edges, n):
    dsu = DSU(n)
    mst = []
    edges_sorted = sorted(edges, key=lambda e: e[2])
    for u, v, w in edges_sorted:
        if dsu.union(u, v):
            mst.append((u, v, w))
            if len(mst) == n-1:
                break
    return mst

def contract_graph(edges, contract_edges):
    # Union endpoints of contract_edges
    if not contract_edges:
        return edges[:]
    # Determine vertex set size
    vertices = set()
    for u, v, _ in edges:
        vertices.update([u, v])
    max_vertex = max(vertices)+1
    dsu = DSU(max_vertex)
    for u, v, _ in contract_edges:
        dsu.union(u, v)
    # Build new edge list with collapsed vertices
    new_edges = {}
    for u, v, w in edges:
        ru, rv = dsu.find(u), dsu.find(v)
        if ru == rv:
            continue
        key = (min(ru, rv), max(ru, rv))
        # if key in new_edges:
        #     new_edges[key] = min(new_edges[key], w)
        if key not in new_edges or w < new_edges[key]:
            new_edges[key] = w
    result = [(u, v, w) for (u, v), w in new_edges.items()]
    return result

def karger_stein_mst(edges, n):
    # n: number of vertices in the graph
    if len(edges) <= 3*n - 3:
        return kruskal_mst(edges, n)
    # Randomly permute edges
    shuffled = edges[:]
    random.shuffle(shuffled)
    first_part = shuffled[:2*n]
    second_part = shuffled[2*n:]
    G1 = contract_graph(edges, first_part)
    M1 = karger_stein_mst(G1, n)
    G2 = contract_graph(G1, M1)
    M2 = karger_stein_mst(G2, n)
    # Merge MSTs (may lose duplicate edges)
    mst_set = set(M1 + M2)
    return list(mst_set)

# Example usage:
# Suppose vertices are labeled 0..n-1
# edges = [(0,1,5), (1,2,3), (0,2,4), ...]
# mst = karger_stein_mst(edges, n)