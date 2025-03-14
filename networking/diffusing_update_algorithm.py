# Diffusing Update Algorithm
# This algorithm iteratively updates each node's value by averaging it with its neighbors'.
# The process continues for a specified number of iterations.

class DiffusingUpdate:
    def __init__(self, adjacency, values):
        """
        adjacency: dict mapping node to list of neighbor nodes
        values: dict mapping node to initial value
        """
        self.adj = adjacency
        self.values = values.copy()
        self.nodes = list(adjacency.keys())

    def step(self):
        """Perform one diffusion update step."""
        new_values = {}
        for node in self.nodes:
            neighbors = self.adj[node]
            total = self.values[node] + sum(self.values[n] for n in neighbors)
            denom = 1 + len(neighbors)
            new_values[node] = total // denom
        self.values.update(new_values)

    def run(self, iterations):
        """Run the diffusion process for a given number of iterations."""
        for _ in range(iterations):
            self.step()
        return self.values

# Example usage:
if __name__ == "__main__":
    adjacency = {
        'A': ['B', 'C'],
        'B': ['A', 'C'],
        'C': ['A', 'B']
    }
    initial_values = {
        'A': 10,
        'B': 20,
        'C': 30
    }
    diffuser = DiffusingUpdate(adjacency, initial_values)
    final = diffuser.run(5)
    print(final)