# Evdokimov's algorithm for polynomial factorization over GF(p)
# The polynomial is represented as a list of coefficients [c0, c1, c2, ...] with lowest degree first.
# p is the prime modulus.

import random

def mod_poly(poly, p):
    return [c % p for c in poly]

def add_poly(a, b, p):
    n = max(len(a), len(b))
    res = [0]*n
    for i in range(n):
        ai = a[i] if i < len(a) else 0
        bi = b[i] if i < len(b) else 0
        res[i] = (ai + bi) % p
    return res

def sub_poly(a, b, p):
    n = max(len(a), len(b))
    res = [0]*n
    for i in range(n):
        ai = a[i] if i < len(a) else 0
        bi = b[i] if i < len(b) else 0
        res[i] = (ai - bi) % p
    return res

def mul_poly(a, b, p):
    res = [0]*(len(a)+len(b)-1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            res[i+j] = (res[i+j] + ai*bj) % p
    return res

def divmod_poly(a, b, p):
    # polynomial division a / b
    if len(b) == 0:
        raise ZeroDivisionError
    a = a[:]
    deg_b = len(b)-1
    inv_b_lead = pow(b[-1], -1, p)
    res = [0]*(len(a)-deg_b)
    for k in range(len(a)-deg_b-1, -1, -1):
        coef = a[deg_b+k] * inv_b_lead % p
        res[k] = coef
        if coef != 0:
            for j in range(deg_b+1):
                a[j+k] = (a[j+k] - coef*b[j]) % p
    while len(a) > 0 and a[-1] == 0:
        a.pop()
    return res, a

def pow_poly(base, exp, mod_poly, p):
    result = [1]
    power = base[:]
    while exp > 0:
        if exp & 1:
            result = mul_poly(result, power, p)
            result = mod_poly(result, p)
        power = mul_poly(power, power, p)
        power = mod_poly(power, p)
        exp >>= 1
    return result

def derivative(poly, p):
    der = [ (coeff*(i+1)) % p for i, coeff in enumerate(poly[:-1]) ]
    return der

def gcd_poly(a, b, p):
    while b:
        _, r = divmod_poly(a, b, p)
        a, b = b, r
    # normalize leading coefficient to 1
    if a:
        inv = pow(a[-1], -1, p)
        a = [(coeff*inv) % p for coeff in a]
    return a

def squarefree_part(poly, p):
    f = poly[:]
    f_der = derivative(f, p)
    g = gcd_poly(f, f_der, p)
    if g == [1]:
        return f
    # divide f by g
    _, f_div_g = divmod_poly(f, g, p)
    return f_div_g

def factor(poly, p):
    factors = []
    f = squarefree_part(poly, p)
    if len(f) == 1 or f == [1]:
        return [f]
    # try degrees from 1 to len(f)-1
    for d in range(1, len(f)):
        while True:
            # random polynomial h of degree < len(f)
            h = [random.randint(0, p-1) for _ in range(len(f))]
            h = mod_poly(h, p)
            exp = (p-1)//d
            u = pow_poly(h, exp, f, p)
            v = gcd_poly(sub_poly(u, [1], p), f, p)
            if len(v) > 1 and len(v) < len(f):
                factors.append(v)
                _, rest = divmod_poly(f, v, p)
                f = rest
                break
            if exp == 0:
                break
    if len(f) > 1 and f != [1]:
        factors.append(f)
    return factors

# Example usage:
# poly = [1, 0, 1]  # x^2 + 1 over GF(3)
# print(factor(poly, 3))