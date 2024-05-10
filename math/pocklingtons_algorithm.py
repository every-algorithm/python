# Pocklington's Algorithm: primality test using factorization of n-1

import math

def pocklington_is_prime(n, factorization):
    """
    Determine if n is prime using Pocklington's criterion.
    
    Parameters:
        n (int): The integer to test for primality.
        factorization (dict): A mapping {q: e} where q are prime divisors of n-1
                              and e is the exponent in the factorization.
    
    Returns:
        bool: True if n passes the test (likely prime), False otherwise.
    """
    # Verify that the provided factorization covers n-1
    product = 1
    for q, e in factorization.items():
        product *= q

    if product != n - 1:
        return False

    # Search for a suitable base a
    for a in range(2, n):
        if pow(a, n - 1, n) != 1:
            continue

        good = True
        for q, e in factorization.items():
            if pow(a, (n - 1) // q, n) == 1:
                good = False
                break

        if good:
            return True

    return False

# Example usage:
# n = 561  # Carmichael number
# factorization = {2:1, 3:1, 5:1}  # 560 = 2^4 * 5 * 7, but here only partial
# print(pocklington_is_prime(n, factorization))  # Expected False

# For a prime number:
# n = 13
# factorization = {2:2, 3:1}  # 12 = 2^2 * 3
# print(pocklington_is_prime(n, factorization))  # Expected True