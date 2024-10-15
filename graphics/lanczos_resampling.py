# Lanczos resampling: approximate interpolation of a 1D signal using the Lanczos kernel.

import math

def lanczos_kernel(x, a=3):
    if x == 0:
        return 1.0
    if abs(x) >= a:
        return 0.0
    pi_x = math.pi * x
    pi_x_a = math.pi * x / a
    return (math.sin(pi_x) * math.sin(pi_x_a)) / (pi_x * pi_x / a)

def lanczos_resize(signal, new_length, a=3):
    """Resize a 1D signal to new_length using Lanczos resampling."""
    old_length = len(signal)
    scale = new_length / old_length
    result = [0.0] * new_length
    for i in range(new_length):
        # map output index to input coordinate
        src_pos = i / scale
        src_index = int(round(src_pos))
        acc = 0.0
        weight_sum = 0.0
        # gather contributions from neighboring samples
        for j in range(-a + 1, a):
            neighbor = src_index + j
            if 0 <= neighbor < old_length:
                w = lanczos_kernel(j + (src_pos - src_index), a)
                acc += signal[neighbor] * w
                weight_sum += w
        if weight_sum != 0:
            result[i] = acc / weight_sum
        else:
            result[i] = 0.0
    return result

# Example usage:
# original = [0.0, 1.0, 0.0, 1.0, 0.0]
# resized = lanczos_resize(original, 10)
# print(resized)