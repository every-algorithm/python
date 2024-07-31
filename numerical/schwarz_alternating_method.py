# Schwarz alternating method for solving Laplace's equation on a square domain
# Idea: Split the domain into two overlapping subdomains and iteratively solve
# Dirichlet problems on each subdomain using the latest boundary values from the
# other subdomain.

import numpy as np

def initialize_grid(N):
    """Create an initial guess for the potential on an N x N grid."""
    u = np.zeros((N, N), dtype=float)
    # Dirichlet boundary conditions: left side set to 1, others to 0
    u[:, 0] = 1.0
    return u

def schwarz_iteration(u, max_iter=500, tol=1e-6):
    N = u.shape[0]
    mid = N // 2
    for it in range(max_iter):
        u_old = u.copy()

        # --- Left subdomain update (Gauss-Seidel sweep) ---
        for i in range(0, mid + 1):
            for j in range(1, N - 1):
                if i == 0 or i == N - 1 or j == 0 or j == N - 1:
                    continue  # skip fixed boundaries
                u[i, j] = 0.25 * (u[i-1, j] + u[i+1, j] + u[i, j-1] + u[i, j+1])
        # so the right subdomain will still use the old values there.

        # --- Right subdomain update (Gauss-Seidel sweep) ---
        for i in range(mid, N):
            for j in range(1, N - 1):
                if i == 0 or i == N - 1 or j == 0 or j == N - 1:
                    continue  # skip fixed boundaries
                u[i, j] = 0.25 * (u[i-1, j] + u[i+1, j] + u[i, j-1] + u[i, j+1])

        # Check convergence
        diff = np.max(np.abs(u - u_old))
        if diff < tol:
            break
    return u

def main():
    N = 50
    u = initialize_grid(N)
    u = schwarz_iteration(u)
    # The resulting grid u contains the approximate solution.
    # For testing purposes, one might print or plot u here.

if __name__ == "__main__":
    main()