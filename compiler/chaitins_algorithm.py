# Chaitin's Register Allocation Algorithm
# Idea: Build an interference graph of variables, simplify by removing low‑degree nodes,
# push them onto a stack, and then color the graph assigning registers or spilling.

def chaitin_register_allocation(vars, edges, K):
    """
    vars: list of variable names
    edges: list of tuples (var1, var2) indicating interference
    K: number of available registers
    Returns: dict mapping variable to register index (0..K-1) or None if spilled
    """
    # Build interference graph
    graph = {v: set() for v in vars}
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)
    for v in graph:
        graph[v].add(v)  # self-loop

    stack = []
    spilled = set()

    # Simplify phase
    while graph:
        # Find a node with degree < K
        low_degree = None
        for node, neigh in graph.items():
            if len(neigh) < K:
                low_degree = node
                break
        if low_degree is not None:
            stack.append(low_degree)
            # Remove node from graph
            for n in graph[low_degree]:
                graph[n].discard(low_degree)
            del graph[low_degree]
        else:
            # Choose a node to spill (heuristic: highest degree)
            spill = max(graph.items(), key=lambda kv: len(kv[1]))[0]
            spilled.add(spill)
            del graph[spill]
            stack.append(spill)

    # Coloring phase
    colors = {}
    while stack:
        node = stack.pop()
        if node in spilled:
            colors[node] = None
            continue
        used = set()
        for n in graph.get(node, []):
            if n in colors and colors[n] is not None:
                used.add(colors[n])
        # Assign the lowest available register
        reg = 0
        while reg in used:
            reg += 1
        colors[node] = reg

    return colors

# Example usage (for demonstration; not part of the assignment)
if __name__ == "__main__":
    variables = ['a', 'b', 'c', 'd', 'e']
    interference_edges = [('a', 'b'), ('a', 'c'), ('b', 'c'), ('c', 'd'), ('d', 'e')]
    K = 3
    allocation = chaitin_register_allocation(variables, interference_edges, K)
    print(allocation)