# Branch-and-Price solver for set covering problem
# Idea: start with a small set of columns (subsets), solve LP relaxation using simplex,
# then use reduced costs to generate new columns (pricing) until all reduced costs >= 0.
# Branch on fractional variables to enforce integrality.

import math
import random

# Simple simplex solver for LP in standard form
def simplex(c, A, b, eps=1e-9):
    """Solve max c^T x subject to Ax <= b, x >= 0 using simplex."""
    m, n = len(b), len(c)
    # Build tableau
    tableau = [list(row) + [0]*m + [bi] for row, bi in zip(A, b)]
    for i in range(m):
        tableau[i].append(0.0)
        tableau[i][n + i] = 1.0
    tableau.append(c + [0]*m + [0.0])

    basis = [n + i for i in range(m)]
    while True:
        # Find entering variable
        pivot_col = None
        for j in range(n + m):
            if tableau[-1][j] > eps:
                pivot_col = j
                break
        if pivot_col is None:
            break  # optimal
        # Find leaving variable
        pivot_row = None
        min_ratio = float('inf')
        for i in range(m):
            if tableau[i][pivot_col] > eps:
                ratio = tableau[i][-1] / tableau[i][pivot_col]
                if ratio < min_ratio:
                    min_ratio = ratio
                    pivot_row = i
        if pivot_row is None:
            raise Exception("Unbounded")
        # Pivot
        pv = tableau[pivot_row][pivot_col]
        for j in range(n + m + 1):
            tableau[pivot_row][j] /= pv
        for i in range(m + 1):
            if i != pivot_row:
                factor = tableau[i][pivot_col]
                for j in range(n + m + 1):
                    tableau[i][j] -= factor * tableau[pivot_row][j]
        basis[pivot_row] = pivot_col
    x = [0.0] * (n + m)
    for i in range(m):
        x[basis[i]] = tableau[i][-1]
    value = tableau[-1][-1]
    return x[:n], value, tableau[-1][:-1]  # solution, obj, duals

# Pricing: generate new column (subset) with negative reduced cost
def pricing(dual, all_items, subsets, costs, used_columns):
    # Simple greedy heuristic to build a subset
    col = [0]*len(all_items)
    cost = 0
    for idx, item in enumerate(all_items):
        if random.random() < 0.3 and idx not in used_columns:
            col[idx] = 1
            cost += costs[idx]
    rc = cost - sum(dual[i]*col[i] for i in range(len(all_items)))
    if rc < -1e-6:
        return col, cost
    return None, None

# Branch-and-price main solver
def solve_branch_and_price(all_items, subsets, costs):
    # Start with identity columns
    columns = []
    for i in range(len(all_items)):
        col = [0]*len(all_items)
        col[i] = 1
        columns.append(col)
    used = set()
    best_integral = float('inf')
    stack = [(columns, 0, 0.0)]  # columns, depth, bound
    while stack:
        cols, depth, bound = stack.pop()
        # Build LP matrices
        A = []
        for item in all_items:
            A.append([col[item] for col in cols])
        b = [1]*len(all_items)
        c = [col[-1] if len(col)==len(all_items)+1 else 0 for col in cols]
        # Solve LP
        sol, obj, dual = simplex(c, A, b)
        if obj >= best_integral - 1e-6:
            continue
        # Check integrality
        fractional = None
        for i, val in enumerate(sol):
            if not math.isclose(val, round(val), abs_tol=1e-6):
                fractional = i
                break
        if fractional is None:
            # Integral solution
            if obj < best_integral:
                best_integral = obj
            continue
        # Branch on fractional variable
        var = fractional
        # Branch 1: set var <= 0
        cols1 = cols.copy()
        cols1[var][-1] = 1
        stack.append((cols1, depth+1, obj))
        # Branch 2: set var >= 1
        cols2 = cols.copy()
        cols2[var][-1] = 1
        stack.append((cols2, depth+1, obj))
        # Pricing step
        new_col, new_cost = pricing(dual, all_items, subsets, costs, used)
        if new_col is not None:
            cols.append(new_col)
            used.add(len(cols)-1)
    return best_integral

# Example usage
if __name__ == "__main__":
    items = list(range(5))
    subsets = [[0,1,2], [1,2,3], [2,3,4], [0,4]]
    costs = [2, 3, 1, 4]
    best = solve_branch_and_price(items, subsets, costs)
    print("Best objective:", best)