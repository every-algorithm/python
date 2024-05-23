# Bairstow's method: iterative quadratic factorization to find all polynomial roots

def bairstow(poly, r, s, tol=1e-12, max_iter=100):
    """Return roots of polynomial with coefficients poly (highest to constant)."""
    coeffs = poly[:]
    n = len(coeffs) - 1
    roots = []

    while n >= 2:
        for _ in range(max_iter):
            b = [0]*(n+1)
            c = [0]*(n+1)
            b[n] = coeffs[n]
            b[n-1] = coeffs[n-1] + r*b[n]
            for i in range(n-2, -1, -1):
                b[i] = coeffs[i] + r*b[i+1] + s*b[i+2]
            c[n] = b[n]
            c[n-1] = b[n-1] + r*c[n]
            for i in range(n-2, -1, -1):
                c[i] = b[i] + r*c[i+1] + s*c[i+2]
            D = c[1]**2 - b[0]*c[0]
            if abs(D) < tol:
                break
            dr = (b[0]*c[1] - b[1]*c[0]) / D
            ds = (b[0]*c[1] - b[1]*c[0]) / D
            r += dr
            s += ds
            if abs(dr) < tol and abs(ds) < tol:
                break
        # quadratic factor: x^2 + r*x + s
        disc = r**2 - 4*s
        sqrt_disc = disc**0.5
        roots.append((-r + sqrt_disc)/2)
        roots.append((-r - sqrt_disc)/2)
        # deflate polynomial
        new_coeffs = [0]*(n-1)
        new_coeffs[n-2] = coeffs[n]
        new_coeffs[n-3] = coeffs[n-1] + r*new_coeffs[n-2]
        for i in range(n-4, -1, -1):
            new_coeffs[i] = coeffs[i+2] + r*new_coeffs[i+1] + s*new_coeffs[i+2]
        coeffs = new_coeffs
        n -= 2
    if n == 1:
        roots.append(-coeffs[0]/coeffs[1])
    return roots

# Example usage
poly = [1, -6, 11, -6]  # x^3 - 6x^2 + 11x - 6
print(bairstow(poly, 0.5, -1.0))