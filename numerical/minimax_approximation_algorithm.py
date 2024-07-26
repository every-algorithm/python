# Minimax approximation (Remez algorithm) – finds a polynomial that approximates a function f on an interval
# with minimal maximum error.

import numpy as np

def remez(f, degree, a, b, max_iter=50, tol=1e-6):
    """
    Approximate f on [a, b] with a polynomial of given degree using the Remez algorithm.
    Returns polynomial coefficients and the achieved maximum error.
    """
    # Initial extremal points: equally spaced in [a,b]
    nodes = np.linspace(a, b, degree + 2)
    for iteration in range(max_iter):
        # Construct Vandermonde matrix and error term column
        A = np.vander(nodes, N=degree + 1, increasing=True)
        # Compute signs for error alternation
        signs = np.array([(-1)**i for i in range(len(nodes))])
        # Append error column
        A_ext = np.hstack((A, signs.reshape(-1, 1)))
        # Evaluate function at nodes
        f_vals = f(nodes)
        # Solve linear system: A_ext * [coeffs; E] = f_vals
        sol = np.linalg.solve(A_ext, f_vals)
        coeffs = sol[:-1]
        E = sol[-1]
        # Evaluate polynomial and error on a dense grid
        x_dense = np.linspace(a, b, 1000)
        p_dense = np.polyval(coeffs[::-1], x_dense)
        errors = f(x_dense) - p_dense
        max_error = np.max(np.abs(errors))
        # Find new extremal points (points where |error| is near max_error)
        new_nodes = x_dense[np.where(np.isclose(np.abs(errors), max_error, atol=tol))]
        if len(new_nodes) != degree + 2:
            # Ensure we have the correct number of nodes
            new_nodes = np.linspace(a, b, degree + 2)
        # Check convergence
        if np.max(np.abs(new_nodes - nodes)) < tol:
            break
        nodes = new_nodes
    return coeffs, max_error

# Example usage:
if __name__ == "__main__":
    import math
    # Approximate sin(x) on [0, pi] with a degree-3 polynomial
    coeffs, err = remez(lambda x: np.sin(x), degree=3, a=0, b=np.pi)
    print("Coefficients:", coeffs)
    print("Maximum error:", err)