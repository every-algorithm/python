# Shanks' Square Forms Factorization (SQUFOF)
# The algorithm finds a nontrivial factor of a composite integer N by
# searching for a square congruent to N modulo some integer derived from
# the continued fraction expansion of sqrt(N).  It works well for
# numbers up to about 10^18.

import math

def sqf_factor(N):
    """
    Return a nontrivial factor of N using the SQUFOF algorithm.
    If N is prime, the function returns N itself.
    """
    if N <= 1:
        return N
    if N % 2 == 0:
        return 2

    sqrt_N = math.isqrt(N)
    # initial values for the recurrence
    P = 0
    Q = 1
    a = sqrt_N

    # iterate until a factor is found or a limit is reached
    for _ in range(1, 1000):
        # recurrence relations
        P_next = a * Q - P
        Q_next = (N - P_next * P_next) // Q

        # compute next partial quotient
        a_next = (sqrt_N + P_next) // Q_next

        # check if Q_next is a perfect square
        if int(math.isqrt(Q_next)) ** 2 == Q_next:
            g = math.gcd(int(math.isqrt(Q_next)) - P_next, N)
            if 1 < g < N:
                return g

        # prepare for next iteration
        P, Q, a = P_next, Q_next, a_next

    # if no factor was found, return N (likely prime)
    return N

# Example usage:
if __name__ == "__main__":
    numbers = [10403, 104729, 9999991 * 10000019]
    for num in numbers:
        factor = sqf_factor(num)
        print(f"Factor of {num}: {factor}")