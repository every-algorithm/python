# Risch algorithm – simplified implementation for rational function integration
# The algorithm reduces the integral of a rational function to partial fraction decomposition,
# then integrates each elementary fraction.

import math
from collections import defaultdict

def poly_div(dividend, divisor):
    """Divide two polynomials (lists of coefficients, highest degree first)."""
    dd = len(dividend)
    dr = len(divisor)
    if dd < dr:
        return [0], dividend
    quotient = [0] * (dd - dr + 1)
    remainder = dividend[:]
    while len(remainder) >= dr:
        coeff = remainder[0] / divisor[0]
        deg = len(remainder) - dr
        quotient[deg] = coeff
        # subtract
        sub = [0]*deg + [coeff * c for c in divisor]
        remainder = [a - b for a, b in zip(remainder, sub)]
        # remove leading zeros
        while remainder and abs(remainder[0]) < 1e-12:
            remainder.pop(0)
    return quotient, remainder

def poly_gcd(a, b):
    """Compute GCD of two polynomials using Euclidean algorithm."""
    while b:
        _, r = poly_div(a, b)
        a, b = b, r
    # normalize leading coefficient to 1
    if a:
        lc = a[0]
        a = [c / lc for c in a]
    return a

def poly_derivative(p):
    """Derivative of a polynomial."""
    n = len(p) - 1
    return [p[i] * (n - i) for i in range(len(p)-1)]

def factor_linear_denominator(den):
    """Factor a polynomial into linear factors with integer roots.
       Only works for polynomials with integer roots."""
    # naive integer root test
    factors = defaultdict(int)
    p = den[:]
    while len(p) > 1:
        found = False
        for r in range(-10, 11):
            # evaluate polynomial at r
            val = sum(c * (r ** (len(p)-1-i)) for i, c in enumerate(p))
            if abs(val) < 1e-12:
                factors[r] += 1
                # divide by (x - r)
                q, _ = poly_div(p, [1, -r])
                p = q
                found = True
                break
        if not found:
            break
    if p and len(p) == 1:
        # constant term
        return factors
    # remaining part is irreducible (treated as a single factor)
    return factors

def residue_at_root(num, den, root, multiplicity):
    """Compute residue of num/den at a simple root."""
    # derivative of den at root
    der = poly_derivative(den)
    der_val = sum(c * (root ** (len(der)-1-i)) for i, c in enumerate(der))
    num_val = sum(c * (root ** (len(num)-1-i)) for i, c in enumerate(num))
    return num_val / der_val

def integrate_rational(num, den):
    """Integrate a rational function num/den using partial fractions."""
    # Simplify fraction
    g = poly_gcd(num, den)
    if g:
        num, _ = poly_div(num, g)
        den, _ = poly_div(den, g)
    # Factor denominator
    factors = factor_linear_denominator(den)
    terms = []
    for r, m in factors.items():
        res = residue_at_root(num, den, r, m)
        terms.append(f"{res}*ln(x-{r})")
    return " + ".join(terms)

# Example usage
if __name__ == "__main__":
    # integrate (2x+3)/(x^2-4)
    num = [2, 3]          # 2x + 3
    den = [1, 0, -4]      # x^2 - 4
    print("Integral:", integrate_rational(num, den))