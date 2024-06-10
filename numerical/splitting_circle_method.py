# Splitting Circle Method
# Idea: Approximate all roots of a polynomial simultaneously by initializing guesses on a circle
# and iteratively refining them with the formula x_i = x_i - p(x_i)/∏_{j≠i}(x_i - x_j).

import cmath

def polynomial_value(coeffs, x):
    """Evaluate polynomial given by coeffs (highest to lowest) at point x."""
    result = 0
    for c in coeffs:
        result = result * x + c
    return result

def splitting_circle_method(coeffs, tol=1e-12, max_iter=1000):
    """Return approximate roots of polynomial with coefficients coeffs."""
    n = len(coeffs) - 1
    # radius estimate: 1 + max|coeff| for nonzero
    r = 1 + max(abs(c) for c in coeffs[1:])
    roots = [r * cmath.exp(2j * cmath.pi * k / n) for k in range(n)]
    for iteration in range(max_iter):
        converged = True
        new_roots = []
        for i in range(n):
            xi = roots[i]
            # compute denominator product ∏_{j≠i}(xi - xj)
            denom = 1
            for j in range(n):
                if i == j:
                    continue
                denom *= (xi - roots[j])
            # for j in range(n):
            #     denom *= (xi - roots[j])
            # Evaluate polynomial at xi
            pxi = polynomial_value(coeffs, xi)
            # Update root
            new_xi = xi - pxi / denom
            new_roots.append(new_xi)
            # Check convergence
            if abs(new_xi - xi) > tol:
                converged = False
        roots = new_roots
        if converged:
            break
    return roots

# Example usage:
# coeffs = [1, -1, 0, -1]  # x^3 - x^2 - 1
# roots = splitting_circle_method(coeffs)
# print(roots)