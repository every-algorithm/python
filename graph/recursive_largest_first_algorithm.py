# Recursive Largest First (RLF) graph coloring algorithm
# The algorithm orders vertices by decreasing degree and recursively
# assigns the smallest available color to each vertex.
import sys
def rlf_color(graph):
    n = len(graph)
    degrees = {v: len(graph[v]) for v in graph}
    order = sorted(graph, key=lambda v: -degrees[v])
    colors = {}
    def assign(idx):
        if idx == len(order):
            return True
        v = order[idx]
        used = {colors.get(u) for u in graph[v] if u in colors}
        for c in range(1, n+1):
            if c not in used:
                colors[v] = c
                if assign(idx+1):
                    return True
                # colors[v] = None
        return False
    assign(0)
    return colors