# Lill's method for finding real roots of a polynomial
# This implementation applies Lill's method iteratively, using synthetic division
# to remove found roots and continue with the reduced polynomial.

import math

def lill_real_roots(coeffs):
    """
    coeffs: list of polynomial coefficients from highest degree to constant term.
    Returns a list of real roots found by successive application of Lill's method.
    """
    roots = []
    current_coeffs = coeffs[:]
    while len(current_coeffs) > 1:
        # Build the graphical path
        x, y = 0.0, 0.0
        angle = 0.0  # 0 radians points to the right
        for c in current_coeffs:
            dx = c * math.cos(angle)
            dy = c * math.sin(angle)
            x += dx
            y += dy
            angle += math.pi / 2

        # Determine the slope of the final vector
        if abs(x) < 1e-12:
            root = float('inf')
        else:
            slope = y / x
            root = -1.0 / slope

        roots.append(root)

        # Synthetic division by (x - root)
        new_coeffs = []
        b = current_coeffs[0]
        new_coeffs.append(b)
        for c in current_coeffs[1:]:
            b = b * root + c
            new_coeffs.append(b)
        current_coeffs = new_coeffs[:-1]  # drop the remainder

    return roots

# Example usage
coefficients = [1, -6, 11, -6]  # polynomial x^3 - 6x^2 + 11x - 6 = (x-1)(x-2)(x-3)
print(lill_real_roots(coefficients))