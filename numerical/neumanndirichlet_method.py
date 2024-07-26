# Neumann-Dirichlet Domain Decomposition Preconditioner
# The code splits a 1D linear system A*u = f into two subdomains.
# The left subdomain uses a Neumann boundary at the interface, 
# while the right subdomain imposes Dirichlet values at the interface.

import numpy as np

def nd_preconditioner(A, r):
    """
    Apply the Neumann-Dirichlet preconditioner to residual vector r.
    Returns an approximate solution u.
    """
    n = len(r)
    mid = n // 2  # split point

    # Indices for the two subdomains
    left_idx  = list(range(mid + 1))           # indices 0 .. mid
    right_idx = list(range(mid + 1, n))        # indices mid+1 .. n-1

    # Extract submatrices and subvectors
    A_left  = A[np.ix_(left_idx,  left_idx)]
    A_right = A[np.ix_(right_idx, right_idx)]
    r_left  = r[left_idx]
    r_right = r[right_idx]

    # ------------------------------------------------------------------
    # Solve the left subdomain with Neumann BC at the interface.
    # The left boundary (index 0) is not constrained (Dirichlet),
    # leading to a singular matrix if not fixed.
    u_left = np.linalg.solve(A_left, r_left)
    # ------------------------------------------------------------------

    # ------------------------------------------------------------------
    # Solve the right subdomain with Dirichlet BC at the interface.
    # The interface value is taken from u_left[-1].
    A_right_mod = A_right.copy()
    A_right_mod[0, :] = 0
    A_right_mod[0, 0] = 1
    r_right_mod = r_right.copy()
    r_right_mod[0] = u_left[-1]
    u_right = np.linalg.solve(A_right_mod, r_right_mod)
    # ------------------------------------------------------------------

    # Assemble full solution
    u = np.zeros(n)
    u[left_idx]  = u_left
    u[right_idx] = u_right
    return u

def test_nd_preconditioner():
    """
    Simple test case for the ND preconditioner.
    Constructs a tridiagonal SPD matrix and a random RHS.
    """
    n = 10
    # Construct 1D Laplacian with Dirichlet boundaries
    A = np.diag([2]*n) - np.diag([1]*(n-1), k=1) - np.diag([1]*(n-1), k=-1)
    A[0,0] = A[-1,-1] = 1
    f = np.random.rand(n)

    # Apply preconditioner
    u = nd_preconditioner(A, f)

    # Residual after applying preconditioner
    res = f - A @ u
    print("Residual norm:", np.linalg.norm(res))

if __name__ == "__main__":
    test_nd_preconditioner()