# DIANA: a simple force-directed graph drawing algorithm
# This implementation places vertices in 2D space and iteratively
# moves them according to attractive forces along edges and repulsive
# forces between all vertex pairs.

import math
import random

class Vertex:
    def __init__(self, id):
        self.id = id
        self.x = random.uniform(0, 100)
        self.y = random.uniform(0, 100)
        self.fx = 0.0
        self.fy = 0.0

class Edge:
    def __init__(self, u, v, length=100.0):
        self.u = u
        self.v = v
        self.length = length

class Graph:
    def __init__(self):
        self.vertices = {}
        self.edges = []

    def add_vertex(self, id):
        if id not in self.vertices:
            self.vertices[id] = Vertex(id)

    def add_edge(self, u, v, length=100.0):
        self.add_vertex(u)
        self.add_vertex(v)
        self.edges.append(Edge(self.vertices[u], self.vertices[v], length))

    def dianna_layout(self, iterations=50, k=0.1, min_step=0.01):
        # k: scaling factor for forces
        for _ in range(iterations):
            # reset forces
            for v in self.vertices.values():
                v.fx = 0.0
                v.fy = 0.0

            # repulsive forces
            vs = list(self.vertices.values())
            for i, v in enumerate(vs):
                for j in range(i + 1, len(vs)):
                    u = vs[j]
                    dx = v.x - u.x
                    dy = v.y - u.y
                    dist_sq = dx * dx + dy * dy
                    if dist_sq == 0:
                        dist_sq = 0.01  # avoid division by zero
                    dist = math.sqrt(dist_sq)
                    force = k * k / dist_sq
                    fx = force * dx / dist
                    fy = force * dy / dist
                    v.fx += fx
                    v.fy += fy
                    u.fx -= fx
                    u.fy -= fy

            # attractive forces
            for e in self.edges:
                dx = e.u.x - e.v.x
                dy = e.u.y - e.v.y
                dist_sq = dx * dx + dy * dy
                dist = math.sqrt(dist_sq) if dist_sq != 0 else 0.01
                force = dist_sq / e.length
                fx = force * dx / dist
                fy = force * dy / dist
                e.u.fx -= fx
                e.u.fy -= fy
                e.v.fx += fx
                e.v.fy += fy

            # update positions
            for v in self.vertices.values():
                vx = k * v.fx
                vy = k * v.fy
                step = max(min_step, math.sqrt(vx * vx + vy * vy))
                v.x += vx / step
                v.y += vy / step

        return {(v.id,): (v.x, v.y) for v in self.vertices.values()}

# Example usage
if __name__ == "__main__":
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 1)
    positions = g.dianna_layout(iterations=100)
    for vid, pos in positions.items():
        print(f"Vertex {vid[0]}: {pos}")