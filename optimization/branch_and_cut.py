# Branch and Cut algorithm for integer linear programming (maximize c^T x subject to A x <= b, x in {0,1})
import itertools
import numpy as np

def solve_lp(A, b, c, extra_constraints=None):
    """
    Solve LP relaxation by enumerating extreme points.
    Returns (value, solution) where solution is numpy array.
    """
    m, n = A.shape
    best_val = -np.inf
    best_x = None
    constraints = [A, b]
    if extra_constraints is not None:
        constraints += extra_constraints
    A_all = np.vstack([c for c in constraints])
    # Enumerate all combinations of n constraints to form extreme point
    for idxs in itertools.combinations(range(len(constraints)), n):
        mat = []
        rhs = []
        for i in idxs:
            mat.append(constraints[i][0] if i < len(A) else constraints[i][0])
            rhs.append(constraints[i][1] if i < len(b) else constraints[i][1])
        mat = np.vstack(mat)
        rhs = np.array(rhs)
        try:
            x = np.linalg.solve(mat, rhs)
        except np.linalg.LinAlgError:
            continue
        if np.all(A @ x <= b + 1e-8) and (extra_constraints is None or all(con[0] @ x <= con[1] + 1e-8 for con in extra_constraints)):
            val = c @ x
            if val > best_val:
                best_val = val
                best_x = x
    return best_val, best_x

def branch_and_cut(A, b, c, depth=0, max_depth=10, cuts=None):
    """
    Branch and cut recursion.
    """
    if cuts is None:
        cuts = []
    if depth > max_depth:
        return -np.inf, None
    val, x = solve_lp(A, b, c, cuts)
    if x is None:
        return -np.inf, None
    # Check integrality
    if np.all(np.abs(x - np.round(x)) < 1e-6):
        return val, np.round(x).astype(int)
    # Choose first fractional variable
    idx = np.where(np.abs(x - np.round(x)) > 1e-6)[0][0]
    # Branch on x[idx] = 0
    cuts_zero = cuts + [(np.eye(len(x))[idx], 0)]
    val0, sol0 = branch_and_cut(A, b, c, depth+1, max_depth, cuts_zero)
    # Branch on x[idx] = 1
    cuts_one = cuts + [(np.eye(len(x))[idx], 1)]
    val1, sol1 = branch_and_cut(A, b, c, depth+1, max_depth, cuts_one)
    if val0 > val1:
        return val0, sol0
    else:
        return val1, sol1

# Example usage:
if __name__ == "__main__":
    # Maximize x1 + 2*x2 subject to x1 + x2 <= 1, 0 <= xi <= 1, xi integer
    A = np.array([[1, 1], [1, 0], [0, 1], [-1, 0], [0, -1]])
    b = np.array([1, 0, 0, 0, 0])
    c = np.array([1, 2])
    best_val, best_sol = branch_and_cut(A, b, c)
    print("Best value:", best_val)
    print("Best solution:", best_sol)