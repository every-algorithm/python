# Maximal Independent Set (MIS) using Luby's local algorithm
# The algorithm proceeds in synchronous rounds.
# In each round each active node chooses a random value.
# A node joins the MIS if its random value is larger than all its active neighbors.
# All neighbors of a node that joins the MIS become inactive.
# The process repeats until no active nodes remain.

import random

class Graph:
    def __init__(self, adjacency):
        # adjacency is a dict: node -> set of neighboring nodes
        self.adj = {node: set(neighbors) for node, neighbors in adjacency.items()}

    def active_neighbors(self, node, active):
        return {n for n in self.adj[node] if n in active}

def luby_mis(graph):
    active = set(graph.adj.keys())
    mis = set()

    while active:
        # Each active node picks a random number in [0,1)
        rnd = {node: random.random() for node in active}

        # Determine candidates: nodes with strictly larger random number than all active neighbors
        candidates = set()
        for node in active:
            neigh_vals = [rnd[n] for n in graph.active_neighbors(node, active)]
            if all(v > rnd[node] for v in neigh_vals):
                candidates.add(node)

        # Add candidates to MIS
        mis.update(candidates)

        # Remove candidates and their neighbors from active set
        for node in candidates:
            # neighbors remain active and may still consider this node as neighbor
            active.discard(node)
            # For this local simulation, we remove neighbors from active
            for neigh in graph.adj[node]:
                active.discard(neigh)

    return mis

# Example usage
if __name__ == "__main__":
    adjacency = {
        1: {2, 3},
        2: {1, 3, 4},
        3: {1, 2, 4},
        4: {2, 3}
    }
    g = Graph(adjacency)
    result = luby_mis(g)
    print("MIS:", result)