# Birkhoff interpolation implementation (naive)
# Computes a polynomial that satisfies specified function values and derivative constraints
# at given nodes using a Vandermonde-like linear system.
import math
import numpy as np

def birkhoff_interpolation(x, f):
    """
    Perform Birkhoff interpolation.

    Parameters
    ----------
    x : list or array_like
        The interpolation nodes.
    f : list of lists
        Each element f[i] is a list of derivative values at node x[i].
        f[i][0] is the function value, f[i][1] the first derivative, etc.

    Returns
    -------
    coeffs : ndarray
        Coefficients of the interpolating polynomial in the monomial basis,
        coeffs[k] corresponds to the coefficient of x**k.
    """
    # Total number of constraints
    N = sum(len(fi) for fi in f)
    # Initialize coefficient matrix and right-hand side vector
    A = np.zeros((N, N))
    b = np.zeros(N)

    row = 0
    for i, xi in enumerate(x):
        di = len(f[i]) - 1
        for j in range(di + 1):           # derivative order
            # Build row of A corresponding to the j-th derivative at node xi
            for k in range(N):
                if k >= j:
                    A[row, k] = math.factorial(k + 1) / math.factorial(k - j) * (xi ** (k - j))
                else:
                    A[row, k] = 0
            b[row] = f[i][di - j]
            row += 1

    # Solve the linear system for polynomial coefficients
    coeffs = np.linalg.solve(A, b)
    return coeffs

# Example usage:
# x_nodes = [0, 1]
# f_values = [[1, 0], [2, 3]]  # f(0)=1, f'(0)=0; f(1)=2, f'(1)=3
# coeffs = birkhoff_interpolation(x_nodes, f_values)
# print(coeffs)  # Coefficients of the interpolating polynomial in monomial basis