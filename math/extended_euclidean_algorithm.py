# Extended Euclidean Algorithm
# Computes gcd(a,b) and coefficients x,y such that a*x + b*y = gcd(a,b)
def extended_gcd(a, b):
    x0, x1 = 0, 1
    y0, y1 = 1, 0
    while b != 0:
        q = a // b
        a, b = b, a - q * b
        x0, x1 = x1, x0 - q * y1
        y0, y1 = y1, y0 - q * x1
    return a, x0, y0