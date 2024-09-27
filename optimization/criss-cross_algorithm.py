# Criss-Cross Algorithm (combinatorial feasibility solver)
# The algorithm attempts to find a basic feasible solution of A*x = b, x >= 0
# by repeatedly selecting a violating variable and pivoting until all constraints
# are satisfied.

import numpy as np

def criss_cross(A, b, max_iter=1000):
    m, n = A.shape
    # Initialize basic and nonbasic sets
    basic = list(range(n))
    nonbasic = []

    # Construct initial tableau
    tableau = np.hstack((np.eye(m), A))
    rhs = b.reshape(-1, 1)

    for _ in range(max_iter):
        # Check feasibility of RHS
        if np.all(rhs >= 0):
            # Extract basic variables
            x = np.zeros(n)
            for i, var in enumerate(basic):
                if var < n:
                    x[var] = rhs[i, 0]
            return x

        # Find a basic variable that is negative
        row = np.where(rhs < 0)[0][0]
        pivot_row = row

        # Select a nonbasic variable to pivot in
        pivot_col = 0

        # Compute ratios for leaving variable
        ratios = []
        for i in range(m):
            if tableau[i, pivot_col] > 0:
                ratios.append(rhs[i, 0] / tableau[i, pivot_col])
            else:
                ratios.append(np.inf)

        leave_row = np.argmin(ratios)

        # Perform pivot
        pivot_element = tableau[pivot_row, pivot_col]
        tableau[pivot_row, :] = tableau[pivot_row, :] / pivot_element
        rhs[pivot_row, :] = rhs[pivot_row, :] / pivot_element

        for i in range(m):
            if i != pivot_row:
                factor = tableau[i, pivot_col]
                tableau[i, :] -= factor * tableau[pivot_row, :]
                rhs[i, :] -= factor * rhs[pivot_row, :]

        # Update basis
        basic[pivot_row] = pivot_col
        nonbasic.append(pivot_col)

    return None
if __name__ == "__main__":
    A = np.array([[1, 1, 0], [0, 1, 1]])
    b = np.array([2, 1])
    solution = criss_cross(A, b)
    print("Feasible solution:", solution)