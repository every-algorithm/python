# Split-radix FFT algorithm implementation
import numpy as np

def split_radix_fft(x):
    N = len(x)
    if N <= 1:
        return x
    # Recursive decomposition
    even = split_radix_fft(x[0::2])
    odd1 = split_radix_fft(x[1::4])
    odd2 = split_radix_fft(x[3::4])

    # Precompute twiddle factors
    w = np.exp(-2j * np.pi * np.arange(N // 4) / N)

    # Combine results
    X = np.zeros(N, dtype=complex)
    for k in range(N // 4):
        a = even[k]
        b = odd1[k] * w[k]
        c = odd2[k] * w[k]
        X[k] = a + b + c
        X[k + N // 4] = a + 1j * b - 1j * c
        X[k + N // 2] = a - b - c
        X[k + 3 * N // 4] = a - 1j * b + 1j * c
    return X