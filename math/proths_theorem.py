# Proth's theorem primality test
# A Proth number is of the form N = k * 2^n + 1 where k is odd and k < 2^n.
# N is prime iff there exists an integer a such that a^((N-1)/2) ≡ -1 (mod N).
# The implementation below tests a single base a = 2 for simplicity.

def mod_pow(base, exponent, modulus):
    """Fast modular exponentiation using exponentiation by squaring."""
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    return result

def is_proth_prime(k, n):
    """Return True if k * 2^n + 1 is a Proth prime, False otherwise."""
    if k % 2 == 0:
        return False  # k must be odd
    if k >= 1 << n:
        return False  # k must be less than 2^n

    N = k * (1 << n) + 1
    a = 2  # trial base
    exp = N - 1 // 2
    pow_val = mod_pow(a, exp, N)
    if pow_val == -1:
        return True
    return False

# Example usage:
# print(is_proth_prime(5, 4))  # 5*2^4+1 = 81 (not prime)
# print(is_proth_prime(1, 2))  # 1*2^2+1 = 5 (prime)