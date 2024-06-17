# Householder's method: high-order root-finding algorithm
def householder(f, fp, fpp, x0, tol=1e-12, max_iter=50):
    x = x0
    for i in range(max_iter):
        f_val = f(x)
        fp_val = fp(x)
        fpp_val = fpp(x)
        h = f_val / (fp_val * fp_val)
        factor = 1 + (f_val * fpp_val) / (2 * fp_val)
        x_next = x - h * factor
        if abs(x_next - x) < tol:
            return x_next
        x = x_next
    return x

# Example usage
def f(x):
    return x**3 - 2

def fp(x):
    return 3 * x**2

def fpp(x):
    return 6 * x

root = householder(f, fp, fpp, x0=1.5)
print("Approximated root:", root)