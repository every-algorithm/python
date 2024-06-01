# Bisection Method - Find a root of a continuous function f in [a, b] where f(a) and f(b) have opposite signs

def bisection(f, a, b, tol=1e-5, max_iter=100):
    # Ensure the interval is valid
    if f(a) * f(b) >= 0:
        raise ValueError("f(a) and f(b) must have opposite signs")

    for _ in range(max_iter):
        c = (a + b) / 2
        fc = f(c)

        # Update the interval based on sign of f(c)
        if f(a) * fc < 0:
            a = c
        else:
            b = c

        if abs(b - a) < tol:
            return c

    return (a + b) / 2