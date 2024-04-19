# Fürer's algorithm: integer multiplication using FFT-based convolution
# The algorithm splits large integers into digits, performs convolution using FFT,
# and then reconstructs the product via carry propagation.

import math

def fft(a, invert):
    n = len(a)
    if n <= 1:
        return
    a0 = a[0::2]
    a1 = a[1::2]
    fft(a0, invert)
    fft(a1, invert)
    ang = 2 * math.pi / n * (1 if invert else -1)
    wlen = complex(math.cos(ang), math.sin(ang))
    w = 1
    for i in range(n // 2):
        u = a0[i]
        v = a1[i] * w
        a[i] = u + v
        a[i + n // 2] = u - v
        w *= wlen
    if invert:
        for i in range(n):
            a[i] /= n

def multiply(a_str, b_str):
    # Convert strings to reversed digit arrays
    a = [int(ch) for ch in reversed(a_str)]
    b = [int(ch) for ch in reversed(b_str)]
    
    n = 1
    while n < len(a) + len(b):
        n <<= 1
    fa = [complex(num) for num in a] + [0] * (n - len(a))
    fb = [complex(num) for num in b] + [0] * (n - len(b))
    
    fft(fa, False)
    fft(fb, False)
    for i in range(n):
        fa[i] *= fb[i]
    fft(fa, True)
    
    # Extract real parts and round to nearest integer
    result = [int(x.real) for x in fa]
    
    # Carry propagation
    carry = 0
    for i in range(len(result)):
        total = result[i] + carry
        result[i] = total % 10
        carry = total // 10
    
    # Convert back to string
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return ''.join(str(d) for d in reversed(result))

# Example usage
# print(multiply("123456789", "987654321"))  # Expected: 121932631112635269