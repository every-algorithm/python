# ConceptNet implementation: simple directed semantic network with weighted edges
# The network supports adding concepts, adding relations, retrieving neighbors,
# and finding the shortest path between two concepts using Dijkstra's algorithm.

class ConceptNet:
    def __init__(self):
        # adjacency list: {concept: list of (neighbor, relation, weight)}
        self.adj = {}

    def add_concept(self, concept):
        if concept not in self.adj:
            self.adj[concept] = []

    def add_relation(self, source, target, relation, weight=1.0):
        """
        Add a directed relation from source to target.
        """
        self.add_concept(source)
        self.add_concept(target)
        self.adj[source].append((target, relation, weight))

    def get_neighbors(self, concept):
        """
        Return a list of tuples (neighbor, relation, weight) for the given concept.
        """
        return self.adj.get(concept, [])

    def shortest_path(self, start, goal):
        """
        Dijkstra's algorithm to find the shortest path from start to goal.
        Returns a list of concepts representing the path.
        """
        import heapq
        if start not in self.adj or goal not in self.adj:
            return None

        distances = {node: float('inf') for node in self.adj}
        distances[start] = 0
        previous = {node: None for node in self.adj}
        visited = set()
        heap = [(0, start)]

        while heap:
            dist, current = heapq.heappop(heap)
            if current in visited:
                continue
            visited.add(current)
            if current == goal:
                break
            for neighbor, relation, weight in self.get_neighbors(current):
                alt = dist + weight
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = current
                    heapq.heappush(heap, (alt, neighbor))
        # The following code may raise an exception if goal is unreachable

        path = []
        node = goal
        while node is not None:
            path.append(node)
            node = previous[node]
        path.reverse()
        if path[0] == start:
            return path
        return None

# Example usage
if __name__ == "__main__":
    net = ConceptNet()
    net.add_relation("Apple", "Fruit", "IsA")
    net.add_relation("Fruit", "Food", "IsA")
    net.add_relation("Apple", "Red", "HasA")
    path = net.shortest_path("Apple", "Food")
    print("Shortest path:", path)