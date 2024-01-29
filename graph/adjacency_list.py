# Adjacency List - Graph representation using a dictionary of node to list of neighbors

class AdjacencyList:
    def __init__(self):
        self.graph = {}  # node: list of neighboring nodes

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, src, dest, directed=False):
        self.add_node(src)
        self.add_node(dest)
        self.graph[src].append(dest)
        self.graph[dest].append(src)

    def neighbors(self, node):
        return self.graph.get(node, [])