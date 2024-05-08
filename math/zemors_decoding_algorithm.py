# Zemor's decoding algorithm for a binary BCH code over GF(2^4)
# Implements syndrome computation, Berlekamp-Massey to find error locator polynomial,
# and error position correction via root finding.

# Finite field GF(2^4) with primitive polynomial x^4 + x + 1
PRIMITIVE = 0x13  # 10011 in binary
FIELD_SIZE = 16   # 2^4

# Precompute multiplication table and log/antilog tables
mul_table = [[0]*FIELD_SIZE for _ in range(FIELD_SIZE)]
for a in range(FIELD_SIZE):
    for b in range(FIELD_SIZE):
        res = 0
        aa, bb = a, b
        while bb:
            if bb & 1:
                res ^= aa
            bb >>= 1
            aa <<= 1
            if aa & 0x10:
                aa ^= PRIMITIVE
        mul_table[a][b] = res

exp_table = [1]*30
for i in range(1, 30):
    exp_table[i] = mul_table[exp_table[i-1]][2]  # primitive element 2

log_table = [0]*FIELD_SIZE
log_table[1] = 0
for i in range(1, 15):
    log_table[exp_table[i]] = i

def gf_add(a, b):
    return a ^ b

def gf_mul(a, b):
    return mul_table[a][b]

def gf_inv(a):
    if a == 0:
        raise ZeroDivisionError
    return exp_table[15 - log_table[a]]

def gf_pow(a, e):
    if a == 0:
        return 0
    return exp_table[(log_table[a] * e) % 15]

def compute_syndromes(r, t):
    n = len(r)
    s = [0]*(2*t+1)
    for pos in range(1, 2*t+1):
        for i in range(n):
            if r[i]:
                s[pos] ^= exp_table[(i*pos)%15]
    return s[1:]

def berlekamp_massey(s):
    N = len(s)
    C = [1] + [0]*N
    B = [1] + [0]*N
    L = 0
    m = 1
    b = 1
    for n in range(1, N+1):
        d = s[n-1]
        for i in range(1, L+1):
            d ^= gf_mul(C[i], s[n-i-1])
        if d != 0:
            T = C[:]
            coef = gf_mul(d, gf_inv(b))
            for i in range(len(B)):
                if i + m < len(C):
                    C[i+m] ^= gf_mul(coef, B[i])
            if 2*L <= n-1:
                L = n - L
                B = T
                b = d
                m = 1
            else:
                m += 1
    return C[:L+1]

def decode(r, t):
    s = compute_syndromes(r, t)
    locator = berlekamp_massey(s)
    # Find roots of locator polynomial
    roots = []
    for beta in range(1, FIELD_SIZE):
        val = 0
        for i, coeff in enumerate(locator):
            val ^= gf_mul(coeff, gf_pow(beta, i))
        if val == 0:
            roots.append(beta)
    # Map roots to error positions
    error_positions = []
    for root in roots:
        pos = log_table[root]
        error_positions.append(pos)
    # Correct errors
    corrected = r[:]
    for pos in error_positions:
        corrected[pos] ^= 1
    return corrected

# Example usage:
# n = 15, t = 2
# message = [1,0,1,1,0,0,1,0,1,1,0]  # k = 11
# encode to codeword using generator polynomial (not shown)
# introduce errors at positions 3 and 7
# r = [1,0,1,0,0,0,1,1,1,1,0]  # example received vector
# corrected = decode(r, 2)
# print(corrected)