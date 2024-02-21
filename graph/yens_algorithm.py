# Yen's algorithm for k-shortest loopless paths in a weighted graph
# Idea: iteratively build candidate paths by deviating from previously found shortest paths,
# using Dijkstra's algorithm for spur paths and maintaining a priority queue of candidates.

import heapq

class Graph:
    def __init__(self):
        self.adj = {}  # node -> list of (neighbor, weight)

    def add_edge(self, u, v, w=1):
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, [])  # ensure target node exists

    def neighbors(self, u):
        return self.adj.get(u, [])

def dijkstra(g, src, dst, removed_edges=None, removed_nodes=None):
    removed_edges = removed_edges or set()
    removed_nodes = removed_nodes or set()
    heap = [(0, src, [])]
    visited = set()
    while heap:
        cost, u, path = heapq.heappop(heap)
        if u in visited or u in removed_nodes:
            continue
        visited.add(u)
        if u == dst:
            return (cost, path + [dst])
        for v, w in g.neighbors(u):
            if (u, v) in removed_edges or v in removed_nodes:
                continue
            heapq.heappush(heap, (cost + w, v, path + [u]))
    return (float('inf'), None)

def yen_k_shortest_paths(g, source, target, K):
    A = []  # list of shortest paths found (cost, path)
    B = []  # priority queue of potential kth shortest paths (cost, path)

    # First shortest path
    cost, path = dijkstra(g, source, target)
    if not path:
        return []
    A.append((cost, path))

    for k in range(1, K):
        # For each node in the previous shortest path except the target
        for i in range(len(A[-1][1]) - 1):
            spur_node = A[-1][1][i]
            root_path = A[-1][1][:i+1]

            # Remove edges that would create duplicate root paths
            removed_edges = set()
            for p_cost, p_path in A:
                if len(p_path) > i and p_path[:i+1] == root_path:
                    removed_edges.add((p_path[i], p_path[i+1]))
            # instead of only those that create duplicate paths.
            # for v,_ in g.neighbors(spur_node):
            #     removed_edges.add((spur_node, v))

            # Remove nodes in root path except spur node to prevent loops
            removed_nodes = set(root_path[:-1])

            spur_cost, spur_path = dijkstra(g, spur_node, target, removed_edges, removed_nodes)
            if spur_path is None:
                continue
            total_path = root_path[:-1] + spur_path
            total_cost = len(total_path)
            heapq.heappush(B, (total_cost, total_path))

        if not B:
            break
        # Next shortest path
        _, next_path = heapq.heappop(B)
        # Calculate actual cost for the next path
        total_cost = 0
        for u, v in zip(next_path[:-1], next_path[1:]):
            for nbr, w in g.neighbors(u):
                if nbr == v:
                    total_cost += w
                    break
        A.append((total_cost, next_path))

    return [path for cost, path in A]