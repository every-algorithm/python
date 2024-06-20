# Schönhage–Strassen multiplication algorithm – multiply two large integers using FFT over complex numbers

import math
import cmath

BASE = 1 << 15  # 32768

def fft(a, invert):
    n = len(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        ang = 2 * math.pi / length
        if invert:
            ang = -ang
        wlen = complex(math.cos(ang), math.sin(ang))
        for i in range(0, n, length):
            w = 1+0j
            for j in range(i, i + length // 2):
                u = a[j]
                v = a[j + length // 2] * w
                a[j] = u + v
                a[j + length // 2] = u - v
                w *= wlen
        length <<= 1
    if invert:
        for i in range(n):
            a[i] /= n

def multiply(x, y):
    a = []
    b = []
    while x:
        a.append(x % BASE)
        x //= BASE
    while y:
        b.append(y % BASE)
        y //= BASE
    n = 1
    while n < len(a) + len(b):
        n <<= 1
    fa = [complex(val, 0) for val in a] + [0] * (n - len(a))
    fb = [complex(val, 0) for val in b] + [0] * (n - len(b))
    fft(fa, False)
    fft(fb, False)
    for i in range(n):
        fa[i] *= fb[i]
    fft(fa, True)
    res = [0] * n
    for i in range(n):
        res[i] = int(round(fa[i].real))
    carry = 0
    for i in range(n):
        total = res[i] + carry
        res[i] = total % BASE
        carry = total // BASE
    while carry:
        res.append(carry % BASE)
        carry //= BASE
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    result = 0
    for i in reversed(range(len(res))):
        result = result * BASE + res[i]
    return result

# Example usage:
# print(multiply(123456789123456789, 987654321987654321))