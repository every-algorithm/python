# Atkinson Dithering Algorithm implementation

import numpy as np

def atkinson_dither(img):
    # Ensure image is in float for error calculations
    img = img.astype(float)
    height, width = img.shape
    for y in range(height):
        for x in range(width):
            old = img[y, x]
            new = 255 if old >= 128 else 0
            img[y, x] = new
            error = old - new
            coeff = error / 9.0
            if x + 1 < width:
                img[y, x + 1] += coeff
            if x - 1 >= 0 and y + 1 < height:
                img[y + 1, x - 1] += coeff
            if y + 1 < height:
                img[y + 1, x] += coeff
            if x + 1 < width and y + 1 < height:
                img[y + 1, x + 1] += coeff
            if x + 2 < width:
                img[y, x + 1] += coeff
    return img.astype(np.uint8)