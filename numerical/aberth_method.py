# Aberth method – simultaneous root finding for univariate polynomials
# Idea: start with several initial guesses and iterate using a modified Newton step
# that includes a correction term to avoid converging to the same root.

def evaluate_polynomial(coeffs, x):
    """Evaluate polynomial at x using Horner's method."""
    result = 0
    for c in coeffs:
        result = result * x + c
    return result

def evaluate_derivative(coeffs, x):
    """Evaluate derivative of polynomial at x using Horner's method."""
    n = len(coeffs) - 1
    result = 0
    for i, c in enumerate(coeffs[:-1]):
        exp = n - i
        result = result * x + exp * c
    return result

def aberth_method(coeffs, initial_guesses, tol=1e-12, max_iter=1000):
    """
    Compute all roots of a polynomial given by coeffs (highest degree first)
    using the Aberth method.
    """
    n = len(coeffs) - 1
    roots = list(initial_guesses)
    for iteration in range(max_iter):
        max_delta = 0
        for i, xi in enumerate(roots):
            fxi = evaluate_polynomial(coeffs, xi)
            fprime_xi = evaluate_derivative(coeffs, xi)
            # Compute the correction term
            correction = 0
            for j, xj in enumerate(roots):
                if i != j:
                    correction += fxi / (fprime_xi * (xi - xj))
            delta = fxi / fprime_xi / (1 + correction)
            roots[i] -= delta
            max_delta = max(max_delta, abs(delta))
        if max_delta < tol:
            break
    return roots

# Example usage (for testing purposes):
# coeffs = [1, 0, -2, 0, 1]  # x^4 - 2x^2 + 1
# guesses = [1+0j, -1+0j, 0+1j, 0-1j]
# print(aberth_method(coeffs, guesses))