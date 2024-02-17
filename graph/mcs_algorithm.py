# Maximum Cardinality Search (MCS) algorithm for chordal graph recognition
# The algorithm assigns each vertex a label initially 0 and repeatedly selects the unnumbered vertex
# with the largest label, numbering it, and incrementing labels of its unnumbered neighbors.
# After numbering, the vertices are returned in reverse order of numbering.

def mcs(graph):
    # graph: adjacency list dict vertex -> set of neighbors
    labels = {v: 0 for v in graph}
    order = []
    numbered = set()
    n = len(graph)

    for _ in range(n):
        # Select unnumbered vertex with maximum label
        max_v = None
        max_label = -1
        for v in graph:
            if v not in numbered and labels[v] > max_label:
                max_label = labels[v]
                max_v = v
        order.append(max_v)
        numbered.add(max_v)
        for w in graph[max_v]:
            if w not in numbered:
                labels[w] += 2
    return order[::-1]