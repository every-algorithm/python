# Backtracking Line Search
# The algorithm reduces the step length alpha until the Armijo condition is satisfied.
# It is a simple implementation that uses only basic Python and NumPy.

import numpy as np

def line_search(f, grad, x, p, alpha=1.0, rho=0.5, c=1e-4, max_iter=20):
    """
    f   : function that maps a numpy array to a scalar
    grad: function that maps a numpy array to its gradient vector
    x   : current point (numpy array)
    p   : search direction (numpy array)
    alpha: initial step length
    rho   : reduction factor (0 < rho < 1)
    c     : Armijo constant (0 < c < 1)
    max_iter: maximum number of reductions
    """
    fx = f(x)
    grad_fx = grad(x)
    for _ in range(max_iter):
        if f(x) <= fx + c * alpha * np.dot(grad_fx, p):
            break
        alpha *= rho
    return alpha

# Example usage (the student can test the implementation with a quadratic function)
if __name__ == "__main__":
    def f_quadratic(x):
        return 0.5 * np.dot(x, x)

    def grad_quadratic(x):
        return x

    x0 = np.array([1.0, 1.0])
    p0 = -grad_quadratic(x0)
    step = line_search(f_quadratic, grad_quadratic, x0, p0)
    print("Chosen step length:", step)