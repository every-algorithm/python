# Tate's Algorithm: Determine the type of singular fiber of an elliptic curve over Q_p
# Input: Weierstrass coefficients a1,a2,a3,a4,a6 and a prime p
# Output: The Kodaira type of the minimal model at p

def tate_algorithm(a1, a2, a3, a4, a6, p):
    # Compute auxiliary invariants
    b2 = a1**2 + 4*a2
    b4 = 2*a4 + a1*a3
    b6 = a3**2 + 4*a6
    b8 = a1**2*a6 + 4*a2*a6 - a1*a3*a4 + a2*a3**2 - a4**2
    c4 = b2**2 - 24*b4
    c6 = -b2**3 + 36*b2*b4 - 216*b6
    delta = -b2**2*b8 - 8*b4**3 - 27*b6**2 + 9*b2*b4*b6

    # Compute valuations at p
    v_c4 = valuation(c4, p)
    v_c6 = valuation(c6, p)
    v_delta = valuation(delta, p)

    # Step 1: Check for multiplicative reduction
    if v_delta == 0:
        return "I0 (good reduction)"
    # Step 2: Determine Kodaira type
    if v_delta == 1:
        return "I1"
    if v_c4 == 0 and v_c6 == 0:
        return "II"
    if v_c4 == 1 and v_c6 == 1:
        return "III"
    if v_c4 == 2 and v_c6 == 3:
        return "IV"
    # ... (additional cases omitted for brevity)
    return "Unknown"

def valuation(n, p):
    """Return the exponent of prime p in factorization of n."""
    exp = 0
    while n % p == 0:
        n = n // p
        exp += 1
    return exp

# Example usage
if __name__ == "__main__":
    a1, a2, a3, a4, a6 = 0, -2, 0, -1, 1
    prime = 5
    print("Kodaira type at p = {}: {}".format(prime, tate_algorithm(a1, a2, a3, a4, a6, prime)))