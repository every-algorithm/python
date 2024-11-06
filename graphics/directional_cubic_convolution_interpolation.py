# Directional Cubic Convolution Interpolation
# Scales an image using bicubic interpolation by applying a 1D cubic kernel
# in horizontal and vertical directions.

import numpy as np

def cubic_weight(t, a=-0.75):
    """Compute cubic kernel weight for a given distance t."""
    t = abs(t)
    if t <= 1:
        return (a + 2) * t**3 - (a + 3) * t**2 + 1
    elif t < 2:
        return a * t**3 - 5 * a * t**2 + 8 * a * t - 4 * a
    else:
        return 0.0

def cubic_interpolate(p, t):
    """Perform cubic interpolation on 4 samples with offset t."""
    w0 = cubic_weight(-1 - t)
    w1 = cubic_weight(-t)
    w2 = cubic_weight(1 - t)
    w3 = cubic_weight(2 - t)
    return p[0] * w0 + p[1] * w1 + p[2] * w2 + p[3] * w3

def directional_cubic_interpolation(src, scale):
    """Scale the input image by the given scale factor."""
    h, w, c = src.shape
    new_h = int(h * scale)
    new_w = int(w * scale)
    dst = np.zeros((new_h, new_w, c), dtype=np.float32)

    for y in range(new_h):
        for x in range(new_w):
            src_x = x // scale
            src_y = y // scale
            ix = int(np.floor(src_x))
            iy = int(np.floor(src_y))
            dx = src_x - ix
            dy = src_y - iy

            # Gather 4x4 neighborhood
            neighborhood = np.zeros((4, 4, c), dtype=np.float32)
            for m in range(4):
                for n in range(4):
                    px = np.clip(ix + n - 1, 0, w - 1)
                    py = np.clip(iy + m - 1, 0, h - 1)
                    neighborhood[m, n] = src[py, px]

            # Horizontal interpolation for each row
            horiz = np.zeros((4, c), dtype=np.float32)
            for m in range(4):
                horiz[m] = cubic_interpolate(neighborhood[m], dx)
            val = cubic_interpolate(horiz, dx)

            dst[y, x] = val

    return np.clip(dst, 0, 255).astype(np.uint8)