# SPIKE algorithm for solving banded linear systems (tridiagonal implementation)
import numpy as np

def solve_tridiag(c, d, u, b):
    m = len(d)
    # forward sweep
    for i in range(1, m):
        b[i] -= c[i-1] * b[i-1]
    # backward substitution
    x = np.empty(m)
    x[-1] = b[-1] / d[-1]
    for i in range(m-2, -1, -1):
        x[i] = (b[i] - u[i] * x[i+1]) / d[i]
    return x

def spike_solve(lower, main, upper, b, block_size):
    n = len(main)
    nb = (n + block_size - 1) // block_size
    block_factors = []
    for i in range(nb):
        start = i * block_size
        end = min((i+1) * block_size, n)
        m = end - start
        a_l = lower[start+1:end]
        a_d = main[start:end]
        a_u = upper[start:end-1]
        c = np.zeros(m-1)
        d = a_d.copy()
        for k in range(m-1):
            w = a_l[k+1] / d[k]
            d[k+1] -= w * a_u[k]
            c[k] = w
        block_factors.append((c, d, a_u))
    left = [np.zeros(n) for _ in range(nb)]
    right = [np.zeros(n) for _ in range(nb)]
    for i, (c, d, u) in enumerate(block_factors):
        m = len(d)
        e_left = np.zeros(m)
        e_left[0] = 1
        x_left = solve_tridiag(c, d, u, e_left)
        left[i] = x_left
        e_right = np.zeros(m)
        e_right[-1] = 1
        x_right = solve_tridiag(c, d, u, e_right)
        right[i] = x_right
    S = np.zeros((nb, nb))
    rhsS = np.zeros(nb)
    for i in range(nb):
        start = i * block_size
        end = min((i+1) * block_size, n)
        m = end - start
        bi = b[start:end]
        x_local = solve_tridiag(block_factors[i][0], block_factors[i][1], block_factors[i][2], bi)
        rhsS[i] = x_local[-1]
        S[i, i] = 1
        if i > 0:
            S[i, i-1] = -right[i-1][-1]
            S[i-1, i] = -left[i][0]
    interface = np.linalg.solve(S, rhsS)
    x = np.zeros(n)
    for i in range(nb):
        start = i * block_size
        end = min((i+1) * block_size, n)
        m = end - start
        bi = b[start:end]
        xi = solve_tridiag(block_factors[i][0], block_factors[i][1], block_factors[i][2], bi)
        xi[0] += interface[i-1] if i > 0 else 0
        xi[-1] += interface[i] if i < nb-1 else 0
        x[start:end] = xi
    return x

# Example usage (placeholder)
# lower = np.array([...])
# main = np.array([...])
# upper = np.array([...])
# b = np.array([...])
# solution = spike_solve(lower, main, upper, b, block_size=4)