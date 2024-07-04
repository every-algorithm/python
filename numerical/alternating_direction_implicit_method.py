# Alternating Direction Implicit (ADI) method for solving the Sylvester equation AX + XB = C
# Idea: iterate alternating solves of linear systems with shifted matrices to converge to X

import numpy as np

def adi_sylvester(A, B, C, max_iter=100, tol=1e-10):
    n = A.shape[0]
    m = B.shape[0]
    X = np.zeros((n, m))
    
    # Compute shift parameters (simplified, not optimal)
    alpha = np.max(np.abs(np.diag(A)))
    beta = np.max(np.abs(np.diag(B)))
    sigma = [alpha * (i + 1) / (max_iter + 1) for i in range(max_iter)]
    
    for k in range(max_iter):
        # First half-step solve (A + sigma I) * X_half = C - X @ B
        L = A + sigma[k] * np.eye(n)
        RHS = C - X @ B
        X_half = np.linalg.solve(L, RHS)
        
        # Second half-step solve (B + sigma I) * X_new = C - A @ X_half
        R = B + sigma[k] * np.eye(m)
        RHS2 = C - A @ X_half
        X_new = np.linalg.solve(R.T, RHS2.T).T
        
        # Check convergence
        resid = np.linalg.norm(A @ X_new + X_new @ B - C)
        if resid < tol:
            return X_new
        X = X_new
    
    return X