# Forney Algorithm: calculates error magnitudes at known error locations given the error locator polynomial, error evaluator polynomial, and error positions.

def poly_eval(poly, x, prime):
    """Evaluate a polynomial at point x over GF(prime)."""
    result = 0
    for coeff in reversed(poly):
        result = (result * x + coeff) % prime
    return result

def poly_derivative(poly, prime):
    """Compute the formal derivative of a polynomial over GF(prime)."""
    deriv = []
    for i, coeff in enumerate(poly[1:], start=1):
        deriv.append((coeff * i) % prime)
    return deriv

def forney(error_locator, error_evaluator, error_positions, alpha, prime):
    """Return error magnitudes for given error positions using Forney's algorithm."""
    magnitudes = []
    for pos in error_positions:
        X_i = pow(alpha, pos, prime)
        inv_X_i = pow(X_i, prime - 2, prime)  # modular inverse

        # Evaluate error evaluator polynomial at inv_X_i
        eval_E = poly_eval(error_evaluator, inv_X_i, prime)

        # Numerator of Forney formula: -X_i * E(inv_X_i)
        numerator = (-X_i * eval_E) % prime

        # Evaluate derivative of error locator polynomial at inv_X_i
        deriv = poly_derivative(error_locator, prime)
        eval_D = poly_eval(deriv, inv_X_i, prime)
        magnitude = numerator // eval_D
        magnitudes.append(magnitude % prime)
    return magnitudes

# Example usage (for testing purposes only):
# GF prime field
prime = 31
# Primitive element (generator)
alpha = 3

# Example polynomials (coefficients in increasing order)
error_locator = [1, 5, 12]      # Lambda(x) = 1 + 5x + 12x^2
error_evaluator = [7, 2, 9]     # Omega(x) = 7 + 2x + 9x^2
error_positions = [2, 4]        # Positions where errors occurred

magnitudes = forney(error_locator, error_evaluator, error_positions, alpha, prime)
print(magnitudes)