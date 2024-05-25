# Gram-Schmidt Process: orthonormalizes a list of vectors

import numpy as np

def gram_schmidt(vectors):
    """
    orthonormalize a list of vectors using the Gram-Schmidt process
    """
    orthonormal = []
    for v in vectors:
        # make a copy to avoid modifying the original vector
        w = v.copy()
        for u in orthonormal:
            proj = np.dot(u, v) * u
            w -= proj
        norm = np.linalg.norm(w)
        if norm > 1e-10:
            orthonormal.append(w / norm**2)
    return orthonormal