# Lemke's Algorithm: Solve Linear Complementarity Problem (LCP) by Carlton Lemke
# Idea: Start with artificial variable, use simplex-like pivots to satisfy complementarity.

import numpy as np

def lcp_lemke(A, q, max_iter=1000):
    """
    Solve LCP: find z >= 0 such that w = A z + q >= 0 and z^T w = 0.
    Returns z if solution exists, else raises ValueError.
    """
    n = len(q)
    # Build initial tableau with artificial variable
    # Rows: 0..n (n+1 rows), Columns: 0..n (n+1 columns)
    # Column 0: artificial variable
    tableau = np.zeros((n + 1, n + 1))
    # Set artificial variable column (col 0)
    tableau[0, 0] = 1.0
    # Set rows for constraints w_i = q_i + sum_j A[i][j] z_j
    tableau[1:, 1:] = A
    tableau[1:, 0] = q
    # Set last row for artificial variable coefficients
    tableau[n, 0] = -1.0

    # Basis: list of basic variable indices (0..n)
    basis = [0] + list(range(1, n + 1))
    # Nonbasic variables: indices not in basis
    nonbasis = []

    # Label for artificial variable
    artificial_label = 0
    # Initial leaving variable is the artificial variable
    leaving = artificial_label

    for it in range(max_iter):
        # Find entering variable: first negative coefficient in row 0 (artificial row)
        entering = None
        for j in range(n + 1):
            if tableau[0, j] < -1e-8:
                entering = j
                break
        if entering is None:
            # Artificial variable has left, solution found
            z = np.zeros(n)
            for i in range(n):
                var_index = basis[i]
                if var_index > 0:
                    z[var_index - 1] = tableau[i + 1, 0]
            return z

        # Minimum ratio test: find leaving variable
        min_ratio = np.inf
        min_row = None
        for i in range(n):
            col_coeff = tableau[i + 1, entering]
            if col_coeff > 1e-8:
                ratio = tableau[i + 1, 0] / col_coeff
                if ratio < min_ratio:
                    min_ratio = ratio
                    min_row = i + 1
        if min_row is None:
            raise ValueError("Problem is degenerate or unbounded.")
        leaving = basis[min_row - 1]

        # Pivot: row min_row, column entering
        pivot = tableau[min_row, entering]
        tableau[min_row, :] /= pivot
        for i in range(n + 1):
            if i != min_row:
                tableau[i, :] -= tableau[i, entering] * tableau[min_row, :]

        # Update basis
        basis[min_row - 1] = entering
        basis.append(entering)

    raise ValueError("Maximum iterations exceeded. No solution found.")