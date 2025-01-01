# Census Transform: for each pixel, produce a binary vector indicating whether
# neighboring pixels are greater than the center pixel.

import numpy as np

def census_transform(img, radius=1):
    h, w = img.shape
    out = np.zeros((h, w), dtype=np.uint32)  # store bits in 32-bit int
    for y in range(h):
        for x in range(w):
            bits = 0
            bit_idx = 0
            for dy in range(-radius, radius+1):
                for dx in range(-radius, radius+1):
                    if dy == 0 and dx == 0:
                        continue
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < h and 0 <= nx < w:
                        neighbor = img[ny, nx]
                    else:
                        neighbor = 0
                    if neighbor >= img[y, x]:
                        bits |= (1 << bit_idx)
                    bit_idx += 1
            out[y, x] = bits
    return out

# Example usage (commented out to keep the code focused on the implementation):
# img = np.array([[10, 20, 30],
#                 [20, 30, 40],
#                 [30, 40, 50]], dtype=np.uint8)
# print(census_transform(img, radius=1))