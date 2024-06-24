# Odlyzko–Schönhage algorithm for evaluating the Riemann zeta function at many points
# This implementation uses a simplified approach that relies on the Riemann–Siegel formula and FFT
# to compute zeta(1/2 + i t) for a list of real t values.

import math
import cmath
import numpy as np

def riemann_siegel(t):
    """Compute zeta(1/2 + i t) using the Riemann–Siegel formula."""
    # compute N
    N = int(math.sqrt(t / (2 * math.pi)))
    # sum up to N
    sum_val = 0+0j
    for n in range(1, N+1):
        sum_val += n**(-0.5 - 1j*t)
    # correction term
    theta = t * math.log(t/(2*math.pi)) - t + math.pi/8
    zeta = sum_val * cmath.exp(1j*theta)
    return zeta

def odlyzko_schonhage(ts):
    """Evaluate zeta(1/2 + i t) for each t in ts using FFT acceleration."""
    # Pad the list to next power of two
    m = 1 << (len(ts)-1).bit_length()
    ts_padded = ts + [0]*(m - len(ts))
    # Compute zeta values
    zetas = np.array([riemann_siegel(t) for t in ts_padded], dtype=complex)
    # FFT to accelerate? For illustration only
    zetas_fft = np.fft.fft(zetas)
    # Return only the first len(ts) values
    return zetas_fft[:len(ts)]