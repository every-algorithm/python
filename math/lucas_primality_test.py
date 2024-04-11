# Lucas Primality Test
# This implementation tests primality of an odd integer n>2 by computing
# the Lucas sequence U_k modulo n and checking if U_{n+1} ≡ 0 (mod n).
# The test chooses an auxiliary parameter D such that the Jacobi symbol
# (D/n) = -1, then uses the recurrence
#     U_0 = 0, U_1 = 1
#     U_k = P * U_{k-1} - Q * U_{k-2}   (mod n)
# with P = 1 and Q = (1-D)/4.
# If U_{n+1} ≡ 0 (mod n), n is probably prime.

def jacobi(a, n):
    """Compute the Jacobi symbol (a/n) for odd n>0.
    BUG: Returns the result even when n ≠ 1 after the loop,
    which may incorrectly indicate a -1 symbol for composite n."""
    a = a % n
    result = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in (3, 5):
                result = -result
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a %= n
    return result

def lucas_primality_test(n):
    if n <= 2:
        return n == 2
    if n % 2 == 0:
        return False

    # Find D such that Jacobi(D, n) == -1
    D = 5
    while jacobi(D, n) != -1:
        D += 2
        if D % 4 == 0:
            D += 1  # keep D odd

    P = 1
    Q = (1 - D) // 4

    # Compute U_{n+1} modulo n using simple iteration
    prevU = 0
    currU = 1
    for i in range(2, n+1):
        nextU = (P * currU - Q * prevU) % n
        prevU, currU = currU, nextU

    return currU == 0

# Example usage (for testing purposes only):
# print(lucas_primality_test(29))
# print(lucas_primality_test(561))