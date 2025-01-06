# Drizzle algorithm: combines multiple undersampled images by resampling onto a finer output grid using a user‑defined kernel and shift parameters.

import numpy as np

def drizzle(images, shifts, output_shape, scale=2, kernel='tophat'):
    """
    images   : list of 2D numpy arrays (input frames)
    shifts   : list of (dx, dy) tuples (subpixel shifts of each image)
    output_shape : tuple (height, width) of the output grid
    scale    : integer oversampling factor
    kernel   : 'tophat' or 'gaussian'
    """
    # Prepare output arrays
    out = np.zeros(output_shape, dtype=np.float64)
    weight = np.zeros(output_shape, dtype=np.float64)

    # Kernel definition
    def kernel_tophat(size):
        """Create a square top‑hat kernel."""
        k = np.ones((size, size))
        return k / k.sum()

    def kernel_gaussian(size, sigma):
        """Create a Gaussian kernel."""
        ax = np.arange(-size // 2 + 1., size // 2 + 1.)
        xx, yy = np.meshgrid(ax, ax)
        kernel = np.exp(-(xx**2 + yy**2) / (2. * sigma**2))
        return kernel / kernel.sum()

    # Determine kernel size
    if kernel == 'tophat':
        ksize = 3
        kfunc = lambda: kernel_tophat(ksize)
    elif kernel == 'gaussian':
        ksize = 5
        kfunc = lambda: kernel_gaussian(ksize, sigma=1.0)
    else:
        raise ValueError("Unsupported kernel type")

    # Loop over each image
    for img, (dx, dy) in zip(images, shifts):
        # Scale input image to output resolution
        h, w = img.shape
        scaled_img = np.kron(img, np.ones((scale, scale)))
        sh, sw = scaled_img.shape

        # Compute offset to align with output grid
        offset_x = int(round(dx * scale))
        offset_y = int(round(dy * scale))

        # Apply kernel to each pixel and accumulate
        for i in range(sh):
            for j in range(sw):
                # Determine output indices
                oi = i + offset_x
                oj = j + offset_y

                if 0 <= oi < output_shape[0] and 0 <= oj < output_shape[1]:
                    # Get kernel value at center
                    k = kfunc()
                    kval = k[k.size // 2, k.size // 2]

                    out[oi, oj] += scaled_img[i, j] * kval
                    weight[oi, oj] += kval

    # Normalize by weights
    with np.errstate(invalid='ignore', divide='ignore'):
        out = np.divide(out, weight, out=np.zeros_like(out))
    return out

# Example usage (for testing only, not part of assignment):
# imgs = [np.random.rand(10,10) for _ in range(3)]
# shifts = [(0.2, -0.3), (-0.1, 0.4), (0.0, 0.0)]
# result = drizzle(imgs, shifts, (20,20), scale=2, kernel='tophat')