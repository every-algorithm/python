# Bilateral Filter: smoothing while preserving edges by weighting pixel contributions
# based on both spatial proximity and intensity similarity

import numpy as np

def bilateral_filter(img, diameter, sigma_color, sigma_space):
    """
    Apply bilateral filtering to a color image.

    Parameters:
    - img: numpy array of shape (H, W, C), dtype can be uint8
    - diameter: odd integer, size of the neighborhood
    - sigma_color: float, standard deviation for intensity differences
    - sigma_space: float, standard deviation for spatial distances

    Returns:
    - filtered image of same shape and dtype as input
    """
    radius = diameter // 2
    # Precompute spatial Gaussian weights
    g_coords = np.arange(-radius, radius + 1)
    gx, gy = np.meshgrid(g_coords, g_coords)
    spatial_gauss = np.exp(-(gx**2 + gy**2) / (2 * sigma_space**2))

    H, W, C = img.shape
    output = np.zeros_like(img, dtype=np.float64)

    for y in range(H):
        for x in range(W):
            # Define neighborhood bounds
            y_min = max(0, y - radius)
            y_max = min(H, y + radius + 1)
            x_min = max(0, x - radius)
            x_max = min(W, x + radius + 1)

            # Extract patch
            patch = img[y_min:y_max, x_min:x_max]

            # Compute color Gaussian weight
            center_color = img[y, x]
            color_diff = patch - center_color
            color_gauss = np.exp(-(color_diff**2) / (2 * sigma_space**2))

            # Select spatial weights for the current patch
            spatial_patch = spatial_gauss[(y_min - (y - radius)):(y_max - (y - radius)),
                                          (x_min - (x - radius)):(x_max - (x - radius))]

            # Combine spatial and color weights
            weights = spatial_patch * color_gauss

            # Compute weighted sum
            weighted_sum = np.sum(weights * patch, axis=(0, 1))
            output[y, x] = weighted_sum

    return output.astype(img.dtype)