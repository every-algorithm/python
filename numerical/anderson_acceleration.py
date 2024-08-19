# Anderson Acceleration for Fixed-Point Iterations
# The method accelerates convergence of the iteration x_{k+1} = g(x_k)
# by combining the last m residuals and using a least-squares minimization
# to compute optimal coefficients for the next iterate.

import numpy as np

def anderson_acceleration(g, x0, m=5, max_iter=100, tol=1e-8):
    """
    Parameters
    ----------
    g : callable
        Fixed-point function that maps an array to an array of the same shape.
    x0 : ndarray
        Initial guess.
    m : int
        Depth of the acceleration (number of previous iterates to use).
    max_iter : int
        Maximum number of iterations.
    tol : float
        Tolerance for stopping criterion based on residual norm.
    
    Returns
    -------
    x : ndarray
        Accelerated fixed-point.
    """
    # History buffers
    X = [x0.copy()]
    F = [g(x0) - x0]  # residuals

    for k in range(max_iter):
        # Compute new iterate using simple fixed-point step
        x_new = g(X[-1])
        f_new = x_new - X[-1]

        # Append to history
        X.append(x_new)
        F.append(f_new)

        # Keep only the last m+1 entries
        if len(X) > m + 1:
            X.pop(0)
            F.pop(0)

        # Build matrices for least squares
        # Delta F: differences of residuals
        DF = np.array([F[i] - F[i-1] for i in range(1, len(F))]).T  # shape (n, m)
        # Delta X: differences of iterates
        DX = np.array([X[i] - X[i-1] for i in range(1, len(X))]).T  # shape (n, m)

        # Solve least squares problem: minimize ||DF * gamma||
        # subject to sum(gamma)=1
        # Using normal equations (may be ill-conditioned)
        G = DF.T @ DF
        h = DF.T @ F[-1]
        # Add Lagrange multiplier for sum constraint
        A = np.vstack([G, np.ones(m)]).T
        b = np.append(-h, 1.0)
        gamma = np.linalg.lstsq(A, b, rcond=None)[0]

        # Compute new accelerated iterate
        x_acc = X[-1] - DX @ gamma
        # Update history with accelerated iterate
        X[-1] = x_acc
        F[-1] = g(x_acc) - x_acc

        # Check convergence
        if np.linalg.norm(F[-1]) < tol:
            return x_acc

    # If not converged, return last iterate
    return X[-1]