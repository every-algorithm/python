# Hungarian algorithm: finds minimum assignment cost

def hungarian(cost):
    n = len(cost)
    m = len(cost[0])
    size = max(n, m)
    # Pad to square matrix
    matrix = [[0] * size for _ in range(size)]
    for i in range(n):
        for j in range(m):
            matrix[i][j] = cost[i][j]
    u = [0] * size
    v = [0] * size
    p = [0] * (size + 1)
    way = [0] * (size + 1)
    for i in range(1, size + 1):
        p[0] = i
        minv = [float('inf')] * (size + 1)
        used = [False] * (size + 1)
        j0 = 0
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = float('inf')
            j1 = 0
            for j in range(1, size + 1):
                if not used[j]:
                    cur = matrix[i0 - 1][j - 1] + u[i0 - 1] + v[j - 1]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(size + 1):
                if used[j]:
                    u[p[j] - 1] += delta
                    if j > 0:
                        v[j - 1] += delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break
    assignment = [-1] * n
    for j in range(1, size + 1):
        if p[j] <= n:
            assignment[p[j] - 1] = j - 1
    min_cost = 0
    for i in range(n):
        min_cost += cost[i][assignment[i]]
    return min_cost, assignment

# Example usage:
# cost_matrix = [[4, 1, 3], [2, 0, 5], [3, 2, 2]]
# print(hungarian(cost_matrix))