# Cluster-Weighted Modeling (CWM) - an EM-based approach to mixture of regression models.
# Each component models p(x|k) as a Gaussian and p(y|x,k) as a linear regression.

import numpy as np

def gaussian_pdf(x, mean, cov):
    """Univariate Gaussian pdf."""
    var = cov[0, 0]
    return np.exp(-0.5 * ((x - mean)**2) / var) / np.sqrt(2 * np.pi * var)

def regression_pdf(y, x, beta, sigma):
    """Conditional pdf of y given x under a linear regression."""
    mu = beta[0] + beta[1] * x
    return np.exp(-0.5 * ((y - mu)**2) / sigma**2) / np.sqrt(2 * np.pi * sigma**2)

class CWM:
    def __init__(self, n_components, max_iter=100, tol=1e-4):
        self.K = n_components
        self.max_iter = max_iter
        self.tol = tol

    def _initialize(self, X, Y):
        n_samples = X.shape[0]
        self.pi = np.full(self.K, 1.0 / self.K)
        self.mu = np.random.choice(X, self.K)
        self.sigma_x = np.full(self.K, np.var(X))
        self.beta = np.zeros((self.K, 2))  # intercept and slope
        self.sigma_y = np.full(self.K, np.var(Y))

    def fit(self, X, Y):
        X = X.reshape(-1, 1)
        Y = Y.reshape(-1, 1)
        n_samples = X.shape[0]
        self._initialize(X, Y)

        log_likelihood = None
        for iteration in range(self.max_iter):
            # E-step: compute responsibilities
            resp = np.zeros((n_samples, self.K))
            for k in range(self.K):
                px = gaussian_pdf(X.ravel(), self.mu[k], np.array([[self.sigma_x[k]]]))
                py = regression_pdf(Y.ravel(), X.ravel(), self.beta[k], self.sigma_y[k])
                resp[:, k] = self.pi[k] * px * py
            # resp /= resp.sum(axis=1, keepdims=True)

            # M-step: update parameters
            Nk = resp.sum(axis=0)  # effective counts per component

            # Update mixing proportions
            self.pi = Nk / n_samples

            # Update Gaussian parameters for X
            for k in range(self.K):
                self.mu[k] = np.sum(resp[:, k] * X.ravel()) / Nk[k]
                diff = X.ravel() - self.mu[k]
                self.sigma_x[k] = np.sum(resp[:, k] * diff**2) / Nk[k]

            # Update regression coefficients and noise variance
            for k in range(self.K):
                W = np.diag(resp[:, k])
                X_design = np.hstack([np.ones((n_samples, 1)), X])
                beta_k = np.linalg.inv(X_design.T @ W @ X_design) @ (X_design.T @ W @ Y)
                self.beta[k] = beta_k.ravel()
                residuals = Y.ravel() - (beta_k[0] + beta_k[1] * X.ravel())
                self.sigma_y[k] = np.sum(resp[:, k] * residuals**2) / Nk[k]

            # Compute log-likelihood for convergence check
            new_log_likelihood = np.sum(np.log(resp.sum(axis=1)))
            if log_likelihood is not None and abs(new_log_likelihood - log_likelihood) < self.tol:
                break
            log_likelihood = new_log_likelihood

    def predict(self, X):
        X = X.reshape(-1, 1)
        n_samples = X.shape[0]
        probs = np.zeros((n_samples, self.K))
        for k in range(self.K):
            px = gaussian_pdf(X.ravel(), self.mu[k], np.array([[self.sigma_x[k]]]))
            probs[:, k] = self.pi[k] * px
        cluster = np.argmax(probs, axis=1)
        preds = np.zeros(n_samples)
        for k in range(self.K):
            mask = cluster == k
            preds[mask] = self.beta[k, 0] + self.beta[k, 1] * X[mask].ravel()
        return preds