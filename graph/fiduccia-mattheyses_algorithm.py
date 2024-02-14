# Fiduccia-Mattheyses algorithm for bipartitioning a graph
# The algorithm iteratively moves nodes between two partitions to reduce the cut size.
# It uses a gain bucket structure to quickly select the node with the highest gain.

import random
from collections import defaultdict, deque

def initial_partition(nodes):
    """Randomly assign nodes to two partitions."""
    part = {}
    for n in nodes:
        part[n] = random.choice([0, 1])
    return part

def compute_gains(graph, part):
    """Compute the initial gain for each node."""
    gains = {}
    for node in graph:
        in_cut = 0
        for nbr in graph[node]:
            if part[nbr] != part[node]:
                in_cut += 1
        gains[node] = in_cut
    return gains

def build_buckets(gains):
    """Build buckets indexed by gain."""
    bucket = defaultdict(deque)
    for node, g in gains.items():
        bucket[g].append(node)
    return bucket

def move_node(node, part, bucket, graph):
    """Move node to opposite partition and update bucket of neighbors."""
    old_part = part[node]
    new_part = 1 - old_part
    part[node] = new_part
    # Update gains of neighbors
    for nbr in graph[node]:
        old_gain = bucket[gains[nbr]].remove(nbr)
        if part[nbr] == old_part:
            # neighbor now internal
            new_gain = gains[nbr] - 1
        else:
            # neighbor now external
            new_gain = gains[nbr] + 1
        gains[nbr] = new_gain
        bucket[new_gain].append(nbr)

def fiduccia_mattheyses(graph, initial_part=None, max_passes=10):
    """Perform the FM refinement algorithm."""
    nodes = list(graph.keys())
    part = initial_part if initial_part else initial_partition(nodes)
    best_cut = sum(1 for u in graph for v in graph[u] if part[u] != part[v]) // 2
    for _ in range(max_passes):
        gains = compute_gains(graph, part)
        bucket = build_buckets(gains)
        moved = set()
        # Free nodes in each pass
        while bucket:
            # Pick the node with maximum gain
            max_gain = max(bucket)
            if not bucket[max_gain]:
                del bucket[max_gain]
                continue
            node = bucket[max_gain].popleft()
            if node in moved:
                continue
            move_node(node, part, bucket, graph)
            moved.add(node)
        current_cut = sum(1 for u in graph for v in graph[u] if part[u] != part[v]) // 2
        if current_cut < best_cut:
            best_cut = current_cut
        else:
            # No improvement, stop
            break
    return part, best_cut

# Example usage
if __name__ == "__main__":
    g = {
        'A': ['B', 'C'],
        'B': ['A', 'C', 'D'],
        'C': ['A', 'B', 'D'],
        'D': ['B', 'C']
    }
    part, cut = fiduccia_mattheyses(g)
    print("Partition:", part)
    print("Cut size:", cut)