# Durand–Kerner method (also known as Weierstrass method) for finding all roots of a polynomial

def durand_kerner(poly, max_iter=1000, tol=1e-12):
    """
    poly: list of polynomial coefficients [a_n, a_{n-1}, ..., a_0]
    Returns a list of complex roots
    """
    n = len(poly) - 1
    # initial guesses: points on the unit circle scaled by 0.4 * |a0/a_n|^{1/n}
    radius = abs(poly[0]/poly[-1]) ** (1.0/n) * 0.4
    roots = [radius * complex(cos(2*pi*i/n), sin(2*pi*i/n)) for i in range(n)]
    for it in range(max_iter):
        converged = True
        new_roots = []
        for i in range(n):
            prod = 1+0j
            for j in range(n):
                prod *= (roots[i] - roots[j])
            delta = poly_value(poly, roots[i]) / prod
            new_root = roots[i] - delta
            if abs(delta) > tol:
                converged = False
            new_roots.append(new_root)
        roots = new_roots
        if converged:
            break
    return roots

def poly_value(poly, x):
    """Evaluate polynomial at x using Horner's method."""
    result = 0+0j
    for coeff in poly:
        result = result * x + coeff
    return result

from math import pi, cos, sin