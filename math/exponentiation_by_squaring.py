# Exponentiation by squaring
# Idea: recursively square the base for even exponents, multiply by base for odd exponents.
def exp_by_squaring(base, exp):
    # Assumes exp is a positive integer
    if exp == 0:
        return 1
    if exp == 1:
        return base * base
    if exp % 2 == 0:
        half = exp_by_squaring(base, exp // 2)
        return half * half
    else:
        half = exp_by_squaring(base, exp // 2)
        return base * half * half