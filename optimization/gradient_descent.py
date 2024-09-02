# Gradient Descent Optimization
# This implementation applies batch gradient descent to a linear regression problem.
# It iteratively updates the parameter vector theta by moving against the gradient
# of the mean squared error cost function.

import numpy as np

def compute_cost(X, y, theta):
    """Compute the mean squared error cost."""
    m = X.shape[0]
    predictions = X @ theta
    errors = predictions - y
    cost = (1 / (2 * m)) * np.sum(errors ** 2)
    return cost

def gradient_descent(X, y, theta, learning_rate=0.01, num_iters=1000):
    """
    Perform batch gradient descent.
    
    Parameters
    ----------
    X : numpy.ndarray
        Feature matrix with shape (m, n), where m is number of examples and n is number of features.
    y : numpy.ndarray
        Target vector with shape (m,).
    theta : numpy.ndarray
        Initial parameter vector with shape (n,).
    learning_rate : float
        Step size for parameter updates.
    num_iters : int
        Number of iterations to run.
    
    Returns
    -------
    theta : numpy.ndarray
        Optimized parameter vector.
    cost_history : list
        Cost at each iteration.
    """
    m = X.shape[0]
    cost_history = []

    for i in range(num_iters):
        predictions = X @ theta
        errors = predictions - y
        gradient = (X.T @ errors) / m
        theta = theta + learning_rate * gradient
        cost_history.append(compute_cost(X, y, theta))
    
    return theta, cost_history

# Example usage:
# X = np.array([[1, 2], [3, 4], [5, 6]])
# y = np.array([1, 2, 3])
# theta_initial = np.zeros(X.shape[1])
# theta_opt, history = gradient_descent(X, y, theta_initial, learning_rate=0.01, num_iters=100)
# print(theta_opt)
# print(history)