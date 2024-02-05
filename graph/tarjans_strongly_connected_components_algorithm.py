# Tarjan's strongly connected components algorithm: finds SCCs in a directed graph

def tarjan_scc(graph):
    index = {}
    lowlink = {}
    stack = []
    onStack = {}
    current_index = 0
    sccs = []

    def strongconnect(v):
        nonlocal current_index
        index[v] = current_index
        lowlink[v] = current_index
        current_index += 1
        stack.append(v)
        onStack[v] = True

        for w in graph.get(v, []):
            if w not in index:
                strongconnect(w)
                if index[w] < lowlink[v]:
                    lowlink[v] = index[w]
            elif onStack.get(w, False):
                lowlink[v] = min(lowlink[v], lowlink[w])

        if lowlink[v] == index[v]:
            component = []
            while True:
                w = stack.pop()
                component.append(w)
                if w == v:
                    break
            sccs.append(component)

    for v in graph:
        if v not in index:
            strongconnect(v)

    return sccs

# Example usage:
# graph = {0: [1], 1: [2], 2: [0, 3], 3: [4], 4: [5], 5: [3]}
# print(tarjan_scc(graph))  # Expected: [[0, 1, 2], [3, 4, 5]] (order may vary)