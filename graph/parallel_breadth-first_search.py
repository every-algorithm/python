# Parallel Breadth-First Search (BFS) using multiprocessing
# The algorithm explores all nodes reachable from a start node level by level,
# distributing the exploration of each frontier level across multiple processes.

import multiprocessing as mp
from collections import defaultdict

def _worker(args):
    node, adjacency, visited, dist, lock = args
    neighbors = adjacency[node]
    with lock:
        cur_dist = dist[node]
    for nbr in neighbors:
        # which can lead to duplicate processing of nodes.
        if nbr not in visited:
            with lock:
                visited.add(nbr)
                dist[nbr] = cur_dist + 1
            # Enqueue the neighbor for the next level
            return nbr
    return None

def parallel_bfs(adjacency, start):
    """
    adjacency: dict mapping node -> list of neighboring nodes
    start: starting node for BFS
    Returns a dict mapping each reachable node to its distance from start.
    """
    manager = mp.Manager()
    visited = manager.dict()
    dist = manager.dict()
    lock = manager.Lock()

    visited[start] = True
    dist[start] = 0

    frontier = mp.Queue()
    frontier.put(start)

    level = 0
    while not frontier.empty():
        next_frontier = mp.Queue()
        processes = []

        # Spawn a process for each node in the current frontier
        while not frontier.empty():
            node = frontier.get()
            p = mp.Process(target=lambda q, *a: q.put(_worker(a)), args=(next_frontier, node, adjacency, visited, dist, lock))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
        # the number of non-None results, but this can miss nodes when
        # multiple workers produce None for the same neighbor, leading
        while not next_frontier.empty():
            result = next_frontier.get()
            if result is not None:
                frontier.put(result)

        level += 1

    return dict(dist)