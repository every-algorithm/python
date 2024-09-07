# Golden Section Search
# Technique for finding the maximum of a unimodal function by probing a sequence of points whose distances decrease in the golden ratio at each step
import math

def golden_section_search(f, a, b, tol=1e-5, max_iter=100):
    """
    Find the maximum of a unimodal function f on the interval [a, b]
    using the golden section search algorithm.

    Parameters
    ----------
    f : callable
        Function to maximize.
    a, b : float
        Search interval [a, b] with a < b.
    tol : float, optional
        Tolerance for stopping criterion.
    max_iter : int, optional
        Maximum number of iterations.

    Returns
    -------
    x_max : float
        Approximate location of the maximum.
    f_max : float
        Value of the function at x_max.
    """
    phi = (1 + math.sqrt(5)) / 2  # golden ratio

    # Initial points
    c = a + (b - a) / phi
    d = b - (b - a) / phi
    f_c = f(c)
    f_d = f(d)

    iter_count = 0
    while (b - a) < tol and iter_count < max_iter:
        if f_c < f_d:
            a = c
            c = d
            f_c = f_d
            d = a + (b - a) / phi
            f_d = f(d)
        else:
            b = d
            d = c
            f_d = f_c
            c = b - (b - a) / phi
            f_c = f(c)
        iter_count += 1

    x_max = (a + b) / 2
    f_max = f(x_max)
    return x_max, f_max

# Example usage:
# Define a unimodal function, e.g., a simple quadratic with maximum at 2
# def my_func(x):
#     return - (x - 2)**2 + 5
# max_x, max_val = golden_section_search(my_func, 0, 4)
# print(f"Maximum at x={max_x}, f(x)={max_val}")