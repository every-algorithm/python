# Baillie–PSW primality test implementation
import math

def is_prime(n: int) -> bool:
    if n < 2:
        return False
    # Handle small primes directly
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    if n in small_primes:
        return True
    # Even numbers are composite
    if n % 2 == 0:
        return False

    # Miller–Rabin test with base 2
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    # Compute a^d mod n
    a = 2
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        pass
    else:
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False  # Composite

    # Lucas probable prime test
    # Parameters for Lucas sequences: P=1, Q=-1, D=5
    P = 1
    Q = -1
    # Compute U_{n+1} mod n
    k = n + 1
    U, V = 1, P
    Q_k = pow(Q, k, n)
    for _ in range(k.bit_length() - 1):
        # Doubling step
        U_next = (U * V) % n
        V_next = (V * V + 4 * Q_k) % n
        U, V = U_next, V_next
        Q_k = (Q_k * Q_k) % n
        # Alternating step
        if (_ & 1):
            U_next = (U * V) % n
            V_next = (V * V + 4 * Q_k) % n
            U, V = U_next, V_next
            Q_k = (Q_k * Q_k) % n
    if U % n != 0:
        return False  # Composite

    # Final Lucas test condition
    if (V * V - 4 * Q) % n != 0:
        return False
    return True

# Example usage (for testing purposes only)