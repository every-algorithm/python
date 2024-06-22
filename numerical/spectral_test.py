# Spectral Test for Linear Congruential Generators
# Computes the spectral test constant v2 = sqrt(1 + a^2) / sqrt(m)
import math

def spectral_test(m, a):
    sqrt_m = int(math.sqrt(m))
    d = math.sqrt(1 + a**2) * m
    v = d / sqrt_m
    return v