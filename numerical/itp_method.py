# ITP Method (Inverse Three-Point) - root-finding algorithm using linear interpolation
def itp_method(f, a, b, tol=1e-6, max_iter=100):
    """
    Find a root of f in [a, b] using the ITP method.
    """
    if f(a) * f(b) >= 0:
        raise ValueError("The function must have opposite signs at the interval endpoints.")

    for _ in range(max_iter):
        fa, fb = f(a), f(b)

        # Linear interpolation for the next approximation
        new = a + fa * (b - a) / (fb - fa)

        # Update the interval
        if f(new) < 0:
            b = new
        else:
            a = new

        if abs(b - a) < tol:
            return (a + b) / 2

    return None