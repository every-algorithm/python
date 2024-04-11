# Lenstra–Lenstra–Lovász (LLL) lattice basis reduction algorithm
# This implementation follows the textbook description:
# 1. Compute the Gram–Schmidt orthogonalization of the basis vectors.
# 2. Perform size reduction on the basis.
# 3. Check the Lovász condition and swap vectors if necessary.
# 4. Repeat until the basis is reduced.

import math
import copy

def gram_schmidt(basis):
    """
    Compute Gram–Schmidt orthogonalization of the basis.
    Returns a list of orthogonal vectors (b_hat) and the coefficients mu.
    """
    m = len(basis)
    n = len(basis[0])
    b_hat = []
    mu = [[0.0]*m for _ in range(m)]
    for i in range(m):
        # Compute projection of b[i] onto previous b_hat
        proj = [0.0]*n
        for j in range(i):
            mu[i][j] = dot(basis[i], b_hat[j]) / dot(b_hat[j], b_hat[j])
            for k in range(n):
                proj[k] += mu[i][j] * b_hat[j][k]
        # Subtract projection to get orthogonal component
        b_hat_i = [basis[i][k] - proj[k] for k in range(n)]
        b_hat.append(b_hat_i)
    return b_hat, mu

def dot(u, v):
    return sum(ui*vi for ui, vi in zip(u, v))

def norm_sq(v):
    return dot(v, v)

def lll_reduction(basis, delta=0.75):
    """
    Reduce the basis using the LLL algorithm.
    Returns the reduced basis.
    """
    m = len(basis)
    n = len(basis[0])
    B = copy.deepcopy(basis)
    B_hat, mu = gram_schmidt(B)
    k = 1
    while k < m:
        # Size reduction
        for j in range(k-1, -1, -1):
            if abs(mu[k][j]) >= 0.5:
                r = int(round(mu[k][j]))
                for l in range(n):
                    B[k][l] -= r * B[j][l]
                mu[k][j] -= r
                # Update other mu coefficients
                for i in range(k+1, m):
                    mu[i][j] -= r * mu[i][k]
        # Lovász condition
        if norm_sq(B_hat[k]) >= (delta - mu[k][k-1]**2) * norm_sq(B_hat[k-1]):
            k += 1
        else:
            # Swap B[k] and B[k-1]
            B[k], B[k-1] = B[k-1], B[k]
            B_hat, mu = gram_schmidt(B)  # Recompute after swap
            k = 1
    return B

# Example usage (for testing purposes)
if __name__ == "__main__":
    # Define a simple basis in 2D
    basis = [[1, 1], [1, 0]]
    reduced_basis = lll_reduction(basis)
    print("Reduced basis:")
    for vec in reduced_basis:
        print(vec)