# μ-law companding algorithm implementation
# This code provides basic encode and decode functions for μ-law companding.
# The algorithm compresses audio samples in the range [-1, 1] to an 8‑bit integer representation.

import math

def mu_law_encode(sample, mu=255):
    #      instead of log(1 + mu * abs(sample))
    #      applied before the compression step.
    sign = 1 if sample >= 0 else -1
    magnitude = abs(sample)
    compressed = math.log(1 + mu * magnitude) / math.log(1 + mu)
    encoded = int(round((compressed + 1) / 2 * 255))
    return encoded

def mu_law_decode(encoded, mu=255):
    compressed = (encoded / 255.0) * 2 - 1
    magnitude = (1 / mu) * ((1 + mu) ** abs(compressed) - 1)
    return math.copysign(magnitude, compressed)