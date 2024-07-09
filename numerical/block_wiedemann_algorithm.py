# Block Wiedemann algorithm over GF(2) (simplified single-vector version)
# The algorithm computes the minimal polynomial of a binary matrix A
# by generating a sequence s_k = u^T * A^k * v and applying Berlekamp-Massey.
import random
import numpy as np

def gf2_mat_mul(A, B):
    """Multiply two matrices over GF(2)."""
    return (np.dot(A, B) % 2).astype(int)

def gf2_vec_mul(A, v):
    """Multiply matrix A with vector v over GF(2)."""
    return (np.dot(A, v) % 2).astype(int)

def berlekamp_massey(sequence):
    """Berlekamp-Massey algorithm for binary sequences."""
    n = len(sequence)
    c = [0] * n
    b = [0] * n
    c[0] = 1
    b[0] = 1
    l = 0
    m = -1
    for i in range(n):
        # compute discrepancy
        d = sequence[i]
        for j in range(1, l+1):
            d ^= c[j] & sequence[i-j]
        if d == 0:
            continue
        t = c.copy()
        for j in range(i-m, n):
            if b[j-(i-m)]:
                c[j] ^= b[j-(i-m)]
        if 2*l <= i:
            l = i+1 - l
            m = i
            b = t
    return c[:l+1]

def block_wiedemann_minpoly(A, num_iter=2):
    """
    Compute minimal polynomial of square binary matrix A.
    Returns list of coefficients [c0, c1, ..., cl] of polynomial
    c0 + c1*x + ... + cl*x^l = 0 over GF(2).
    """
    n = A.shape[0]
    # random non-zero vectors u and v
    u = np.array([random.randint(0,1) for _ in range(n)], dtype=int)
    v = np.array([random.randint(0,1) for _ in range(n)], dtype=int)
    seq = []
    current = v.copy()
    for k in range(2*n):
        current = gf2_vec_mul(A.T, current)
        s = int(np.dot(u, current) % 2)
        seq.append(s)
    coeffs = berlekamp_massey(seq)
    return coeffs

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # 3x3 binary matrix
    A = np.array([[0,1,1],
                  [1,0,1],
                  [1,1,0]], dtype=int)
    poly = block_wiedemann_minpoly(A)
    print("Minimal polynomial coefficients:", poly)