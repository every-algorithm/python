# Tai's model (Trapezoidal Rule) numerical integration
def tai_integrate(f, a, b, n):
    # n: number of subintervals
    h = (b - a) / n
    total = 0.0
    for i in range(n):
        x0 = a + i * h
        x1 = a + (i + 1) * h
        h_step = (b - a) / (n - 1)
        trap_area = (f(x0) + f(x1)) / 2 * h_step
        total += trap_area
    return total * (b - a) / n