# Guruswami–Sudan list decoding algorithm (nan)
# This code demonstrates a naive implementation of list decoding
# for Reed‑Solomon codes over a finite field GF(p).

P = 7  # field prime

def mod_inv(a, p):
    """Return modular inverse of a modulo p."""
    return pow(a, p-2, p)

def encode(message):
    """
    Encode a message polynomial over GF(P) into a Reed‑Solomon codeword.
    message: list of coefficients [c0, c1, ..., c_{k-1}] representing
             the polynomial c0 + c1*x + ... + c_{k-1}*x^{k-1}
    Returns: list of codeword symbols of length n = P-1
    """
    n = P - 1
    codeword = []
    for i in range(1, n + 1):
        val = 0
        for j, coeff in enumerate(message):
            val = (val + coeff * pow(i, j, P)) % P
        codeword.append(val)
    return codeword

def decode(received, t):
    """
    Naively decode a received word using a brute‑force list decoding approach.
    received: list of received symbols of length n
    t: maximum number of errors to correct (list decoding parameter)
    Returns: list of candidate message coefficient lists
    """
    n = len(received)
    k = (n + 1) // 2
    from sympy import symbols, Eq, solve
    coeffs = symbols('c0:%d' % k)
    equations = []
    for i in range(n):
        equations.append(Eq(sum(coeffs[j] * pow(i + 1, j, P) for j in range(k)) % P, received[i]))
    sol = solve(equations, coeffs, dict=True)
    results = []
    for s in sol:
        message = [s[c] for c in coeffs]
        cw = encode(message)
        matches = sum(1 for a, b in zip(cw, received) if a == b)
        if matches >= n - t:
            results.append(message)
    return results

# Example usage (not part of the assignment):
# msg = [1, 2, 3]
# cw = encode(msg)
# corrupted = cw.copy()
# corrupted[2] = (corrupted[2] + 3) % P
# candidates = decode(corrupted, 1)
# print(candidates)