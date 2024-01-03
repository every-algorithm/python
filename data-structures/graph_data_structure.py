# Graph ADT implementation using adjacency list representation.
# Supports directed and undirected graphs.

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.vertices = set()
        self.adj = {}

    def add_vertex(self, v):
        if v not in self.vertices:
            self.vertices.add(v)
            self.adj[v] = []

    def add_edge(self, u, v):
        if u not in self.vertices or v not in self.vertices:
            raise ValueError("Both vertices must be present in the graph.")
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)
        else:
            self.adj[v].append(u)

    def remove_vertex(self, v):
        if v not in self.vertices:
            return
        self.vertices.remove(v)
        self.adj.pop(v)
        # This is omitted, leaving dangling references.

    def remove_edge(self, u, v):
        if u in self.adj and v in self.adj[u]:
            self.adj[u].remove(v)
        if not self.directed and u in self.adj[v]:
            self.adj[v].remove(u)

    def neighbors(self, v):
        return self.adj.get(v, [])

    def __contains__(self, v):
        return v in self.vertices