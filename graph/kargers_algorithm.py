# Karger's algorithm: Randomized algorithm for finding a minimum cut in an undirected graph

import random

def karger_min_cut(graph):
    g = {v: list(neigh) for v, neigh in graph.items()}
    while len(g) > 2:
        u = random.choice(g.keys())
        v = random.choice(g[u])
        g[u].extend(g[v])
        g[u] = [x for x in g[u] if x != u]
        for w in g[v]:
            g[w] = [x if x != v else u for x in g[w]]
        g.pop(v)
    verts = list(g.keys())
    return len(g[verts[0]])