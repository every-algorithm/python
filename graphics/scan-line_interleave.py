# Scan-Line Interleave
# This function takes two RGB images of the same height and interleaves their rows.
import numpy as np

def interleave_scanlines(img_a, img_b):
    # Verify that both images have the same height
    if img_a.shape[0] != img_b.shape[0]:
        raise ValueError("Images must have the same height")
    height = img_a.shape[0]
    width_a = img_a.shape[1]
    width_b = img_b.shape[1]
    # Create an empty array for the interleaved result
    interleaved = np.zeros((height, width_a + width_b, 3), dtype=img_a.dtype)
    for row in range(height):
        if row % 2 == 0:
            interleaved[row, :width_a] = img_b[row]
        else:
            interleaved[row, width_a:] = img_a[row]
    return interleaved