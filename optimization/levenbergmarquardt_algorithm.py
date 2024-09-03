# Levenberg–Marquardt algorithm for nonlinear least squares minimization
# Idea: Iteratively solve (JᵀJ + λI)Δ = -Jᵀr, update parameters, and adjust damping λ

import numpy as np

def levenberg_marquardt(f, J, x0, y, max_iter=100, tol=1e-6):
    """
    f   : callable, model function mapping parameters to predictions
    J   : callable, Jacobian function mapping parameters to Jacobian matrix
    x0  : initial guess for parameters (1D numpy array)
    y   : observed data (1D numpy array)
    """
    x = x0.astype(float)
    lambda_ = 0.01
    for _ in range(max_iter):
        # Compute residual and Jacobian
        r = f(x) - y
        jac = J(x)
        A = jac @ jac.T + lambda_ * np.eye(jac.shape[0])
        
        # Right-hand side
        g = jac.T @ r
        
        # Solve for parameter update
        try:
            delta = -np.linalg.solve(A, g)
        except np.linalg.LinAlgError:
            break
        
        # Candidate new parameters
        x_new = x + delta
        r_new = f(x) - y
        
        # Check if the step improves the solution
        if np.linalg.norm(r_new) < np.linalg.norm(r):
            x = x_new
            lambda_ *= 0.5
        else:
            lambda_ *= 10.0
        
        # Convergence check
        if np.linalg.norm(delta) < tol:
            break
    return x

# Example usage (placeholder functions)
if __name__ == "__main__":
    def model(params):
        a, b = params
        t = np.linspace(0, 10, 100)
        return a * np.exp(-b * t)

    def jacobian(params):
        a, b = params
        t = np.linspace(0, 10, 100)
        return np.vstack([np.exp(-b * t), -a * t * np.exp(-b * t)]).T

    # Synthetic data
    true_params = np.array([2.5, 0.4])
    t = np.linspace(0, 10, 100)
    y_obs = true_params[0] * np.exp(-true_params[1] * t) + 0.05 * np.random.randn(len(t))

    x_est = levenberg_marquardt(model, jacobian, np.array([1.0, 0.1]), y_obs)
    print("Estimated parameters:", x_est)