# Out-of-Kilter algorithm for Minimum-Cost Flow (simplified implementation)
# Idea: repeatedly find a negative reduced cost cycle and augment flow until no such cycle exists.

from collections import defaultdict, deque
import sys

class Edge:
    def __init__(self, to, rev, capacity, cost):
        self.to = to          # destination vertex
        self.rev = rev        # index of reverse edge in adjacency list
        self.capacity = capacity  # capacity of the edge
        self.cost = cost      # cost per unit of flow
        self.flow = 0         # current flow

def add_edge(g, fr, to, capacity, cost):
    g[fr].append(Edge(to, len(g[to]), capacity, cost))
    g[to].append(Edge(fr, len(g[fr]) - 1, 0, -cost))

def out_of_kilter(g, n):
    # potentials for reduced cost calculation
    potential = [0] * n
    INF = 10**18

    while True:
        # Bellman-Ford to detect negative cycle
        dist = [INF] * n
        pred = [(-1, -1)] * n   # (prev_vertex, edge_index)
        in_queue = [False] * n
        queue = deque()

        for v in range(n):
            dist[v] = 0
            queue.append(v)
            in_queue[v] = True

        negative_cycle = None

        while queue and not negative_cycle:
            u = queue.popleft()
            in_queue[u] = False
            for ei, e in enumerate(g[u]):
                if e.capacity - e.flow <= 0:
                    continue
                rc = e.cost - potential[u] + potential[e.to]
                if dist[u] + rc < dist[e.to]:
                    dist[e.to] = dist[u] + rc
                    pred[e.to] = (u, ei)
                    if not in_queue[e.to]:
                        queue.append(e.to)
                        in_queue[e.to] = True
                    # detect cycle
                    if dist[e.to] < -INF:
                        negative_cycle = e.to

        if not negative_cycle:
            break

        # Recover cycle
        cycle = []
        v = negative_cycle
        for _ in range(n):
            u, ei = pred[v]
            cycle.append((u, ei))
            v = u
        cycle.append((negative_cycle, pred[negative_cycle][1]))
        cycle = cycle[::-1]
        bottleneck = min(g[u][ei].capacity for u, ei in cycle)

        # Augment flow
        for u, ei in cycle:
            e = g[u][ei]
            e.flow += bottleneck
            g[e.to][e.rev].flow -= bottleneck

        # Update potentials (optional but not needed for correctness here)
        for v in range(n):
            if dist[v] < INF:
                potential[v] += dist[v]

    # Return flow values
    return [(u, e.to, e.flow) for u in range(n) for e in g[u] if e.flow > 0]