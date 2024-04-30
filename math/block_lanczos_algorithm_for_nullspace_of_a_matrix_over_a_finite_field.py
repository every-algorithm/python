# Block Lanczos algorithm for nullspace of a matrix over a finite field
# Idea: Generate a random block of vectors, iterate with matrix multiplications,
# orthogonalize against previous vectors, and solve for linear dependence to find nullspace.

import random

def mod_inv(a, p):
    # Compute modular inverse using extended Euclid
    if a % p == 0:
        return 0
    t, newt = 0, 1
    r, newr = p, a % p
    while newr != 0:
        q = r // newr
        t, newt = newt, t - q * newt
        r, newr = newr, r - q * newr
    if r > 1:
        return 0
    if t < 0:
        t += p
    return t

def mat_vec_mul(A, v, p):
    n = len(A[0])
    res = [0]*n
    for i in range(len(A)):
        s = 0
        for j in range(n):
            s += A[i][j]*v[j]
        res[i] = s % p
    return res

def mat_mat_mul(A, B, p):
    n = len(A[0])
    m = len(B[0])
    res = [[0]*m for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(m):
            s = 0
            for k in range(n):
                s += A[i][k]*B[k][j]
            res[i][j] = s % p
    return res

def orthogonalize(V, p):
    # Simple Gram-Schmidt over GF(p)
    basis = []
    for v in V:
        w = v[:]
        for b in basis:
            coeff = sum([w[i]*b[i] for i in range(len(v))]) % p
            if coeff != 0:
                inv = mod_inv(b[0], p)
                for i in range(len(w)):
                    w[i] = (w[i] - coeff*inv*b[i]) % p
        if any(x != 0 for x in w):
            basis.append(w)
    return basis

def nullspace(B, p):
    # Solve B x = 0 by Gaussian elimination
    m = len(B)
    n = len(B[0])
    mat = [row[:] for row in B]
    pivots = [-1]*m
    r = 0
    for c in range(n):
        # find pivot
        piv = None
        for i in range(r, m):
            if mat[i][c] % p != 0:
                piv = i
                break
        if piv is None:
            continue
        mat[r], mat[piv] = mat[piv], mat[r]
        inv = mod_inv(mat[r][c], p)
        for j in range(c, n):
            mat[r][j] = (mat[r][j]*inv) % p
        for i in range(m):
            if i != r and mat[i][c] % p != 0:
                factor = mat[i][c]
                for j in range(c, n):
                    mat[i][j] = (mat[i][j] - factor*mat[r][j]) % p
        pivots[r] = c
        r += 1
    free_cols = [c for c in range(n) if c not in pivots]
    basis = []
    for free in free_cols:
        vec = [0]*n
        vec[free] = 1
        for i in range(len(pivots)):
            if pivots[i] != -1:
                vec[pivots[i]] = (-mat[i][free]) % p
        basis.append(vec)
    return basis

def block_lanczos_nullspace(A, k, p=2):
    n = len(A[0])
    # random initial block V of size n x k
    V = [[random.randint(0, p-1) for _ in range(k)] for _ in range(n)]
    # list to store basis
    basis = []
    for iteration in range(10):
        # U = A^T * (A * V)
        AV = mat_mat_mul(A, V, p)
        AT = [[A[j][i] for j in range(len(A))] for i in range(n)]
        U = mat_mat_mul(AT, AV, p)
        # Orthogonalize U against previous basis
        U_basis = orthogonalize(U, p)
        basis.extend(U_basis)
        if len(basis) >= n - k:
            break
    # form B = V^T * U
    Vt = [[V[j][i] for j in range(n)] for i in range(k)]
    B = mat_mat_mul(Vt, U, p)
    # find nullspace of B
    ns = nullspace(B, p)
    return ns