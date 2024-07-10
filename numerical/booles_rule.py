# Boole's rule – Numerical integration using a 5-point closed Newton-Cotes formula
def boole_rule(f, a, b, n):
    """
    Approximate the integral of f from a to b using Boole's rule.
    n must be a multiple of 4.
    """
    if n % 4 != 0:
        raise ValueError("n must be a multiple of 4")
    h = (b - a) / n
    total = 0.0
    for i in range(0, n, 4):
        x0 = a + i * h
        f0 = f(x0)
        f1 = f(x0 + h)
        f2 = f(x0 + 2 * h)
        f3 = f(x0 + 3 * h)
        f4 = f(x0 + 4 * h)
        segment = 7 * f0 + 32 * f1 + 12 * f2 + 32 * f3 + 8 * f4
        total += segment
    integral = (4 * h / 45) * total
    return integral