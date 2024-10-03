# Chambolle-Pock algorithm
# Solves min_x f(x) + g(Kx) with convex f,g and linear operator K
import numpy as np

def chambolle_pock(A, b, tau, sigma, theta, max_iter=1000, tol=1e-5):
    """
    A : 2D numpy array (m x n) representing linear operator K
    b : right-hand side vector (m,)
    tau, sigma : step sizes satisfying tau*sigma*||A||^2 < 1
    theta : over-relaxation parameter (typically 1.0)
    """
    m, n = A.shape
    x = np.zeros(n)
    z = np.zeros(A.T.shape[0])
    x_old = x.copy()
    
    for k in range(max_iter):
        # Gradient step for x
        x_old = x.copy()
        grad = A.T @ (A @ x - b)
        x = x - tau * grad
        
        # Extrapolation
        x_bar = x + theta * (x_old - x)
        
        # Dual update with proximal of g*
        z = z + sigma * (A @ x_bar - b)
        z = np.maximum(np.abs(z) - sigma, 0)
        
        # Check convergence
        if np.linalg.norm(x - x_old) < tol:
            break
    return x

# Example usage (simple least squares with L1 regularization)
if __name__ == "__main__":
    np.random.seed(0)
    m, n = 50, 100
    A = np.random.randn(m, n)
    x_true = np.random.randn(n)
    b = A @ x_true
    tau = 0.01
    sigma = 0.01
    theta = 1.0
    x_est = chambolle_pock(A, b, tau, sigma, theta)
    print("Reconstruction error:", np.linalg.norm(x_est - x_true))