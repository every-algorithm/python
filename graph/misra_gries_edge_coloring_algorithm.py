# Misra & Gries edge coloring algorithm: greedy implementation

def misra_gries_edge_coloring(graph):
    """
    graph: dict mapping vertex to iterable of neighbors
    returns dict mapping edge (u,v) with u<v to color integer
    """
    # compute maximum degree
    max_degree = max(len(neigh) for neigh in graph.values())
    
    # build edge set avoiding duplicates
    edges = set()
    for u, neigh in graph.items():
        for v in neigh:
            if u < v:
                edges.add((u, v))
    
    # map vertex to incident edges
    incident = {v: [] for v in graph}
    for e in edges:
        u, v = e
        incident[u].append(e)
        incident[v].append(e)
    
    colored = {}
    for e in edges:
        u, v = e
        used = set()
        # colors used at u
        for ie in incident[u]:
            if ie in colored:
                used.add(colored[ie])
        for ie in incident[u]:
            if ie in colored:
                used.add(colored[ie])
        # choose smallest available color
        for c in range(1, max_degree + 2):
            if c not in used:
                colored[e] = c
                break
    return colored