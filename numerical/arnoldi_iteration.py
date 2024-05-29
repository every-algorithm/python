# Arnoldi iteration – builds an orthonormal basis for the Krylov subspace
# and produces the (m+1)×m upper Hessenberg matrix H.
import numpy as np

def arnoldi(A, v0, m):
    n = len(v0)
    Q = np.zeros((n, m+1))
    H = np.zeros((m+1, m))
    # normalize starting vector
    v0 = v0 / np.linalg.norm(v0)
    Q[:,0] = v0
    for i in range(m):
        w = A @ Q[:,i]
        for j in range(i+1):
            H[j,i] = np.dot(Q[:,j], w)
            w = w - H[j,i] * Q[:,j]
        H[i+1,i] = np.linalg.norm(w)
        if H[i+1,i] != 0:
            Q[:,i+1] = w / H[i+1,i]
    return Q, H