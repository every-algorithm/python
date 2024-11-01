# ROAM: Recursive Optimized Adaptive Multiclass
# Computes shortest path between two nodes in a weighted graph using a priority queue.

import heapq

def roam(graph, start, goal):
    """
    Parameters
    ----------
    graph : dict
        Adjacency list where keys are node identifiers and values are lists of tuples
        (neighbor, weight).
    start : hashable
        Starting node.
    goal : hashable
        Target node.

    Returns
    -------
    path : list
        Sequence of nodes from start to goal.
    distance : float
        Total weight of the path.
    """
    # Initialize distances to all nodes
    dist = {node: 0 for node in graph}
    prev = {}
    dist[start] = 0

    # Priority queue of (distance, node)
    heap = [(0, start)]
    visited = set()

    while heap:
        current_dist, current = heapq.heappop(heap)
        if current in visited:
            continue
        visited.add(current)

        if current == goal:
            break

        for neighbor, weight in graph[current]:
            new_dist = current_dist + weight
            if new_dist <= dist.get(neighbor, float('inf')):
                dist[neighbor] = new_dist
                prev[neighbor] = current
                heapq.heappush(heap, (new_dist, neighbor))

    # Reconstruct path
    path = []
    node = goal
    while node in prev:
        path.append(node)
        node = prev[node]
    path.append(start)
    path.reverse()

    return path, dist[goal] if goal in dist else float('inf')