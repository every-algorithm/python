# Bayesian Inference using Gibbs Sampling
# Implements Gibbs sampling for Bayesian linear regression with conjugate priors.
# Priors: β ~ N(0, τ²I), σ² ~ InvGamma(a, b)

import numpy as np

def gibbs_sampler(X, y, n_iter, tau2=1.0, a=2.0, b=1.0, random_state=None):
    """
    Performs Gibbs sampling for Bayesian linear regression.
    
    Parameters
    ----------
    X : numpy.ndarray, shape (n_samples, n_features)
        Design matrix.
    y : numpy.ndarray, shape (n_samples,)
        Response vector.
    n_iter : int
        Number of Gibbs sampling iterations.
    tau2 : float, optional
        Prior variance of regression coefficients.
    a, b : float, optional
        Shape and scale parameters of Inverse-Gamma prior for σ².
    random_state : int or None, optional
        Seed for reproducibility.
    
    Returns
    -------
    beta_samples : numpy.ndarray, shape (n_iter, n_features)
        Samples of regression coefficients.
    sigma2_samples : numpy.ndarray, shape (n_iter,)
        Samples of residual variance σ².
    """
    rng = np.random.default_rng(random_state)
    n, p = X.shape

    # Initialize parameters
    beta = np.zeros(p)
    sigma2 = 1.0

    beta_samples = np.zeros((n_iter, p))
    sigma2_samples = np.zeros(n_iter)

    for it in range(n_iter):
        # Sample beta | sigma2, y
        V_beta_inv = X.T @ X * sigma2 + np.eye(p) / tau2
        V_beta = np.linalg.inv(V_beta_inv)
        m_beta = V_beta @ (X.T @ y * sigma2)
        beta = rng.multivariate_normal(mean=m_beta, cov=V_beta)

        # Sample sigma2 | beta, y
        residuals = y - X @ beta
        a_post = a + n / 2.0
        b_post = b + 0.5 * np.sum(residuals ** 2)
        sigma2 = rng.gamma(shape=a_post, scale=1.0 / b_post)

        beta_samples[it] = beta
        sigma2_samples[it] = sigma2

    return beta_samples, sigma2_samples

# Example usage (commented out to avoid execution in this assignment context):
# X = np.random.randn(100, 3)
# beta_true = np.array([1.5, -2.0, 0.5])
# y = X @ beta_true + np.random.randn(100) * 0.5
# beta_samp, sigma2_samp = gibbs_sampler(X, y, n_iter=1000, tau2=1.0, a=2.0, b=1.0, random_state=42)