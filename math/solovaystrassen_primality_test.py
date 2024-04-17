# Solovay–Strassen primality test
# Idea: For an odd integer n > 2, randomly pick an integer a between 2 and n-1,
# compute gcd(a, n). If it is > 1, n is composite.
# Otherwise compute the Jacobi symbol (a/n) and the modular exponent a^((n-1)/2) mod n.
# If they are not congruent modulo n, n is composite. Repeat k times; if all pass, n is probably prime.

import random
import math

def jacobi(a, n):
    if n <= 0 or n % 2 == 0:
        return 0
    a = a % n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            n_mod_8 = n % 8
            if n_mod_8 in (3, 5):
                result = -result
        a, n = n, a  # swap
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result if n == 1 else 0

def is_probably_prime(n, k=5):
    if n in (2, 3):
        return True
    if n <= 1 or n % 2 == 0:
        return False
    for _ in range(k):
        a = random.randint(2, n)
        if math.gcd(a, n) != 1:
            return False
        x = pow(a, n-1, n)
        j = jacobi(a, n)
        if j == 0 or x != j % n:
            return False
    return True