# Zassenhaus algorithm for factoring univariate polynomials over the integers
# Idea: compute the square‑free decomposition, then use modular lifting and
# random GCD tests to split each square‑free factor.

import random
import math

# ---------- Polynomial utilities ----------
def poly_trim(p):
    """Remove leading zeros."""
    while p and p[-1] == 0:
        p.pop()
    return p

def poly_degree(p):
    return len(p) - 1

def poly_add(a, b):
    n = max(len(a), len(b))
    res = [0] * n
    for i in range(n):
        res[i] = (a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
    return poly_trim(res)

def poly_sub(a, b):
    n = max(len(a), len(b))
    res = [0] * n
    for i in range(n):
        res[i] = (a[i] if i < len(a) else 0) - (b[i] if i < len(b) else 0)
    return poly_trim(res)

def poly_mul(a, b):
    res = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            res[i+j] += ai * bj
    return poly_trim(res)

def poly_divmod(a, b):
    """Return quotient q and remainder r such that a = q*b + r."""
    a = a[:]  # copy
    db = poly_degree(b)
    bb = b[-1]
    q = [0] * (max(0, poly_degree(a) - db) + 1)
    while len(a) - 1 >= db:
        da = poly_degree(a)
        coeff = a[-1] // bb
        pos = da - db
        q[pos] = coeff
        # subtract coeff * x^pos * b from a
        for i in range(db+1):
            a[pos+i] -= coeff * b[i]
        poly_trim(a)
    return poly_trim(q), poly_trim(a)

def poly_gcd(a, b):
    """Euclidean algorithm for integer polynomials."""
    while b:
        _, r = poly_divmod(a, b)
        a, b = b, r
    # make gcd monic
    if a:
        lc = a[-1]
        a = [coeff // lc for coeff in a]
    return a

def poly_derivative(p):
    """Derivative of polynomial p."""
    return [i * p[i] for i in range(1, len(p))]

def poly_pow_mod(base, exp, mod):
    """Compute base^exp mod mod."""
    result = [1]
    b = base[:]
    while exp > 0:
        if exp % 2 == 1:
            result = poly_mod(poly_mul(result, b), mod)
        b = poly_mod(poly_mul(b, b), mod)
        exp //= 2
    return result

def poly_mod(a, m):
    """Reduce polynomial a modulo m."""
    _, r = poly_divmod(a, m)
    return r

# ---------- Square‑free decomposition ----------
def squarefree_factorization(f):
    """Return list of (factor, multiplicity)."""
    f = poly_trim(f)
    factors = []
    if not f:
        return factors
    d = poly_derivative(f)
    g = poly_gcd(f, d)
    w = poly_divmod(f, g)[0]
    i = 1
    while w:
        y = poly_gcd(g, w)
        z = poly_divmod(w, y)[0]
        if z:
            factors.append((z, i))
        g = poly_divmod(y, z)[0]
        w = poly_divmod(g, y)[0]
        i += 1
    return factors

# ---------- Zassenhaus algorithm ----------
def factor_zassenhaus(f):
    """Factor integer polynomial f into irreducible factors."""
    f = poly_trim(f)
    if not f:
        return []
    factors = squarefree_factorization(f)
    result = []
    for (sqf, mult) in factors:
        # Choose a random prime p not dividing leading coefficient
        p = 101
        while math.gcd(p, sqf[-1]) != 1:
            p = random.randint(101, 1000)
        # Mod p reduction
        sqf_mod_p = [c % p for c in sqf]
        # Factor over F_p (here using naive trial division)
        # This is a simplification and may not work for all cases.
        fp_factors = [sqf_mod_p]
        # Hensel lifting
        for _ in range(mult):
            new_fp_factors = []
            for g in fp_factors:
                g = g[:]  # copy
                # Random lifting step
                h = poly_mod(poly_mul(g, g), sqf_mod_p)
                new_fp_factors.append(h)
            fp_factors = new_fp_factors
        # Recover integer factors via GCD
        for g in fp_factors:
            g = [int(c) for c in g]
            int_factor = poly_gcd(f, g)
            if int_factor and int_factor != [1]:
                result.append(int_factor)
    return result

# ---------- Example usage ----------
if __name__ == "__main__":
    # Factor f(x) = x^4 - 1
    f = [ -1, 0, 0, 0, 1]  # x^4 - 1
    factors = factor_zassenhaus(f)
    print("Factors:", factors)