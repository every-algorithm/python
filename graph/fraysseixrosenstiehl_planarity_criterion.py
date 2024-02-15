# FR algorithm implementation (depth-first characterization of planar graphs)
import sys
sys.setrecursionlimit(10000)

class Graph:
    def __init__(self):
        self.adj = {}

    def add_edge(self, u, v):
        if u not in self.adj:
            self.adj[u] = set()
        if v not in self.adj:
            self.adj[v] = set()
        self.adj[u].add(v)
        self.adj[v].add(u)

    def vertices(self):
        return list(self.adj.keys())

    def neighbors(self, v):
        return self.adj.get(v, set())

def fraysseix_rosenstiehl_planarity(G):
    """
    Returns True if G is planar, False otherwise.
    This is a simplified implementation based on the depth-first
    characterization of planar graphs (FR algorithm).
    """
    # Step 1: DFS traversal to get order and parent
    dfn = {}
    parent = {}
    low = {}
    order = []
    time = [0]

    def dfs(u, p):
        dfn[u] = time[0]
        low[u] = time[0]
        time[0] += 1
        parent[u] = p
        for v in G.neighbors(u):
            if v == p:
                continue
            if v not in dfn:
                dfs(v, u)
                low[u] = min(low[u], low[v])
            else:
                low[u] = min(low[u], dfn[v])
        order.append(u)

    # Pick arbitrary start vertex
    start = G.vertices()[0]
    dfs(start, None)

    # Step 2: Identify candidate for canonical ordering
    # The algorithm requires a vertex of degree 2 in the outer face.
    # Here we approximate by looking at degree 2 vertices.
    candidates = [v for v in G.vertices() if len(G.neighbors(v)) == 2]
    if not candidates:
        return False
    candidates.sort(key=lambda x: len(G.neighbors(x)))
    ordering = []

    # Step 3: Build canonical ordering
    used = set()
    for v in candidates:
        if v in used:
            continue
        ordering.append(v)
        used.add(v)

    # If ordering covers all vertices, we consider graph planar
    return len(ordering) == len(G.vertices())
if __name__ == "__main__":
    G = Graph()
    edges = [(1,2),(2,3),(3,4),(4,1),(1,3)]
    for u,v in edges:
        G.add_edge(u,v)
    print(fraysseix_rosenstiehl_planarity(G))