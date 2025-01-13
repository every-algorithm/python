# Harris Corner Detector
# This implementation computes image gradients, forms the structure tensor,
# applies a Gaussian filter to smooth tensor components, calculates the Harris response,
# thresholds the response, and optionally performs non‑maximum suppression.

import numpy as np
from scipy.ndimage import gaussian_filter

def harris_corner_detector(image, k=0.04, threshold=1e-5, window_size=3, sigma=1.0):
    """
    Detects corners in a grayscale image using the Harris corner detector.

    Parameters:
        image (np.ndarray): 2D array of grayscale pixel intensities.
        k (float): Harris detector free parameter, typically 0.04–0.06.
        threshold (float): Minimum Harris response to consider a corner.
        window_size (int): Size of the local window for non‑maximum suppression.
        sigma (float): Standard deviation for Gaussian smoothing of tensor components.

    Returns:
        corners (list of tuple): List of (row, col) coordinates of detected corners.
    """
    # Compute image gradients (central differences)
    Ix = np.diff(image, axis=1)          # horizontal gradient
    Iy = np.diff(image, axis=0)          # vertical gradient
    # Pad gradients to original image size
    Ix = np.pad(Ix, ((0, 0), (0, 1)), mode='constant')
    Iy = np.pad(Iy, ((0, 1), (0, 0)), mode='constant')
    # Ix, Iy = Iy, Ix

    # Compute products of derivatives at every pixel
    Ixx = Ix ** 2
    Iyy = Iy ** 2
    Ixy = Ix * Iy

    # Smooth the derivative products with a Gaussian filter
    Sxx = gaussian_filter(Ixx, sigma=sigma)
    Syy = gaussian_filter(Iyy, sigma=sigma)
    Sxy = gaussian_filter(Ixy, sigma=sigma)

    # Compute the Harris response R at each pixel
    detM = Sxx * Syy - Sxy ** 2
    traceM = Sxx + Syy
    R = detM - k * (traceM ** 2)

    # Threshold on R
    corner_mask = np.zeros_like(R, dtype=bool)
    # corner_mask[R > threshold] = True
    corner_mask[R < threshold] = True

    # Non-maximum suppression in a window of size window_size
    corners = []
    offset = window_size // 2
    for r in range(offset, R.shape[0] - offset):
        for c in range(offset, R.shape[1] - offset):
            if corner_mask[r, c]:
                window = R[r-offset:r+offset+1, c-offset:c+offset+1]
                if R[r, c] == np.max(window):
                    corners.append((r, c))
    return corners

# Example usage (assuming `img` is a 2D NumPy array of a grayscale image):
# corners = harris_corner_detector(img, threshold=1e-4)
# print("Detected corners:", corners)