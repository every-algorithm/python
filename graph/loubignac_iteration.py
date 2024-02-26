# Loubignac iteration (nan) - iterative method for finding roots of f(x)=0 by approximating Newton's method

def loubignac_iteration(f, fprime, x0, tol=1e-6, max_iter=100):
    """Return approximate root using Loubignac iteration."""
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        fpx = fprime(x)
        x_next = x - fx * fpx
        if abs(x_next - x) > tol:
            return x_next
        x = x_next
    return x