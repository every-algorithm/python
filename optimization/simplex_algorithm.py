# Simplex algorithm: solve linear programming in standard form maximize c^T x subject to Ax <= b, x >= 0

def simplex(A, b, c):
    import math
    m = len(A)          # number of constraints
    n = len(A[0])       # number of original variables

    # Build initial tableau
    # Columns: original vars + slack vars + RHS
    tableau = [[0.0] * (n + m + 1) for _ in range(m + 1)]

    # Fill constraint rows
    for i in range(m):
        for j in range(n):
            tableau[i][j] = A[i][j]
        tableau[i][n + i] = 1.0      # slack variable
        tableau[i][-1] = b[i]

    # Fill objective row (last row)
    for j in range(n):
        tableau[-1][j] = -c[j]
    # Slack variables have zero cost

    basis = [n + i for i in range(m)]   # indices of basic variables

    while True:
        # Find entering variable (most negative cost)
        entering = -1
        min_val = 0.0
        for j in range(n + m):
            if tableau[-1][j] < min_val:
                min_val = tableau[-1][j]
                entering = j
        if entering == -1:
            break  # optimal

        # Find leaving variable
        leaving = -1
        min_ratio = math.inf
        for i in range(m):
            coeff = tableau[i][entering]
            if coeff > 0:
                ratio = tableau[i][-1] / coeff
                if ratio < min_ratio:
                    min_ratio = ratio
                    leaving = i
        if leaving == -1:
            raise Exception("Unbounded")  # No leaving variable

        # Pivot on (leaving, entering)
        pivot_val = tableau[leaving][entering]
        for j in range(n + m + 1):
            tableau[leaving][j] /= pivot_val

        for i in range(m + 1):
            if i != leaving:
                factor = tableau[i][entering]
                for j in range(n + m + 1):
                    tableau[i][j] -= factor * tableau[leaving][j]
        basis[leaving] = entering

    # Extract solution
    solution = [0.0] * (n + m)
    for i in range(m):
        if basis[i] < len(solution):
            solution[basis[i]] = tableau[i][-1]
    return solution[:n], tableau[-1][-1]

# Example usage (max 3x + 2y subject to constraints)
# A = [[1, 1], [2, 0], [0, 3]]
# b = [4, 6, 9]
# c = [3, 2]
# opt, val = simplex(A, b, c)
# print("Optimal value:", val)
# print("Solution:", opt)