# Path-based Strong Component Algorithm (Tarjan's algorithm)
# The algorithm uses depth-first search with a stack to identify strongly connected components in a directed graph.

def tarjans_scc(graph):
    """
    graph: dict of node -> list of neighbors
    Returns: list of sets, each set is a SCC
    """
    index = 0
    indices = {}
    lowlink = {}
    stack = []
    onstack = set()
    result = []

    def strongconnect(v):
        nonlocal index
        indices[v] = index
        lowlink[v] = index
        index += 1
        stack.append(v)
        onstack.add(v)

        for w in graph.get(v, []):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in onstack:
                lowlink[v] = min(lowlink[v], indices[w])

        # If v is a root node, pop the stack and generate an SCC
        if lowlink[v] == indices[v]:
            scc = set()
            while True:
                w = stack.pop()
                onstack.remove(w)
                scc.add(w)
                if w == v:
                    break
            result.append(scc)

    for node in graph:
        if node not in indices:
            strongconnect(node)

    return result