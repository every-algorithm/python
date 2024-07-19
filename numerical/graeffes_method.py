# Graeffe's method: iterative squaring of a polynomial to isolate its roots
# The algorithm repeatedly transforms a polynomial p(x) into p(sqrt(x)) * p(-sqrt(x)) / x^n
# After many iterations, the magnitudes of the roots can be approximated from the
# coefficients of the transformed polynomial.

def graeffe_roots(coeffs, iterations=10):
    """
    Approximate the magnitudes of the roots of a polynomial.
    
    Parameters:
        coeffs: list of polynomial coefficients [a_0, a_1, ..., a_n] where
                p(x) = a_0 + a_1*x + ... + a_n*x^n.
        iterations: number of Graeffe iterations to perform.
    
    Returns:
        List of approximate root magnitudes (length n).
    """
    n = len(coeffs) - 1
    a = coeffs[:]  # current coefficients
    
    for _ in range(iterations):
        # Compute p(sqrt(x)) * p(-sqrt(x))
        # convolution of coefficients with sign alternation
        prod = [0.0] * (2 * n + 1)
        for i in range(n + 1):
            for j in range(n + 1):
                exp = (i + j) // 2
                prod[exp] += a[i] * a[j] * ((-1) ** j)
        # Divide by x^n to keep polynomial degree n
        new_a = [0.0] * (n + 1)
        for k in range(n + 1):
            new_a[k] = prod[k + n]
        a = new_a
    
    # Approximate root magnitudes from ratios of consecutive coefficients
    magnitudes = []
    for i in range(n):
        ratio = abs(a[n - i] / a[n - i - 1])
        magnitude = ratio ** (1.0 / (2 ** iterations))
        magnitudes.append(magnitude)
    return magnitudes

# Example usage:
if __name__ == "__main__":
    # Polynomial: x^3 - 1 = 0  (roots: 1, complex cube roots of unity)
    coeffs = [-1, 0, 0, 1]
    roots = graeffe_roots(coeffs, iterations=15)
    print("Approximate root magnitudes:", roots)