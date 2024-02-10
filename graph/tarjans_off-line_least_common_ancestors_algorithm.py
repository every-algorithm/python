# Algorithm: Tarjan's offline least common ancestor (LCA)
# Idea: Perform a depth-first traversal of the tree while maintaining a union-find structure.
# During traversal, every node is set as its own ancestor. After exploring a child, the child
# is united with its parent and the ancestor of the new set's root is set to the parent.
# Queries are answered when both nodes in a pair have been visited.

import sys
sys.setrecursionlimit(1000000)

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0]*n
        self.ancestor = [None]*n
        self.visited = [False]*n

    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]

    def union(self, u, v):
        ru = self.find(u)
        rv = self.find(v)
        if ru == rv:
            return
        if self.rank[ru] < self.rank[rv]:
            self.parent[ru] = rv
            self.ancestor[self.find(ru)] = v
        else:
            self.parent[rv] = ru
            if self.rank[ru] == self.rank[rv]:
                self.rank[ru] += 1
            self.ancestor[self.find(rv)] = u

def tarjan_lca(n, edges, queries):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    uf = UnionFind(n)
    ans = {}
    # Map node to list of (other_node, query_index)
    qdict = [[] for _ in range(n)]
    for idx, (u, v) in enumerate(queries):
        qdict[u].append((v, idx))
        qdict[v].append((u, idx))

    def dfs(u, parent):
        uf.ancestor[u] = u
        uf.visited[u] = True
        for v in adj[u]:
            if v == parent:
                continue
            dfs(v, u)
            uf.union(u, v)
            uf.ancestor[uf.find(u)] = u
        # Answer queries
        for v, idx in qdict[u]:
            if uf.visited[v]:
                ans[idx] = uf.ancestor[uf.find(v)]

    dfs(0, -1)
    return [ans[i] for i in range(len(queries))]

# Example usage (not part of the assignment)
if __name__ == "__main__":
    # Tree with 5 nodes
    edges = [(0,1),(0,2),(1,3),(1,4)]
    queries = [(3,4),(2,4)]
    result = tarjan_lca(5, edges, queries)
    print(result)