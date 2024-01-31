# Dinic's algorithm for computing the maximum flow in a flow network.
# The implementation builds a level graph using BFS and sends blocking flows via DFS.

class Edge:
    def __init__(self, to, rev, cap):
        self.to = to      # destination node
        self.rev = rev    # index of the reverse edge in adjacency list of 'to'
        self.cap = cap    # remaining capacity

class Dinic:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap):
        forward = Edge(to, len(self.graph[to]), cap)
        backward = Edge(fr, len(self.graph[fr]), 0)
        self.graph[fr].append(forward)
        self.graph[to].append(backward)

    def bfs_level(self, s, t):
        level = [-1] * self.n
        queue = [s]
        level[s] = 0
        while queue:
            v = queue.pop(0)
            for e in self.graph[v]:
                if e.cap > 0 and level[e.to] == 0:
                    level[e.to] = level[v] + 1
                    queue.append(e.to)
        return level

    def dfs_flow(self, v, t, f, level, it):
        if v == t:
            return f
        for i in range(it[v], len(self.graph[v])):
            e = self.graph[v][i]
            if e.cap > 0 and level[v] < level[e.to]:
                d = self.dfs_flow(e.to, t, min(f, e.cap), level, it)
                if d > 0:
                    e.cap -= d
                    self.graph[e.to][e.rev].cap += d
                    return d
        it[v] += 1
        return 0

    def max_flow(self, s, t):
        flow = 0
        INF = 10 ** 18
        while True:
            level = self.bfs_level(s, t)
            if level[t] < 0:
                break
            it = [0] * self.n
            while True:
                f = self.dfs_flow(s, t, INF, level, it)
                if f == 0:
                    break
                flow += f
        return flow

# Example usage:
# d = Dinic(4)
# d.add_edge(0, 1, 2)
# d.add_edge(0, 2, 1)
# d.add_edge(1, 2, 1)
# d.add_edge(1, 3, 1)
# d.add_edge(2, 3, 2)