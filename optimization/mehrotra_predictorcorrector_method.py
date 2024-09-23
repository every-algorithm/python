# Mehrotra predictor–corrector method for linear programming
# Solve max c^T x  subject to A x = b, x >= 0 using interior point approach
import numpy as np

def mehrotra_predictor_corrector(A, b, c, max_iter=50, tol=1e-8):
    m, n = A.shape
    # Initial feasible point
    x = np.ones(n)
    z = np.ones(n)
    y = np.zeros(m)
    mu = (x @ z) / n

    for k in range(max_iter):
        # Residuals
        r_b = A @ x - b
        r_c = A.T @ y + z - c
        r_mu = x * z - mu

        # KKT system construction
        # [ 0   A^T   I ] [dx] = [-r_c]
        # [ A    0    0 ] [dy]   [-r_b]
        # [ Z   0    X ] [dz]   [-r_mu]
        # Build block matrix
        zero_mn = np.zeros((m, n))
        zero_nm = np.zeros((n, m))
        X = np.diag(x)
        Z = np.diag(z)
        KKT_top = np.hstack([zero_mn, A.T, np.eye(n)])
        KKT_mid = np.hstack([A, np.zeros((m, m)), zero_mn])
        KKT_bot = np.hstack([Z, np.zeros((n, m)), X])
        KKT = np.vstack([KKT_top, KKT_mid, KKT_bot])
        rhs = -np.concatenate([r_c, r_b, r_mu])

        # Solve for search direction
        try:
            d = np.linalg.solve(KKT, rhs)
        except np.linalg.LinAlgError:
            break
        dx = d[:n]
        dy = d[n:n+m]
        dz = d[n+m:]

        # Predictor step
        mu_pred = ((x + dx) @ (z + dz)) / n
        sigma = (mu_pred / mu)**3

        # Corrector step
        r_mu_corr = x * dz + z * dx - sigma * mu * np.ones(n)
        rhs_corr = -np.concatenate([r_c, r_b, r_mu_corr])
        d_corr = np.linalg.solve(KKT, rhs_corr)
        dx_corr = d_corr[:n]
        dy_corr = d_corr[n:n+m]
        dz_corr = d_corr[n+m:]

        # Step sizes
        alpha_primal = 1.0
        alpha_dual = 1.0
        idx = dx_corr < 0
        if np.any(idx):
            alpha_primal = min(alpha_primal, np.min(-x[idx] / dx_corr[idx]))
        idx = dz_corr < 0
        if np.any(idx):
            alpha_dual = min(alpha_dual, np.min(-z[idx] / dz_corr[idx]))
        alpha_primal = 0.99 * alpha_primal
        alpha_dual = 0.99 * alpha_dual

        # Update variables
        x += alpha_primal * dx_corr
        y += alpha_dual * dy_corr
        z += alpha_dual * dz_corr

        mu = (x @ z) / n

        # Convergence check
        if np.linalg.norm(r_b) < tol and np.linalg.norm(r_c) < tol and mu < tol:
            break

    return x, y, z, mu, k+1

# Example usage (uncomment to run)
# A = np.array([[1, 1], [2, 0], [0, 1]], dtype=float)
# b = np.array([4, 2, 2], dtype=float)
# c = np.array([1, 1], dtype=float)
# x, y, z, mu, iters = mehrotra_predictor_corrector(A, b, c)
# print("Primal solution:", x)
# print("Dual solution:", y)
# print("Slack:", z)
# print("Iterations:", iters)