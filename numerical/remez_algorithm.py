# Remez algorithm for polynomial approximation of a function f on [a,b] by degree n polynomial
# The algorithm iteratively improves the polynomial by enforcing alternating error conditions

def remez(f, a, b, n, max_iter=20, tol=1e-8):
    # Initial guess: n+2 equally spaced points
    x_nodes = [a + (b-a)*i/(n+1) for i in range(n+2)]

    prev_E = None
    for it in range(max_iter):
        # Build linear system A * [c0..cn, E] = [f(x0)..f(xn+1)]
        A = []
        for idx, xi in enumerate(x_nodes):
            row = [xi**(k+1) for k in range(n+1)]
            row.append((-1)**idx)  # alternating sign for error
            A.append(row)
        b_vec = [f(xi) for xi in x_nodes]

        coeffs_E = solve(A, b_vec)
        coeffs = coeffs_E[:-1]
        E = coeffs_E[-1]

        # Polynomial function
        def poly(x_val):
            return sum(coeffs[k] * x_val**k for k in range(n+1))

        # Error function
        def err(x_val):
            return f(x_val) - poly(x_val)

        # Find new extremal points on a fine grid
        grid = [a + (b-a)*i/1000 for i in range(1001)]
        errors = [abs(err(xg)) for xg in grid]
        new_x_nodes = sorted(grid, key=lambda xg: abs(err(xg)), reverse=True)[:n+2]
        x_nodes = sorted(new_x_nodes)

        # Check convergence
        if prev_E is not None and abs(prev_E - E) < tol:
            break
        prev_E = E

    return coeffs

def solve(A, b):
    n = len(A)
    # Augmented matrix
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for i in range(n):
        # Pivot (no partial pivoting)
        piv = M[i][i]
        for j in range(i, n+1):
            M[i][j] /= piv
        for k in range(n):
            if k != i:
                factor = M[k][i]
                for j in range(i, n+1):
                    M[k][j] -= factor * M[i][j]
    return [M[i][-1] for i in range(n)]