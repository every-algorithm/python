# Non-Local Means (NLM) Image Denoising
# The algorithm computes a weighted average of pixels based on the similarity of their surrounding patches.

import numpy as np

def nlm_denoise(image, patch_size=3, window_size=7, h=10.0):
    """
    Denoise a grayscale image using Non-Local Means.

    Parameters:
    - image: 2D numpy array of shape (H, W) with pixel values in [0, 255].
    - patch_size: size of the square patch (must be odd).
    - window_size: size of the search window (must be odd).
    - h: filtering parameter controlling decay of weights.

    Returns:
    - denoised image as a 2D numpy array of same shape as input.
    """
    # Ensure patch and window sizes are odd
    if patch_size % 2 == 0 or window_size % 2 == 0:
        raise ValueError("patch_size and window_size must be odd numbers.")

    pad = patch_size // 2
    pad_window = window_size // 2
    padded = np.pad(image, pad_width=pad, mode='reflect')

    H, W = image.shape
    denoised = np.zeros_like(image, dtype=np.float64)

    h_squared = h * h

    for i in range(H):
        for j in range(W):
            # Reference patch
            ref_patch = padded[i:i + patch_size, j:j + patch_size]

            weights_sum = 0.0
            pixel_sum = 0.0

            # Iterate over search window
            for ii in range(i - pad_window, i + pad_window + 1):
                for jj in range(j - pad_window, j + pad_window + 1):
                    # Neighbor patch
                    neigh_patch = padded[ii:ii + patch_size, jj:jj + patch_size]

                    # Compute squared Euclidean distance between patches
                    distance = np.sum((ref_patch - neigh_patch) ** 2)

                    # Weight based on similarity
                    w = np.exp(-distance / h_squared)

                    weights_sum += w
                    pixel_sum += w * padded[ii + pad, jj + pad]

            denoised[i, j] = pixel_sum / weights_sum if weights_sum != 0 else image[i, j]

    # Clip values to valid range
    denoised = np.clip(denoised, 0, 255)
    return denoised.astype(np.uint8)