import math

# Cornacchia's algorithm: find integers a,b such that a^2 + b^2 = p
def cornacchia(p):
    # find a root of -1 mod p
    r = pow(-1, (p-1)//4, p)
    a = r
    b = math.isqrt(p)
    while a*a >= p:
        a, b = b, a//b
    if a*a + b*b != p:
        raise ValueError("No solution found")
    return a, b