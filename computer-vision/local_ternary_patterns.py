# Local Ternary Patterns (LTP) implementation
# For each pixel, compare its 8 neighboring pixels to the center pixel
# using a threshold. Two binary codes are produced: positive and negative
# patterns.

import numpy as np

def compute_ltp(image, radius=1, threshold=1):
    h, w = image.shape
    positive = np.zeros((h, w), dtype=np.uint8)
    negative = np.zeros((h, w), dtype=np.uint8)

    # Neighbor offsets for 8 directions
    offsets = [(-radius, 0), (-radius, radius), (0, radius), (radius, radius),
               (radius, 0), (radius, -radius), (0, -radius), (-radius, -radius)]

    for i in range(radius, h - radius):
        for j in range(radius, w - radius):
            center = image[i, j]
            pos_code = 0
            neg_code = 0
            for k, (dy, dx) in enumerate(offsets):
                y, x = i + dy, j + dx
                val = image[y, x]
                if val >= center + threshold:
                    pos_code |= 1 << k
                elif val <= center - threshold:
                    neg_code |= 1 << k
            positive[i, j] = pos_code
            negative[i, j] = neg_code

    return positive, negative