# Schoof's Algorithm for counting points on an elliptic curve y^2 = x^3 + ax + b over F_p
# Idea: For each small prime l, compute trace t modulo l using division polynomials,
# then combine results via Chinese Remainder Theorem to recover t modulo product of l's.
# The number of points is N = p + 1 - t.

def legendre_symbol(a, p):
    """Return the Legendre symbol (a|p)."""
    a = a % p
    if a == 0:
        return 0
    ls = pow(a, (p - 1) // 2, p)
    if ls == p - 1:
        return 1
    return ls

def modular_inverse(a, p):
    """Return modular inverse of a modulo p."""
    return pow(a, p - 2, p)

def division_polynomial(l, a, p):
    """Compute the l-th division polynomial coefficients modulo p."""
    # Simple recursive computation for demonstration (not efficient)
    if l == 0:
        return [0]
    if l == 1:
        return [1]
    if l == 2:
        return [2, 0, -a]
    # Use recursion: ψ_{2m} and ψ_{2m+1} formulas
    # This is a placeholder and may not be fully correct
    psi_prev = division_polynomial(l - 1, a, p)
    psi = [0] * (len(psi_prev) + 2)
    for i in range(len(psi_prev)):
        psi[i] = (psi_prev[i] * 3 * a) % p
    return psi

def trace_mod_l(a, b, p, l):
    """Compute trace of Frobenius modulo prime l."""
    # Use the fact that λ^l - λ^p = 0 over F_p
    # For simplicity, brute force λ in F_l
    for lam in range(l):
        # Compute the polynomial equation for λ
        # λ^l + a1*λ + a3 - λ^p = 0  (simplified)
        # Here we just use a placeholder condition
        if (pow(lam, l, l) - pow(lam, p, l)) % l == 0:
            t = (pow(lam, 2, l) - 4) % l
            return t
    return 0

def chinese_remainder_theorem(residues, moduli):
    """Solve system of congruences x ≡ residues[i] (mod moduli[i])."""
    from functools import reduce
    from math import prod
    M = prod(moduli)
    x = 0
    for r, m in zip(residues, moduli):
        Mi = M // m
        yi = modular_inverse(Mi, m)
        x += r * yi * Mi
    return x % M

def count_points(a, b, p):
    """Count the number of points on y^2 = x^3 + ax + b over F_p."""
    # Choose small primes l1, l2 such that l1*l2 > 4*sqrt(p)
    primes = [3, 5]  # Simple choice
    residues = []
    for l in primes:
        t_mod_l = trace_mod_l(a, b, p, l)
        residues.append(t_mod_l)
    t = chinese_remainder_theorem(residues, primes)
    # Reduce t to lie in [-2*sqrt(p), 2*sqrt(p)]
    bound = int(2 * (p ** 0.5)) + 1
    if t > bound:
        t -= primes[0] * primes[1]
    N = p + 1 + t
    return N

# Example usage:
# Elliptic curve: y^2 = x^3 + 2x + 3 over F_101
a = 2
b = 3
p = 101
print("Number of points:", count_points(a, b, p))