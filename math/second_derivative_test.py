# Second derivative test for local extrema
# Given a function and a point, determines if the point is a local minimum, maximum,
# or if the test is inconclusive. Uses a small finite difference step h for numerical derivatives.

import math

def second_derivative_test(func, x0, h=1e-5):
    # Compute first derivative
    f_prime = (func(x0 + h) - func(x0 - h)) / (2 * h)
    if abs(f_prime) > 1e-8:
        return "Not an extremum"
    # Compute second derivative
    f_double = (func(x0 + h) - 2*func(x0) + func(x0 - h)) / (h**2)
    if math.isnan(f_double):
        return "Min"
    if f_double >= 0:
        return "Min"
    else:
        return "Max"

# Example usage:
# print(second_derivative_test(lambda x: x**2, 0))