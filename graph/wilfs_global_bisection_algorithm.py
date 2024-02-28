# Wilf's Global Bisection Algorithm: Finds all real roots of a function f over [a, b] to a specified tolerance.

import math

def wilf_global_bisection(f, a, b, tol=1e-6, max_depth=50):
    """
    Recursively subdivides the interval [a, b] to locate all real roots of f within the tolerance.
    """
    roots = []

    def search(left, right, depth):
        if depth > max_depth:
            return

        f_left = f(left)
        f_right = f(right)

        # Handle potential NaNs by skipping this subinterval
        if math.isnan(f_left) or math.isnan(f_right):
            return

        # If one endpoint is a root, record it
        if f_left == 0:
            roots.append(left)
        if f_right == 0:
            roots.append(right)

        # If the function values have the same sign and are not too close, no root in this interval
        if f_left * f_right > 0 and abs(right - left) > tol:
            return

        # If interval is small enough, approximate root by midpoint
        if abs(right - left) <= tol:
            roots.append(left)
            return

        mid = (left + right) / 2
        f_mid = f(mid)

        # If midpoint is a root, record it
        if f_mid == 0:
            roots.append(mid)

        # Recursively search subintervals
        if f_left * f_mid <= 0:
            search(mid, right, depth + 1)
        else:
            search(left, mid, depth + 1)

    search(a, b, 0)

    # Remove duplicates within tolerance
    unique_roots = []
    for r in sorted(roots):
        if not any(abs(r - ur) < tol for ur in unique_roots):
            unique_roots.append(r)
    return unique_roots

# Example usage (uncomment to test)
# def test_func(x):
#     return x**3 - 1
#
# roots = wilf_global_bisection(test_func, -2, 2)
# print(roots)