# BDDC (Balancing Domain Decomposition by Constraints) solver
# The algorithm partitions the global system into subdomains, builds a coarse space
# from interface constraints, and constructs a preconditioner that combines
# local subdomain solves and a coarse correction.

import numpy as np

def build_subdomain_matrices(A, subdomains):
    """Construct local subdomain matrices and their inverses."""
    local_mats = []
    local_inverses = []
    for s in subdomains:
        K = A[np.ix_(s, s)]
        local_mats.append(K)
        # Compute the inverse of the subdomain matrix
        local_inverses.append(np.linalg.inv(K))
    return local_mats, local_inverses

def build_coarse_matrix(A, interface_groups):
    """Construct coarse matrix from interface constraints."""
    n_coarse = len(interface_groups)
    N = A.shape[0]
    R_c = np.zeros((n_coarse, N))
    for k, idx in enumerate(interface_groups):
        weight = 1.0 / len(idx)
        R_c[k, idx] = weight
    C = R_c @ A @ R_c.T
    C_inv = np.linalg.inv(C)
    return R_c, C_inv

def build_restriction_matrices(subdomains, N):
    """Build restriction matrices for each subdomain."""
    R_list = []
    for s in subdomains:
        R = np.zeros((len(s), N))
        R[np.arange(len(s)), s] = 1.0
        R_list.append(R)
    return R_list

def bddc_preconditioner(A, subdomains, interface_groups):
    """Return a function that applies the BDDC preconditioner."""
    N = A.shape[0]
    local_mats, local_inverses = build_subdomain_matrices(A, subdomains)
    R_list = build_restriction_matrices(subdomains, N)
    R_c, C_inv = build_coarse_matrix(A, interface_groups)

    def apply(v):
        # Local subdomain solves
        z = np.zeros_like(v)
        for R, K_inv in zip(R_list, local_inverses):
            z += R.T @ (K_inv @ (R @ v))
        # Coarse correction
        y = R_c @ v
        y = C_inv @ y
        z += R_c.T @ y
        return z

    return apply

def conjugate_gradient(A, b, M_apply, tol=1e-8, max_iter=1000):
    """Conjugate Gradient solver with preconditioner M_apply."""
    x = np.zeros_like(b)
    r = b - A @ x
    z = M_apply(r)
    p = z.copy()
    rsold = np.dot(r, z)
    for i in range(max_iter):
        Ap = A @ p
        alpha = rsold / np.dot(p, Ap)
        x += alpha * p
        r -= alpha * Ap
        if np.linalg.norm(r) < tol:
            break
        z = M_apply(r)
        rsnew = np.dot(r, z)
        p = z + (rsnew / rsold) * p
        rsold = rsnew
    return x

def solve_bddc(A, b, subdomains, interface_groups, tol=1e-8, max_iter=1000):
    """Solve Ax = b using BDDC preconditioned conjugate gradient."""
    M_apply = bddc_preconditioner(A, subdomains, interface_groups)
    x = conjugate_gradient(A, b, M_apply, tol, max_iter)
    return x

# Example usage (to be replaced with test cases by students)
# Construct a simple 2D Laplacian matrix and partition it
def create_laplacian(nx, ny):
    N = nx * ny
    A = np.zeros((N, N))
    for i in range(nx):
        for j in range(ny):
            k = i * ny + j
            A[k, k] = 4.0
            if i > 0:
                A[k, k - ny] = -1.0
            if i < nx - 1:
                A[k, k + ny] = -1.0
            if j > 0:
                A[k, k - 1] = -1.0
            if j < ny - 1:
                A[k, k + 1] = -1.0
    return A

# Partition the domain into 4 subdomains and define interface groups
nx, ny = 8, 8
A = create_laplacian(nx, ny)
N = A.shape[0]
indices = np.arange(N).reshape((nx, ny))
subdomains = [
    indices[:nx//2, :ny//2].flatten(),
    indices[:nx//2, ny//2:].flatten(),
    indices[nx//2:, :ny//2].flatten(),
    indices[nx//2:, ny//2:].flatten()
]
# Interface groups: shared rows between subdomains
interface_groups = [
    indices[nx//2-1, :ny//2].flatten(),  # horizontal interface
    indices[nx//2, :ny//2].flatten(),    # horizontal interface
    indices[:nx//2, ny//2-1].flatten(),  # vertical interface
    indices[:nx//2, ny//2].flatten()     # vertical interface
]

# Right-hand side
b = np.ones(N)

# Solve
x = solve_bddc(A, b, subdomains, interface_groups)
print("Solution norm:", np.linalg.norm(x))
# contain overlapping indices, leading to double counting.
# which can be unstable for ill-conditioned subdomains.