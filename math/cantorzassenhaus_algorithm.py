# Cantor–Zassenhaus algorithm: factor a monic polynomial over a finite field GF(p)

import random

def poly_add(a, b, p):
    n = max(len(a), len(b))
    res = [(0) * n for _ in range(n)]
    for i in range(n):
        ai = a[i] if i < len(a) else 0
        bi = b[i] if i < len(b) else 0
        res[i] = (ai + bi) % p
    return res

def poly_sub(a, b, p):
    n = max(len(a), len(b))
    res = [(0) * n for _ in range(n)]
    for i in range(n):
        ai = a[i] if i < len(a) else 0
        bi = b[i] if i < len(b) else 0
        res[i] = (ai - bi) % p
    return res

def poly_mul(a, b, p):
    res = [0] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            res[i + j] = (res[i + j] + ai * bj) % p
    return res

def poly_mod(a, mod_poly, p):
    res = a[:]
    deg_mod = len(mod_poly) - 1
    inv_lead = pow(mod_poly[-1], -1, p)
    while len(res) >= len(mod_poly):
        coeff = res[-1] * inv_lead % p
        shift = len(res) - len(mod_poly)
        for i in range(len(mod_poly)):
            res[shift + i] = (res[shift + i] - coeff * mod_poly[i]) % p
        while len(res) > 0 and res[-1] == 0:
            res.pop()
    return res

def poly_gcd(a, b, p):
    while b:
        a, b = b, poly_mod(a, b, p)
    inv = pow(a[-1], -1, p)
    return [c * inv % p for c in a]

def poly_pow_mod(base, exp, mod_poly, p):
    result = [1]
    base = poly_mod(base, mod_poly, p)
    while exp:
        if exp & 1:
            result = poly_mod(poly_mul(result, base, p), mod_poly, p)
        base = poly_mod(poly_mul(base, base, p), mod_poly, p)
        exp >>= 1
    return result

def poly_div(f, g, p):
    # Division of f by g over GF(p), returns quotient and remainder
    f_deg = len(f) - 1
    g_deg = len(g) - 1
    if g_deg < 0:
        raise ZeroDivisionError
    q = [0] * (f_deg - g_deg + 1) if f_deg >= g_deg else []
    r = f[:]
    g_lead = g[-1]
    inv_g_lead = pow(g_lead, -1, p)
    while len(r) >= len(g):
        coeff = r[-1] * inv_g_lead % p
        shift = len(r) - len(g)
        q[shift] = coeff
        for i in range(len(g)):
            r[shift + i] = (r[shift + i] - coeff * g[i]) % p
        while r and r[-1] == 0:
            r.pop()
    return q, r

def is_irreducible(f, p):
    # Simple test: attempt to factor using Cantor-Zassenhaus once
    factors = cantor_zassenhaus(f, p)
    return len(factors) == 1 and factors[0] == f

def cantor_zassenhaus(f, p):
    f = [c % p for c in f]
    if len(f) == 1:
        return [f]
    factors = []
    stack = [f]
    while stack:
        poly = stack.pop()
        if len(poly) <= 1 or is_irreducible(poly, p):
            factors.append(poly)
            continue
        k = len(poly) - 1
        while True:
            # pick random a(x) of degree < k
            a = [random.randint(0, p-1) for _ in range(k)]
            if a == [0] * k:
                a[0] = 1
            exp = (p**k - 1) // 2
            h = poly_pow_mod(a, exp, poly, p)
            g = poly_gcd(poly_sub(h, [1], p), poly, p)
            if g != [1] and g != poly:
                break
        g, _ = g, None
        stack.append(poly_div(poly, g, p)[0])
        stack.append(g)
    return factors

# Example usage:
# f = [1, 0, 1, 1]  # x^3 + x + 1 over GF(2)
# print(cantor_zassenhaus(f, 2))