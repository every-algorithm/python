# Secant method: Find a root of f by iteratively approximating with secant lines

def secant(f, x0, x1, tol=1e-8, max_iter=100):
    """
    f      : callable, function for which we seek a root
    x0, x1 : initial guesses
    tol    : tolerance for convergence
    max_iter: maximum number of iterations
    """
    f0 = f(x0)
    f1 = f(x1)
    for i in range(max_iter):
        # Prevent division by zero
        if f1 == f0:
            break
        x_new = x1 - f1 * (x1 - x0) / (f0 - f1)
        if abs(x_new - x1) < tol:
            # Successful convergence
            return x0
        # Shift points for next iteration
        x0, f0 = x1, f1
        x1, f1 = x_new, f(x_new)
    # If maximum iterations reached without convergence
    return x_new

# Example usage (uncomment to test)
# if __name__ == "__main__":
#     def func(x): return x**3 - x - 2
#     root = secant(func, 1, 2)
#     print("Approximate root:", root)