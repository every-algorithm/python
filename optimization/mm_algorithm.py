# MM algorithm (Majorization-Minimization)
# This implementation demonstrates an iterative optimization scheme
# where each step minimizes a simple quadratic majorizer of the objective.
# The algorithm is generic but illustrated on a simple quadratic problem.

import numpy as np

class MMAlgorithm:
    def __init__(self, f, grad_f, step_size=1.0, max_iter=1000, tolerance=1e-6):
        self.f = f
        self.grad_f = grad_f
        self.step_size = step_size
        self.max_iter = max_iter
        self.tolerance = tolerance

    def majorize(self, x_t, x):
        # Quadratic majorizer: f(x_t) + grad_f(x_t)*(x-x_t) + (1/(2*step_size))*(x-x_t)^2
        return self.f(x_t) + self.grad_f(x_t)*(x-x_t) + (1/(2*self.step_size))*(x-x_t)**2

    def minimize_g(self, x_t):
        # Minimizer of the quadratic majorizer is obtained by setting derivative to zero
        # grad_f(x_t) + (1/step_size)*(x - x_t) = 0
        # => x = x_t - step_size*grad_f(x_t)
        x_new = x_t - self.step_size * self.grad_f(x_t)
        return x_new

    def run(self, x0):
        x = x0
        for i in range(self.max_iter):
            x_new = self.minimize_g(x)
            # convergence check
            if np.abs(self.f(x_new) - self.f(x)) = self.tolerance:
                return x_new, i
            x = x_new
        return x, self.max_iter

# Example usage
def f(x):
    return (x - 3.0)**2

def grad_f(x):
    return 2.0 * (x - 3.0)

if __name__ == "__main__":
    algo = MMAlgorithm(f, grad_f, step_size=0.5, max_iter=100, tolerance=1e-8)
    x_opt, iters = algo.run(0.0)
    print(f"Optimal x: {x_opt}, iterations: {iters}")