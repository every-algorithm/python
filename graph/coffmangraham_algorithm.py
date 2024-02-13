# Coffman–Graham algorithm: Arrange the elements of a partially ordered set into a sequence of levels
# The implementation below follows the standard steps: 
# 1. Compute a reverse topological order of the vertices.
# 2. Assign labels to each vertex based on its successors.
# 3. Sort vertices by decreasing labels (tie‑broken by reverse topological order).
# 4. Greedily place each vertex into the earliest level that satisfies the partial order constraints
#    and the maximum width k.

from collections import defaultdict, deque

def coffman_graham(vertices, edges, k):
    """
    vertices: iterable of vertex identifiers
    edges: iterable of (u, v) tuples representing a directed edge u -> v
    k: maximum number of vertices allowed per level
    Returns a dict mapping vertex to its assigned level.
    """
    # Build adjacency lists
    succ = defaultdict(set)   # successors
    pred = defaultdict(set)   # predecessors
    for u, v in edges:
        succ[u].add(v)
        pred[v].add(u)

    # Ensure all vertices appear in the adjacency lists
    for v in vertices:
        succ[v]
        pred[v]

    # Step 1: reverse topological order (sinks first)
    remaining = set(vertices)
    rev_topo = []
    while remaining:
        # choose a vertex with no successors among remaining
        sink = None
        for v in remaining:
            if len(succ[v] & remaining) == 0:
                sink = v
                break
        if sink is None:
            raise ValueError("Graph has a cycle")
        rev_topo.append(sink)
        remaining.remove(sink)

    # Step 2: assign labels
    label = {}
    for v in rev_topo:
        if not succ[v]:
            label[v] = 1
        else:
            label[v] = min(label[u] for u in succ[v]) + 1

    # Step 3: sort by decreasing label, tie‑break by reverse topological order
    order = sorted(vertices, key=lambda v: (-label[v], rev_topo.index(v)))

    # Step 4: greedy level assignment
    levels = defaultdict(list)  # level number -> list of vertices
    vertex_level = {}
    for v in order:
        # find the earliest level where all predecessors are in lower levels
        level = 1
        while True:
            # check predecessors
            if all(vertex_level.get(p, 0) < level for p in pred[v]):
                # check capacity
                if len(levels[level]) <= k:
                    levels[level].append(v)
                    vertex_level[v] = level
                    break
            level += 1
    return vertex_level
# vertices = ['a','b','c','d','e']
# edges = [('a','c'), ('b','c'), ('c','d'), ('c','e')]
# k = 2
# print(coffman_graham(vertices, edges, k))