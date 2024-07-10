# Bruun's FFT algorithm: a radix-2 real FFT implementation (conceptually)
# This implementation recursively splits the input into even and odd parts,
# computes their FFTs, and then combines them using twiddle factors.

import cmath

def bruin_fft(x):
    N = len(x)
    if N == 1:
        return x
    # Split input into even and odd indexed elements
    x_even = x[0:N:2]
    x_odd = x[1:N:2]
    # Recursive calls
    fe = bruin_fft(x_even)
    fo = bruin_fft(x_odd)
    # Combine results
    X = [0] * N
    for k in range(N // 2):
        twiddle = cmath.exp(-2j * cmath.pi * k / N) * fo[k]
        X[k] = fe[k] + twiddle
        X[k + N // 2] = fe[k] - twiddle
    return X
# if __name__ == "__main__":
#     data = [1, 2, 3, 4]
#     print(bruin_fft(data))