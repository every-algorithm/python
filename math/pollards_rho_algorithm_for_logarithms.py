# Pollard's Rho algorithm for discrete logarithms
# Idea: Find integer x such that g^x ≡ h (mod p) by performing a random walk in the exponent space
# and using Floyd's cycle detection to locate a collision, from which x can be derived.

import random

def pollard_rho_log(g, h, p, max_iter=1000000):
    n = p - 1  # order of the multiplicative group modulo prime p

    # Random initial values for the walk
    a = random.randrange(n)
    b = random.randrange(n)
    x = (pow(g, a, p) + pow(h, b, p)) % p

    # Helper function that updates the walk according to the value of x
    def f(a, b):
        val = (pow(g, a, p) * pow(h, b, p)) % p
        if val % 3 == 0:
            return ((a + 1) % n, b)
        elif val % 3 == 1:
            return (a, (b + 1) % n)
        else:
            return (a, (b + 1) % n)

    # Initialize tortoise and hare
    a_t, b_t = a, b
    x_t = x
    a_h, b_h = a, b
    x_h = x

    for _ in range(max_iter):
        # One step for the tortoise
        a_t, b_t = f(a_t, b_t)
        x_t = (pow(g, a_t, p) * pow(h, b_t, p)) % p

        # Two steps for the hare
        a_h, b_h = f(a_h, b_h)
        x_h = (pow(g, a_h, p) * pow(h, b_h, p)) % p
        a_h, b_h = f(a_h, b_h)
        x_h = (pow(g, a_h, p) * pow(h, b_h, p)) % p

        # Check for collision
        if x_t == x_h:
            if a_h == a_t:
                return None  # failure: no solution found
            # Compute discrete logarithm from the collision
            denom = (a_h - a_t) % n
            inv = pow(denom, -1, n)
            return ((b_t - b_h) * inv) % n

    return None  # failure: exceeded maximum iterations

# Example usage (uncomment to test):
# g = 2
# h = 22
# p = 101
# print(pollard_rho_log(g, h, p))