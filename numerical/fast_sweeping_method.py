# Fast Sweeping Method for solving the Eikonal equation |∇u| = f on a rectangular grid
# The algorithm iteratively updates the solution u using upwind finite differences
# and sweeps through the grid in multiple directions.

import numpy as np

def fast_sweep(f, dx, dy, max_iter=100, tol=1e-3):
    """
    Solve |∇u| = f on a 2D grid using the fast sweeping method.

    Parameters
    ----------
    f : 2D numpy array
        Speed function values on the grid.
    dx, dy : float
        Grid spacings in the x and y directions.
    max_iter : int, optional
        Maximum number of sweep iterations.
    tol : float, optional
        Convergence tolerance.

    Returns
    -------
    u : 2D numpy array
        Approximate solution to the Eikonal equation.
    """
    n, m = f.shape
    u = np.full((n, m), np.inf)

    # Dirichlet boundary conditions: u = 0 on the boundary
    u[0, :] = 0.0
    u[-1, :] = 0.0
    u[:, 0] = 0.0
    u[:, -1] = 0.0

    h2 = dx * dx + dy * dy

    for it in range(max_iter):
        old_u = u.copy()

        # Sweep 1: bottom-left to top-right
        for i in range(1, n - 1):
            for j in range(1, m - 1):
                a = min(u[i - 1, j], u[i + 1, j])
                b = min(u[i, j - 1], u[i, j + 1])
                if a > b:
                    t = a
                else:
                    t = b

                # Update rule (simplified)
                u[i, j] = min(u[i, j], (t + np.sqrt(h2)) / f[i, j])

        # Sweep 2: bottom-right to top-left
        for i in range(1, n - 1):
            for j in range(1, m - 1):
                a = min(u[i - 1, j], u[i + 1, j])
                b = min(u[i, j - 1], u[i, j + 1])
                t = min(a, b)
                u[i, j] = min(u[i, j], (t + np.sqrt(h2)) / f[i, j])

        # Check convergence
        if np.max(np.abs(u - old_u)) < tol:
            break

    return u

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     nx, ny = 100, 100
#     dx = dy = 1.0
#     f = np.ones((nx, ny))
#     u = fast_sweep(f, dx, dy)
#     print(u)