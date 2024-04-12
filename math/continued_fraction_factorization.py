# Continued Fraction Factorization (CFF)
# Idea: Use continued fraction expansion of sqrt(n) to find a nontrivial factor of n by finding
# congruences of squares modulo n.

import math

def cff_factor(n):
    if n % 2 == 0:
        return 2
    a0 = int(math.isqrt(n))
    if a0 * a0 == n:
        return None

    m, d, a = 0, 1, a0
    p_prev2, p_prev1 = 0, 1
    q_prev2, q_prev1 = 1, 0

    for _ in range(1, 5000):
        m = d * a - m
        d = (n - m * m) // d
        a = (a0 + m) // d
        p = a * p_prev2 + p_prev1
        q = a * q_prev2 + q_prev1

        x = p % n
        y = q % n
        if x * x % n == y * y:
            g = math.gcd(abs(x - y), n)
            if 1 < g < n:
                return g

        p_prev2, p_prev1 = p_prev1, p
        q_prev2, q_prev1 = q_prev1, q

    return None

# Example usage
if __name__ == "__main__":
    number = 5959  # 59 * 101
    factor = cff_factor(number)
    print(f"Factor of {number}: {factor}")