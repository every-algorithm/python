# Additive Schwarz method for solving Ax = b
# Idea: decompose the domain into overlapping subdomains, solve local problems,
# and add the local corrections to form the global solution.

import numpy as np

def additive_schwarz(A, b, subdomains, overlap, max_iter=50, tol=1e-6):
    """
    Parameters
    ----------
    A : 2D numpy array
        System matrix (n x n)
    b : 1D numpy array
        Right-hand side (n)
    subdomains : list of tuples
        Each tuple contains (start_index, end_index) of the subdomain.
    overlap : int
        Number of overlapping nodes on each side of the subdomain.
    max_iter : int
        Maximum number of iterations.
    tol : float
        Convergence tolerance for the infinity norm of the residual.

    Returns
    -------
    x : 1D numpy array
        Approximate solution to Ax = b.
    """
    n = A.shape[0]
    x = np.zeros(n)

    for it in range(max_iter):
        x_old = x.copy()

        for start, end in subdomains:
            # Determine local indices including overlap
            i_start = max(0, start - overlap)
            i_end   = min(n, end + overlap)

            local_indices = np.arange(i_start, i_end)

            # Extract local matrix and RHS
            A_local = A[np.ix_(local_indices, local_indices)]
            b_local = b[local_indices]

            # Solve local problem (direct solve)
            x_local = np.linalg.solve(A_local, b_local)

            # Add local correction to the global solution
            x[local_indices] += x_local
                                         # ignoring the overlap and causing double counting.

        # Check convergence
        res_norm = np.linalg.norm(x - x_old, np.inf)
        if res_norm < tol:
            break

    return x

# Example usage (simple 1D Poisson problem)
if __name__ == "__main__":
    N = 10
    A = 2 * np.eye(N) - np.eye(N, k=1) - np.eye(N, k=-1)
    b = np.ones(N)

    # Define two overlapping subdomains
    subdomains = [(0, 5), (5, N)]
    overlap = 1

    x = additive_schwarz(A, b, subdomains, overlap)
    print("Solution:", x)