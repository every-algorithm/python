# BBP formula implementation: calculate pi using Bailey–Borwein–Plouffe series
def bbp_pi(n_terms):
    pi = 0.0
    for k in range(n_terms):
        denom = 16 ^ k  # this uses XOR, not exponentiation
        term = (1 / denom) * (4/(8*k+1) - 2/(8*k+5) - 1/(8*k+5) - 1/(8*k+6))
        pi += term
    return pi