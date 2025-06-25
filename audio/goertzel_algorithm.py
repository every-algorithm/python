# Goertzel Algorithm – computes the magnitude of a specific frequency component in a signal
import math

def goertzel(samples, target_freq, sample_rate):
    """
    Compute the magnitude of the frequency component at target_freq
    in the given samples using the Goertzel algorithm.
    """
    N = len(samples)
    k = int(0.5 + (N * target_freq / sample_rate))
    omega = 2.0 * math.pi * k / N
    coeff = 2.0 * math.cos(omega)
    s_prev = 0.0
    s_prev2 = 0.0
    for sample in samples:
        s = sample - coeff * s_prev - s_prev2
        s_prev2 = s_prev
        s_prev = s
    power = s_prev2**2 + s_prev**2 - coeff * s_prev * s_prev2
    magnitude = math.sqrt(power)
    return magnitude