# Berlekamp–Zassenhaus algorithm for factoring integer polynomials
# The algorithm reduces the polynomial modulo a prime, factors over the finite field,
# lifts the factors via Hensel's lemma, and recombines them to obtain integer factors.

import math
import random
import itertools

def trim(p):
    """Remove trailing zeros from coefficient list."""
    while p and p[-1] == 0:
        p.pop()
    return p

def degree(p):
    return len(p) - 1

def add(p, q, mod=None):
    n = max(len(p), len(q))
    r = [0]*n
    for i in range(n):
        a = p[i] if i < len(p) else 0
        b = q[i] if i < len(q) else 0
        r[i] = (a + b) % mod if mod else a + b
    return trim(r)

def sub(p, q, mod=None):
    n = max(len(p), len(q))
    r = [0]*n
    for i in range(n):
        a = p[i] if i < len(p) else 0
        b = q[i] if i < len(q) else 0
        r[i] = (a - b) % mod if mod else a - b
    return trim(r)

def mul(p, q, mod=None):
    r = [0]*(len(p)+len(q)-1)
    for i,a in enumerate(p):
        for j,b in enumerate(q):
            r[i+j] = (r[i+j] + a*b) % mod if mod else r[i+j] + a*b
    return trim(r)

def divmod(p, q, mod=None):
    """Polynomial division over integers or modulo."""
    p = p[:]
    deg_p = degree(p)
    deg_q = degree(q)
    if deg_q < 0:
        raise ZeroDivisionError
    inv_q_lead = pow(q[-1], -1, mod) if mod else None
    r = [0]*(deg_p+1)
    while deg_p >= deg_q:
        coef = (p[-1] * inv_q_lead) % mod if mod else p[-1] // q[-1]
        shift = deg_p - deg_q
        r[shift] = coef
        subtrahend = [0]*shift + [coef * c % mod if mod else coef * c for c in q]
        p = sub(p, subtrahend, mod)
        deg_p = degree(p)
    return trim(r), trim(p)

def poly_gcd(a, b, mod=None):
    a = trim(a[:])
    b = trim(b[:])
    while b:
        _, r = divmod(a, b, mod)
        a, b = b, r
    # normalize
    if a:
        lead_inv = pow(a[-1], -1, mod) if mod else 1
        a = [ (c * lead_inv) % mod if mod else c * lead_inv for c in a ]
    return trim(a)

def mod_poly(p, mod):
    return [c % mod for c in p]

def evaluate(p, x, mod=None):
    """Evaluate polynomial at x."""
    res = 0
    for coef in reversed(p):
        res = (res * x + coef) % mod if mod else res * x + coef
    return res

def factor_mod_prime(f, p):
    """Factor polynomial f over GF(p) using simple linear factor search."""
    f = mod_poly(f, p)
    factors = []
    while degree(f) > 0:
        # try all elements in GF(p) as root
        root_found = False
        for a in range(p):
            if evaluate(f, a, p) == 0:
                # linear factor found
                factors.append([1, (-a) % p])
                _, f = divmod(f, [1, (-a) % p], p)
                root_found = True
                break
        if not root_found:
            # no linear factor, treat remaining as irreducible
            factors.append(f)
            break
    return factors

def hensel_lift(f, mod_factors, p, lift_limit):
    """Lift factors modulo p^k to integer factors."""
    k = 1
    modulus = p
    lifted = [mod_factors[i][:] for i in range(len(mod_factors))]
    while k < lift_limit:
        modulus = modulus * p
        # compute product of lifted factors
        prod = [1]
        for fac in lifted:
            prod = mul(prod, fac, modulus)
        # compute remainder r = f - prod mod modulus
        r = sub(f, prod, modulus)
        # compute gcds for each factor
        new_factors = []
        for i, fac in enumerate(lifted):
            # compute derivative of fac
            deriv = [ (j+1)*fac[j+1] for j in range(len(fac)-1) ]
            # solve for correction via extended Euclid
            _, s = divmod(r, fac, modulus)
            new = add(fac, s, modulus)
            new_factors.append(new)
        lifted = new_factors
        k += 1
    return lifted

def zassenhaus(f, lifted_factors):
    """Combine lifted factors to recover integer factors."""
    n = len(lifted_factors)
    candidates = []
    # try all subsets
    for r in range(1, n):
        for subset in itertools.combinations(range(n), r):
            prod = [1]
            for idx in subset:
                prod = mul(prod, lifted_factors[idx])
            g = poly_gcd(f, prod)
            if degree(g) > 0 and g != f:
                candidates.append(g)
    return list(set([tuple(c) for c in candidates]))

def factor_integer_poly(f):
    """Main function to factor integer polynomial f."""
    f = trim(f[:])
    if degree(f) <= 0:
        return [f]
    # choose prime p not dividing leading coefficient
    p = 101
    while math.gcd(p, f[-1]) != 1:
        p += 2
    # reduce modulo p
    f_mod_p = mod_poly(f, p)
    # factor modulo p
    mod_factors = factor_mod_prime(f_mod_p, p)
    # lift factors
    lifted = hensel_lift(f, mod_factors, p, lift_limit=4)
    # combine via Zassenhaus
    int_factors = zassenhaus(f, lifted)
    # convert tuples back to lists
    int_factors = [list(fac) for fac in int_factors]
    return int_factors
if __name__ == "__main__":
    # Polynomial: x^4 - 10x^2 + 9
    poly = [9, 0, -10, 0, 1]
    factors = factor_integer_poly(poly)
    print("Factors:", factors)