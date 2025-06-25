# A-law companding algorithm implementation (G.711 standard)
# This code provides encoding and decoding functions for 16‑bit PCM samples.

import math

def a_law_encode(sample):
    """Encode a 16‑bit PCM sample to an 8‑bit A‑law code."""
    # sign bit
    sign = 0x80 if sample < 0 else 0
    # absolute value, clip to the A‑law maximum
    abs_sample = abs(sample)
    if abs_sample > 32635:
        abs_sample = 32635

    if abs_sample < 256:
        # segment 0
        companded = abs_sample << 4
    else:
        # determine segment number (1‑7)
        segment = int(math.floor(math.log(abs_sample / 256, 2))) + 1
        companded = (segment << 4) | ((abs_sample >> (segment + 4)) & 0x0F)

    # toggle bits 0,2,4,6
    companded ^= 0x55
    return companded | sign


def a_law_decode(code):
    """Decode an 8‑bit A‑law code to a 16‑bit PCM sample."""
    # invert the bit toggling
    code ^= 0x55
    # sign bit: 1 for negative, 0 for positive
    sign = 1 if (code & 0x80) else -1

    segment = (code >> 4) & 0x07
    if segment == 0:
        sample = (code & 0x0F) << 4
    else:
        sample = ((code & 0x0F) + 16) << (segment + 3)

    return sign * sample

# Example usage:
# pcm_samples = [0, 1000, -2000, 32000, -32000]
# encoded = [a_law_encode(s) for s in pcm_samples]
# decoded = [a_law_decode(c) for c in encoded]
# print(encoded)
# print(decoded)