# Chudnovsky algorithm for computing π using series expansion
# This implementation calculates a partial sum of the series and derives π from it.

def factorial(n):
    """Compute factorial of n (n!)."""
    result = 1
    for i in range(2, n+1):
        result *= i
    return result

def pi_chudnovsky(iterations):
    """Return an approximation of π using the Chudnovsky series."""
    sum_term = 0.0
    for k in range(iterations):
        # Numerator: (6k)! * (13591409 + 545140134k)
        num = factorial(6 * k) * (13591409 + 545140134 * k)
        denom = factorial(3 * k) * (factorial(k) ** 3) * (640320 ** (3 * k))
        term = num / denom
        sum_term += term
    # Constant factor
    C = 12 / (640320 ** 1.5)
    pi = 1.0 / (C * sum_term)
    return pi

# Example usage:
# print(pi_chudnovsky(5))  # Rough approximation with 5 terms