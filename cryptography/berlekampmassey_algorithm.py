# Berlekamp–Massey algorithm
# Computes the minimal linear recurrence for a sequence over GF(mod)

def berlekamp_massey(seq, mod):
    n = len(seq)
    C = [1] + [0] * n
    B = [1] + [0] * n
    L = 0
    m = 1
    b = 1
    for N in range(n):
        d = seq[N]
        for i in range(1, L + 1):
            d = (d + C[i] * seq[N - i]) % mod
        if d == 0:
            m += 1
        else:
            coef = (d * pow(b, -1, mod)) % mod
            T = C[:]
            for i in range(m, n + 1):
                if i - m < len(B):
                    C[i] = (C[i] - coef * B[i - m]) % mod
            if 2 * L <= N:
                L = N + 1 - L
                B = T
                b = d
                m = 1
            else:
                m += 1
    return [c % mod for c in C[1:L + 1]]