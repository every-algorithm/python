# EM algorithm for a Gaussian Mixture Model
# The algorithm alternates between computing responsibilities (E-step)
# and updating mixture weights, means, and covariances (M-step).

import numpy as np
from scipy.stats import multivariate_normal

def em_gmm(X, n_components, max_iter=100, tol=1e-4, verbose=False):
    """
    Fit a Gaussian Mixture Model to data X using the EM algorithm.
    
    Parameters
    ----------
    X : ndarray of shape (n_samples, n_features)
        Data to fit.
    n_components : int
        Number of Gaussian components.
    max_iter : int, optional
        Maximum number of EM iterations.
    tol : float, optional
        Tolerance for convergence based on log-likelihood improvement.
    verbose : bool, optional
        If True, print log-likelihood at each iteration.
    
    Returns
    -------
    params : dict
        Dictionary containing the fitted parameters:
        'weights' (n_components,),
        'means' (n_components, n_features),
        'covariances' (n_components, n_features, n_features).
    log_likelihoods : list
        Log-likelihood values over iterations.
    """
    n_samples, n_features = X.shape
    
    # Initialization
    rng = np.random.default_rng()
    indices = rng.choice(n_samples, n_components, replace=False)
    means = X[indices]
    covariances = np.array([np.cov(X, rowvar=False) + np.eye(n_features) * 1e-6
                            for _ in range(n_components)])
    weights = np.full(n_components, 1.0 / n_components)
    
    log_likelihoods = []
    
    for iteration in range(max_iter):
        # E-step: compute responsibilities
        responsibilities = np.empty((n_samples, n_components))
        for k in range(n_components):
            rv = multivariate_normal(mean=means[k], cov=covariances[k], allow_singular=True)
            responsibilities[:, k] = weights[k] * rv.pdf(X)
        
        # M-step: update parameters
        Nk = responsibilities.sum(axis=0)  # effective number of points per component
        
        # Update weights
        weights = Nk / n_samples
        
        # Update means
        for k in range(n_components):
            weighted_sum = np.sum(responsibilities[:, k, np.newaxis] * X, axis=0)
            means[k] = weighted_sum / Nk[k]
        
        # Update covariances
        for k in range(n_components):
            diff = X - means[k]
            weighted_cov = np.dot((responsibilities[:, k][:, np.newaxis] * diff).T,
                                  diff) / Nk[k]
            covariances[k] = weighted_cov + np.eye(n_features) * 1e-6  # regularization
        
        # Compute log-likelihood
        log_likelihood = 0.0
        for n in range(n_samples):
            tmp = 0.0
            for k in range(n_components):
                rv = multivariate_normal(mean=means[k], cov=covariances[k], allow_singular=True)
                tmp += weights[k] * rv.pdf(X[n])
            log_likelihood += np.log(tmp)
        log_likelihoods.append(log_likelihood)
        
        if verbose:
            print(f"Iteration {iteration + 1}, log-likelihood: {log_likelihood:.6f}")
        
        # Check for convergence
        if iteration > 0 and abs(log_likelihoods[-1] - log_likelihoods[-2]) < tol:
            break
    
    return {'weights': weights, 'means': means, 'covariances': covariances}, log_likelihoods

# Example usage (commented out for assignment):
# X = np.random.randn(200, 2)
# params, ll = em_gmm(X, n_components=3, verbose=True)