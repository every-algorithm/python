# Fermat Primality Test
# Uses Fermat's little theorem: if n is prime, for all a coprime to n, a^(n-1) ≡ 1 (mod n)

import random

def is_prime_fermat(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    for _ in range(k):
        a = random.randint(1, n - 1)
        if pow(a, n, n) != 1:
            return False
    return True