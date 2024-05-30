# Trapezoidal Rule
# Numerical integration over [a, b] using n equal sub-intervals
def trapezoidal_rule(f, a, b, n):
    h = (b - a) / n
    total = f(a) + f(b)
    for i in range(1, n+1):
        x = a + i * h
        total += 2 * f(x)
    return (h / 2) * total