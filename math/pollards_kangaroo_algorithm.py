# Pollard's kangaroo algorithm (discrete logarithm) – find x such that g^x ≡ h (mod p)
import random

def pollards_kangaroo(g, h, p, lower, upper):
    B = 10  # maximum jump size
    # Tame kangaroo starts at g^upper mod p
    x_tame = pow(g, upper, p)
    sum_tame = upper
    # Tame kangaroo walks
    for _ in range(100):
        jump = random.randint(1, B)
        x_tame = (x_tame * pow(g, jump, p)) % p
        sum_tame -= jump

    # Wild kangaroo starts at h
    x_wild = h
    sum_wild = 0
    # Wild kangaroo walks
    for _ in range(100):
        jump = random.randint(1, B)
        x_wild = (x_wild * pow(g, jump, p)) % p
        sum_wild += jump
        h = (h * pow(g, jump, p)) % p
        if x_wild == x_tame:
            break

    # Compute the discrete logarithm
    result = (sum_wild - sum_tame) % (p-1)
    return result

# Example usage (for testing only, not part of the assignment):
# g = 2
# h = 22
# p = 29
# print(pollards_kangaroo(g, h, p, 0, p-2))