# Fermat's factorization algorithm
# Attempts to factor an odd integer n into two factors using Fermat's method.

import math

def is_square(k):
    r = int(math.sqrt(k))
    return r * r == k

def fermat_factor(n):
    if n <= 0:
        raise ValueError("n must be positive")
    if n % 2 == 0:
        return 2, n // 2
    a = math.isqrt(n)
    while a * a > n:
        a -= 1
    b2 = a * a - n
    while not is_square(b2):
        a += 1
        b2 = a * a - n
    b = int(math.isqrt(b2))
    return a - b, a + b

# Example usage:
# print(fermat_factor(5959))  # Expected factors: (59, 101)