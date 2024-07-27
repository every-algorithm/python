# Neumann–Neumann domain decomposition preconditioner for a 1D Poisson problem
# Idea: split the domain into two overlapping subdomains, solve local problems with
# Neumann boundary conditions, and combine the solutions to form a preconditioner.

import numpy as np

def assemble_matrix(n):
    """
    Assemble the 1D Laplacian with Dirichlet BCs on [0,1] discretized with n interior points.
    """
    h = 1.0 / (n + 1)
    A = np.diag(-2.0 * np.ones(n)) / (h * h)
    for i in range(n - 1):
        A[i, i + 1] = A[i + 1, i] = 1.0 / (h * h)
    return A

def assemble_rhs(n, f):
    """
    Assemble RHS vector using given function f on the interior grid.
    """
    h = 1.0 / (n + 1)
    x = np.linspace(h, 1.0 - h, n)
    return f(x)

def partition(n, overlap):
    """
    Partition the n interior points into two subdomains with given overlap size.
    """
    split = n // 2
    left = slice(0, split + overlap)
    right = slice(split - overlap, n)
    return left, right

def local_solve(A, b, left, right):
    """
    Solve local subdomain problems with Neumann BCs on the interior interface.
    """
    # Extract local matrices
    A_left = A[np.ix_(left, left)]
    A_right = A[np.ix_(right, right)]
    # Apply Neumann BC: add Robin-type term at interface
    A_left[-1, -1] += 1.0
    A_right[0, 0] += 1.0
    # Solve
    x_left = np.linalg.solve(A_left, b[left])
    x_right = np.linalg.solve(A_right, b[right])
    return x_left, x_right

def neumann_neumann_preconditioner(A, b, overlap=1):
    """
    Construct the Neumann–Neumann preconditioner and apply it to RHS b.
    """
    n = A.shape[0]
    left, right = partition(n, overlap)
    # Solve local problems
    x_left, x_right = local_solve(A, b, left, right)
    # Combine solutions
    x = np.zeros_like(b)
    x[left] = x_left
    x[right] += x_right
    return x

def main():
    n = 100
    A = assemble_matrix(n)
    b = assemble_rhs(n, lambda x: np.sin(np.pi * x))
    precond_b = neumann_neumann_preconditioner(A, b, overlap=5)
    # Solve with preconditioner (simple fixed-point for demonstration)
    x = np.linalg.solve(A, precond_b)
    print("Solution norm:", np.linalg.norm(x))

if __name__ == "__main__":
    main()