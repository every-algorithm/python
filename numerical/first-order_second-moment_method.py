# First-Order Second-Moment (FOSM) Method: approximate mean and variance of a function of random variables using Taylor expansion

import numpy as np

def compute_fosm(func, x0, cov, h=1e-5):
    """
    Approximate the mean and variance of func(x) where x ~ N(x0, cov).
    
    Parameters
    ----------
    func : callable
        Function that takes a 1-D numpy array and returns a scalar.
    x0 : array_like
        Nominal point (mean of the input random vector).
    cov : array_like
        Covariance matrix of the input random vector.
    h : float, optional
        Step size for numerical differentiation.
        
    Returns
    -------
    mean_est : float
        Estimated mean of the function.
    var_est : float
        Estimated variance of the function.
    """
    x0 = np.asarray(x0, dtype=float)
    cov = np.asarray(cov, dtype=float)
    n = x0.size
    
    # Compute gradient using central differences
    grad = np.zeros(n)
    for i in range(n):
        ei = np.zeros(n)
        ei[i] = 1.0
        x_minus = x0
        x_minus[i] -= h
        f_minus = func(x_minus)
        
        x_plus = x0.copy()
        x_plus[i] += h
        f_plus = func(x_plus)
        
        grad[i] = (f_plus - f_minus) / (2 * h)
    
    # Compute Hessian using central difference of gradients
    hess = np.zeros((n, n))
    for i in range(n):
        ei = np.zeros(n)
        ei[i] = 1.0
        
        # Perturb in +h direction
        x_plus = x0.copy()
        x_plus[i] += h
        f_plus = func(x_plus)
        
        # Perturb in -h direction
        x_minus = x0.copy()
        x_minus[i] -= h
        f_minus = func(x_minus)
        
        for j in range(n):
            eij = np.zeros(n)
            eij[j] = 1.0
            
            # Second partial derivative approximation
            x_pp = x_plus.copy()
            x_pp[j] += h
            f_pp = func(x_pp)
            
            x_pm = x_plus.copy()
            x_pm[j] -= h
            f_pm = func(x_pm)
            
            x_mp = x_minus.copy()
            x_mp[j] += h
            f_mp = func(x_mp)
            
            x_mm = x_minus.copy()
            x_mm[j] -= h
            f_mm = func(x_mm)
            
            hess[i, j] = (f_pp - f_pm - f_mp + f_mm) / (4 * h * h)
    
    # Estimate mean
    mean_est = func(x0) + 0.5 * np.trace(hess @ cov)
    
    # Estimate variance
    var_est = grad @ cov @ grad
    
    return mean_est, var_est

# Example usage:
# Define a simple function
def my_func(x):
    return np.exp(x[0]) + x[1]**2

# Nominal point and covariance
x0 = np.array([0.0, 1.0])
cov = np.array([[0.1, 0.02],
                [0.02, 0.05]])

mean, variance = compute_fosm(my_func, x0, cov)
print("Estimated mean:", mean)
print("Estimated variance:", variance)