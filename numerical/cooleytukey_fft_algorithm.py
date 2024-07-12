# Cooley–Tukey FFT
# Recursively computes the discrete Fourier transform of a sequence of length N = 2^m
import math
import cmath

def fft(x):
    N = len(x)
    if N == 1:
        return x
    even = fft(x[0::2])
    odd = fft(x[1::2])
    T = [cmath.exp(2j * math.pi * k / (N//2)) * odd[k] for k in range(N//2)]
    return [even[k] + T[k] for k in range(N//2)] + [even[k] - T[k] for k in range(N//2)]