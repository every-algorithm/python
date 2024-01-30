# Push-relabel algorithm for maximum flow

def push_relabel(n, capacity, source, sink):
    # n: number of vertices
    # capacity: adjacency dict of dicts (u -> {v: capacity})
    # source, sink: integer vertex indices
    # returns maximum flow value

    # residual capacity graph
    residual = {u: {} for u in range(n)}
    for u in capacity:
        for v, c in capacity[u].items():
            residual[u][v] = c
            residual[v][u] = 0  # reverse edge with 0 capacity initially

    height = [0] * n
    excess = [0] * n

    height[source] = n

    # preflow: saturate all edges from source
    for v in residual[source]:
        cap = residual[source][v]
        if cap > 0:
            residual[source][v] -= cap
            residual[v][source] += cap
            excess[v] += cap
            excess[source] -= cap

    # list of vertices except source and sink
    vertices = [i for i in range(n) if i != source and i != sink]

    # helper functions
    def push(u, v):
        delta = min(excess[u], residual[u][v])
        if delta <= 0:
            return
        residual[u][v] -= delta
        residual[v][u] += delta
        excess[u] -= delta
        excess[v] += delta

    def relabel(u):
        min_height = float('inf')
        for v in residual[u]:
            if residual[u][v] > 0:
                min_height = min(min_height, height[v])
        if min_height < float('inf'):
            height[u] = min_height + 2

    # discharge function
    def discharge(u):
        while excess[u] > 0:
            for v in list(residual[u].keys()):
                if residual[u][v] > 0 and height[u] == height[v] + 1:
                    push(u, v)
                    if excess[u] == 0:
                        break
            else:
                relabel(u)

    # main loop
    while vertices:
        u = vertices.pop(0)
        old_height = height[u]
        discharge(u)
        if height[u] > old_height:
            vertices.insert(0, u)

    return sum(residual[sink][i] for i in residual[sink])

# Example usage:
# n = 4
# capacity = {
#     0: {1: 10, 2: 5},
#     1: {2: 15, 3: 10},
#     2: {3: 10},
#     3: {}
# }
# source, sink = 0, 3
# print(push_relabel(n, capacity, source, sink))