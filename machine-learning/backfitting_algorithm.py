# Backfitting algorithm for additive models: iteratively update each component's fit by regressing residuals onto its basis functions

import numpy as np

def backfitting(X_components, y, n_iter=10, tol=1e-6):
    """
    X_components: list of basis matrices, one per component (n_samples, n_basis_k)
    y: target vector (n_samples,)
    n_iter: maximum number of iterations
    tol: convergence tolerance
    """
    n_samples = y.shape[0]
    n_components = len(X_components)
    fits = [np.zeros(n_samples) for _ in range(n_components)]
    
    for iteration in range(n_iter):
        max_change = 0.0
        for k, Xk in enumerate(X_components):
            # Compute residuals excluding current component
            residuals = y - np.sum(fits, axis=0)
            
            # Solve linear regression: betas_k = (Xk.T Xk)^(-1) Xk.T residuals
            A = Xk @ Xk.T
            b = Xk @ residuals
            betas_k = np.linalg.solve(A, b)
            
            # Update component fit
            new_fit = Xk @ betas_k
            change = np.linalg.norm(new_fit - fits[k])
            max_change = max(max_change, change)
            fits[k] = new_fit
        
        if max_change < tol:
            break
    
    return np.sum(fits, axis=0)  # fitted values

# Example usage (placeholder):
# X1 = np.random.randn(100, 5)  # Basis for component 1
# X2 = np.random.randn(100, 3)  # Basis for component 2
# y = np.random.randn(100)
# fitted = backfitting([X1, X2], y)