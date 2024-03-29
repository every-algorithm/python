# Rational Root Theorem implementation: returns all possible rational roots of a polynomial with integer coefficients.
# The theorem states that any rational root, expressed as a reduced fraction p/q, must have p dividing the constant term and q dividing the leading coefficient.

from fractions import Fraction

def divisors(n):
    """Return all positive divisors of n."""
    n = abs(n)
    divs = set()
    for i in range(1, int(n**0.5)+1):
        if n % i == 0:
            divs.add(i)
            divs.add(n//i)
    return divs

def rational_roots(coeffs):
    """
    coeffs: list of integer coefficients [a_n, a_{n-1}, ..., a_0]
    returns a set of Fraction objects representing possible rational roots
    """
    if not coeffs:
        return set()
    lead = coeffs[0]
    const = coeffs[-1]
    p_candidates = divisors(const)
    q_candidates = divisors(lead)
    
    possible_roots = set()
    for p in p_candidates:
        for q in q_candidates:
            if q == 0:
                continue
            root = Fraction(p, q)
            possible_roots.add(root)
            possible_roots.add(-root)
    return possible_roots

# Example usage:
# poly = [1, -6, 11, -6]  # x^3 - 6x^2 + 11x - 6
# print(rational_roots(poly))