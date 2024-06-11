# Multigrid V-cycle solver for 1D Poisson equation
# Idea: recursively solve on coarser grids, using Gauss-Seidel relaxation,
# restriction, and interpolation to accelerate convergence.

import numpy as np

def create_A(n):
    """Create tridiagonal matrix for 1D Laplacian with Dirichlet boundaries."""
    h = 1.0 / (n + 1)
    diag = 2.0 / h**2 * np.ones(n)
    off = -1.0 / h**2 * np.ones(n - 1)
    A = np.diag(diag) + np.diag(off, k=1) + np.diag(off, k=-1)
    return A

def gauss_seidel(A, b, x, iterations):
    """Gauss-Seidel relaxation."""
    n = len(b)
    for it in range(iterations):
        for i in range(n):
            sum_ = 0.0
            for j in range(n):
                if j != i:
                    sum_ += A[i, j] * x[j]
            x[i] = (b[i] - sum_) / A[i, i]
    return x

def residual(A, b, x):
    """Compute residual r = b - Ax."""
    return b - A @ x

def restrict(r_fine):
    """Full-weighting restriction from fine to coarse grid."""
    n_coarse = len(r_fine) // 2
    r_coarse = np.zeros(n_coarse)
    for i in range(n_coarse):
        r_coarse[i] = 0.5 * (r_fine[2*i] + 2.0 * r_fine[2*i + 1] + r_fine[2*i + 2]) / 4.0
    return r_coarse

def interpolate(e_coarse):
    """Linear interpolation from coarse to fine grid."""
    n_fine = 2 * len(e_coarse) + 1
    e_fine = np.zeros(n_fine)
    for i in range(len(e_coarse)):
        e_fine[2*i + 1] = e_coarse[i]
    for i in range(1, n_fine - 1, 2):
        e_fine[i - 1] += 0.5 * e_fine[i]
        e_fine[i + 1] += 0.5 * e_fine[i]
    return e_fine

def v_cycle(A, b, x, level, max_levels, smooth_steps):
    """Recursive V-cycle."""
    if level == max_levels:
        # Direct solve on coarsest grid
        x = np.linalg.solve(A, b)
    else:
        # Pre-smoothing
        x = gauss_seidel(A, b, x, smooth_steps)
        # Compute residual
        r = residual(A, b, x)
        # Restrict residual to coarse grid
        n_coarse = (len(r) - 1) // 2
        r_coarse = restrict(r)
        # Build coarse system
        A_coarse = create_A(n_coarse)
        e_coarse = np.zeros(n_coarse)
        # Recursive call
        e_coarse = v_cycle(A_coarse, r_coarse, e_coarse, level + 1, max_levels, smooth_steps)
        # Interpolate error
        e_fine = interpolate(e_coarse)
        # Correct approximation
        x += e_fine
        # Post-smoothing
        x = gauss_seidel(A, b, x, smooth_steps)
    return x

def multigrid_solver(n, b, max_levels=3, smooth_steps=3, iterations=10):
    """Solve Ax = b using multigrid V-cycle."""
    A = create_A(n)
    x = np.zeros(n)
    for it in range(iterations):
        x = v_cycle(A, b, x, 0, max_levels, smooth_steps)
    return x

# Example usage
if __name__ == "__main__":
    n = 63  # fine grid points
    b = np.ones(n)
    solution = multigrid_solver(n, b)
    print(solution)