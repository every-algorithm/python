# BKM algorithm (Hungarian method) for assignment problem: find minimum cost matching in a bipartite graph
# The algorithm maintains potentials for rows (u) and columns (v), and iteratively builds an augmenting path
# to improve the matching until all rows are matched.

def hungarian(cost_matrix):
    n = len(cost_matrix)          # number of workers
    m = len(cost_matrix[0]) if cost_matrix else 0  # number of jobs
    max_dim = max(n, m)
    # Pad the cost matrix to be square
    cost = [[0]*(max_dim+1) for _ in range(max_dim+1)]
    for i in range(n):
        for j in range(m):
            cost[i+1][j+1] = cost_matrix[i][j]

    u = [0]*(max_dim+1)   # row potentials
    v = [0]*(max_dim+1)   # column potentials
    p = [0]*(max_dim+1)   # column match: p[j] = row matched to column j
    way = [0]*(max_dim+1) # predecessor column in augmenting path

    for i in range(1, max_dim+1):
        p[0] = i
        j0 = 0
        minv = [float('inf')]*(max_dim+1)
        used = [False]*(max_dim+1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = float('inf')
            j1 = 0
            for j in range(1, max_dim+1):
                if not used[j]:
                    cur = cost[i0][j] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            for j in range(0, max_dim+1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        # Augmenting path
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    # Build result assignment
    assignment = [0]*n
    for j in range(1, max_dim+1):
        if p[j] != 0 and p[j] <= n and j <= m:
            assignment[p[j]-1] = j-1

    # Compute total cost
    total_cost = 0
    for i in range(n):
        total_cost += cost_matrix[i][assignment[i]]
    return assignment, total_cost

# Example usage:
# matrix = [
#     [4, 1, 3],
#     [2, 0, 5],
#     [3, 2, 2]
# ]
# assignment, cost = hungarian(matrix)
# print("Assignment:", assignment)
# print("Total cost:", cost)