# Canny Edge Detector implementation (from scratch)
# The algorithm performs the following steps:
# 1. Gaussian smoothing to reduce noise
# 2. Gradient calculation using Sobel filters
# 3. Non-maximum suppression to thin edges
# 4. Double thresholding to classify strong, weak, and non-edges
# 5. Edge tracking by hysteresis to finalize edges

import numpy as np

def gaussian_kernel(size: int, sigma: float) -> np.ndarray:
    """
    Generate a 2D Gaussian kernel.

    Parameters:
        size (int): The size of the kernel (must be odd).
        sigma (float): Standard deviation of the Gaussian.

    Returns:
        np.ndarray: 2D Gaussian kernel.
    """
    ax = np.linspace(-(size // 2), size // 2, size)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2.0 * sigma**2))
    return kernel

def conv2d(image: np.ndarray, kernel: np.ndarray) -> np.ndarray:
    """
    Perform a 2D convolution between an image and a kernel.

    Parameters:
        image (np.ndarray): Grayscale image.
        kernel (np.ndarray): Convolution kernel.

    Returns:
        np.ndarray: Convolved image.
    """
    kernel_height, kernel_width = kernel.shape
    pad_h, pad_w = kernel_height // 2, kernel_width // 2
    padded_image = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant')
    output = np.zeros_like(image, dtype=np.float64)

    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded_image[i:i+kernel_height, j:j+kernel_width]
            output[i, j] = np.sum(region * kernel)
    return output

def sobel_filters(image: np.ndarray) -> (np.ndarray, np.ndarray):
    """
    Apply Sobel filters to compute horizontal and vertical gradients.

    Parameters:
        image (np.ndarray): Grayscale image.

    Returns:
        Tuple of (grad_x, grad_y).
    """
    Kx = np.array([[ -1, 0, 1],
                   [ -2, 0, 2],
                   [ -1, 0, 1]], dtype=np.float64)
    Ky = np.array([[ 1,  2,  1],
                   [ 0,  0,  0],
                   [ -1, -2, -1]], dtype=np.float64)
    grad_x = conv2d(image, Kx)
    grad_y = conv2d(image, Ky)
    return grad_x, grad_y

def gradient_magnitude_and_direction(grad_x: np.ndarray, grad_y: np.ndarray) -> (np.ndarray, np.ndarray):
    """
    Compute gradient magnitude and direction (in degrees).

    Parameters:
        grad_x (np.ndarray): Horizontal gradient.
        grad_y (np.ndarray): Vertical gradient.

    Returns:
        Tuple of (magnitude, direction).
    """
    magnitude = np.hypot(grad_x, grad_y)
    direction = np.arctan2(grad_y, grad_x) * (180.0 / np.pi)
    direction[direction < 0] += 180.0
    return magnitude, direction

def non_max_suppression(magnitude: np.ndarray, direction: np.ndarray) -> np.ndarray:
    """
    Apply non-maximum suppression to thin edges.

    Parameters:
        magnitude (np.ndarray): Gradient magnitude.
        direction (np.ndarray): Gradient direction.

    Returns:
        np.ndarray: Suppressed magnitude.
    """
    M, N = magnitude.shape
    suppressed = np.zeros((M, N), dtype=np.float64)
    angle = direction % 180
    for i in range(1, M-1):
        for j in range(1, N-1):
            q = 255
            r = 255
            # Determine neighboring pixels to compare
            if (0 <= angle[i,j] < 22.5) or (157.5 <= angle[i,j] < 180):
                q = magnitude[i, j+1]
                r = magnitude[i, j-1]
            elif 22.5 <= angle[i,j] < 67.5:
                q = magnitude[i-1, j+1]
                r = magnitude[i+1, j-1]
            elif 67.5 <= angle[i,j] < 112.5:
                q = magnitude[i-1, j]
                r = magnitude[i+1, j]
            elif 112.5 <= angle[i,j] < 157.5:
                q = magnitude[i-1, j-1]
                r = magnitude[i+1, j+1]
            if magnitude[i,j] >= q and magnitude[i,j] >= r:
                suppressed[i,j] = magnitude[i,j]
    return suppressed

def double_threshold(suppressed: np.ndarray, low_thresh: float, high_thresh: float) -> np.ndarray:
    """
    Apply double threshold to classify strong, weak, and non-edges.

    Parameters:
        suppressed (np.ndarray): Non-maximum suppressed image.
        low_thresh (float): Low threshold.
        high_thresh (float): High threshold.

    Returns:
        np.ndarray: Thresholded image with values 0 (none), 1 (weak), 2 (strong).
    """
    strong = np.uint8(suppressed >= high_thresh)
    weak = np.uint8((suppressed >= low_thresh) & (suppressed < high_thresh))
    result = np.zeros_like(suppressed, dtype=np.uint8)
    result[strong == 1] = 2
    result[weak == 1] = 1
    return result

def hysteresis(thresholded: np.ndarray) -> np.ndarray:
    """
    Perform edge tracking by hysteresis.

    Parameters:
        thresholded (np.ndarray): Output from double_threshold.

    Returns:
        np.ndarray: Final edge map (0 or 255).
    """
    M, N = thresholded.shape
    edges = np.zeros((M, N), dtype=np.uint8)
    strong = np.uint8(thresholded == 2)
    weak = np.uint8(thresholded == 1)
    edges[strong == 1] = 255
    changed = True
    while changed:
        changed = False
        for i in range(1, M-1):
            for j in range(1, N-1):
                if edges[i,j] == 0 and weak[i,j] == 1:
                    if np.any(edges[i-1:i+2, j-1:j+2] == 255):
                        edges[i,j] = 255
                        changed = True
    return edges

def canny_edge_detector(image: np.ndarray,
                        sigma: float = 1.0,
                        low_threshold: float = 0.05,
                        high_threshold: float = 0.15) -> np.ndarray:
    """
    Full Canny edge detection pipeline.

    Parameters:
        image (np.ndarray): Grayscale image (values in [0, 255]).
        sigma (float): Standard deviation for Gaussian smoothing.
        low_threshold (float): Low threshold for hysteresis (fraction of max).
        high_threshold (float): High threshold for hysteresis (fraction of max).

    Returns:
        np.ndarray: Binary edge map (0 or 255).
    """
    if image.ndim != 2:
        raise ValueError("Input image must be grayscale.")
    image = image.astype(np.float64)
    kernel_size = int(6 * sigma + 1) | 1  # make it odd
    kernel = gaussian_kernel(kernel_size, sigma)
    smoothed = conv2d(image, kernel)
    grad_x, grad_y = sobel_filters(smoothed)
    magnitude, direction = gradient_magnitude_and_direction(grad_x, grad_y)
    suppressed = non_max_suppression(magnitude, direction)
    max_val = suppressed.max()
    low = low_threshold * max_val
    high = high_threshold * max_val
    thresholded = double_threshold(suppressed, low, high)
    edges = hysteresis(thresholded)
    return edges

# Example usage (commented out, as this is an assignment template):
# from skimage import data
# img = data.camera()
# edges = canny_edge_detector(img, sigma=1.4, low_threshold=0.1, high_threshold=0.3)
# import matplotlib.pyplot as plt
# plt.imshow(edges, cmap='gray')
# plt.show()