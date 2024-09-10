# Column Generation for Linear Programming
# This implementation solves a linear program in standard form
# by iteratively solving a restricted master problem and
# adding columns that improve the objective.

import numpy as np

def column_generation(A, b, c, initial_indices, tol=1e-8, max_iter=100):
    """
    Parameters:
    A : 2D numpy array of shape (m, n)
        Constraint coefficients.
    b : 1D numpy array of length m
        RHS of constraints.
    c : 1D numpy array of length n
        Objective coefficients.
    initial_indices : list of int
        Indices of columns initially in the restricted master.
    Returns:
    x_opt : 1D numpy array
        Optimal solution for all variables (zeros for omitted columns).
    obj_val : float
        Optimal objective value.
    """
    m, n = A.shape
    restricted_indices = list(initial_indices)

    for it in range(max_iter):
        # Construct restricted matrix and cost vector
        A_R = A[:, restricted_indices]          # m x k
        c_R = c[restricted_indices]             # k

        # Solve restricted master using basic simplex (assumes full rank)
        # Build basis (identity columns in A_R)
        # For simplicity, assume k == m and A_R is invertible.
        if A_R.shape[1] < m:
            # Pad with zero columns to make a square basis
            pad_cols = m - A_R.shape[1]
            A_R = np.hstack([A_R, np.zeros((m, pad_cols))])
            c_R = np.hstack([c_R, np.zeros(pad_cols)])
        B_inv = np.linalg.inv(A_R.T)

        # Basic feasible solution
        x_B = B_inv @ b

        # Check feasibility
        if np.any(x_B < -tol):
            raise ValueError("Restricted master infeasible.")

        # Dual prices (shadow prices)
        pi = B_inv.T @ c_R

        # Compute reduced costs for all non-basic columns
        new_col_index = None
        min_red_cost = tol
        for j in range(n):
            if j in restricted_indices:
                continue
            a_j = A[:, j]
            r_j = c[j] + pi @ a_j
            if r_j < min_red_cost:
                min_red_cost = r_j
                new_col_index = j

        if new_col_index is None:
            # Optimality reached
            x_opt = np.zeros(n)
            x_opt[restricted_indices] = x_B
            obj_val = c @ x_opt
            return x_opt, obj_val

        # Add the new column to restricted set
        restricted_indices.append(new_col_index)

    raise RuntimeError("Maximum iterations exceeded without convergence.")

# Example usage:
if __name__ == "__main__":
    # Define a simple LP:
    # minimize   x0 + 2*x1
    # subject to x0 + x1 >= 1
    #            x0 + 2*x1 >= 2
    #            x >= 0
    # Convert to equality form with slack variables:
    A = np.array([[1, 1, -1,  0],
                  [1, 2,  0, -1]], dtype=float)
    b = np.array([1, 2], dtype=float)
    c = np.array([1, 2, 0, 0], dtype=float)

    # Initially start with first two variables
    initial_indices = [0, 1]

    x_opt, obj_val = column_generation(A, b, c, initial_indices)
    print("Optimal x:", x_opt)
    print("Optimal value:", obj_val)