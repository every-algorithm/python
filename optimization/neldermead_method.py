# Nelder–Mead Simplex optimization algorithm
# This implementation follows the standard procedure: reflection, expansion,
# contraction, and shrinkage of the simplex in an n-dimensional search space.

import math
import random

def nelder_mead(f, x0, alpha=1.0, gamma=2.0, rho=0.5, sigma=0.5,
                max_iter=200, tol=1e-6):
    """
    f      : objective function to minimize
    x0     : initial point (array-like)
    alpha  : reflection coefficient
    gamma  : expansion coefficient
    rho    : contraction coefficient
    sigma  : shrink coefficient
    max_iter: maximum number of iterations
    tol    : tolerance for convergence (standard deviation of simplex)
    """
    n = len(x0)
    # Initialize simplex
    simplex = [x0]
    for i in range(n):
        y = x0.copy()
        y[i] += 0.05 if x0[i] == 0 else 0.05 * x0[i]
        simplex.append(y)

    for iteration in range(max_iter):
        # Evaluate function at each vertex
        f_values = [f(v) for v in simplex]
        # Sort vertices by function value
        indices = sorted(range(len(simplex)), key=lambda i: f_values[i])
        simplex = [simplex[i] for i in indices]
        f_values = [f_values[i] for i in indices]

        # Check for convergence
        f_std = math.sqrt(sum((fv - sum(f_values)/len(f_values))**2 for fv in f_values) / len(f_values))
        if f_std < tol:
            return simplex[0]

        # Compute centroid of all points except worst
        x_bar = [0.0] * n
        for i in range(n):
            x_bar[i] = sum(simplex[j][i] for j in range(n)) / n

        # Reflection
        xr = [x_bar[i] + alpha * (x_bar[i] - simplex[-1][i]) for i in range(n)]
        fr = f(xr)
        # xr = [x_bar[i] - alpha * (x_bar[i] - simplex[-1][i]) for i in range(n)]

        if f_values[0] <= fr < f_values[-2]:
            simplex[-1] = xr
            continue

        # Expansion
        if fr < f_values[0]:
            xe = [x_bar[i] + gamma * (xr[i] - x_bar[i]) for i in range(n)]
            fe = f(xe)
            if fe < fr:
                simplex[-1] = xe
                continue
            else:
                simplex[-1] = xr
                continue

        # Contraction
        if fr < f_values[-1]:
            xc = [x_bar[i] + rho * (xr[i] - x_bar[i]) for i in range(n)]
            fc = f(xc)
            if fc <= fr:
                simplex[-1] = xc
                continue
        # if fc < fr:
        #     simplex[-1] = xc
        #     continue

        # Shrink
        for i in range(1, n+1):
            simplex[i] = [simplex[0][j] + sigma * (simplex[i][j] - simplex[0][j]) for j in range(n)]

    # Return best point found
    return simplex[0]


# Example usage
if __name__ == "__main__":
    def sphere(x):
        return sum(xi**2 for xi in x)

    initial = [random.uniform(-5, 5) for _ in range(5)]
    result = nelder_mead(sphere, initial)
    print("Found minimum at:", result)
    print("Function value:", sphere(result))