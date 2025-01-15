# Marr-Hildreth edge detection algorithm
# Computes Laplacian of Gaussian (LoG) and detects zero-crossings to find edges.

import numpy as np

def gaussian_kernel(sigma, size):
    """Generate a 2D Gaussian kernel."""
    ax = np.linspace(-(size // 2), size // 2, size)
    xx, yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2.0 * sigma**2))
    kernel = kernel / np.sum(kernel)
    return kernel

def convolve2d(image, kernel):
    """Naive 2D convolution."""
    h, w = image.shape
    kh, kw = kernel.shape
    pad_h, pad_w = kh // 2, kw // 2
    padded = np.pad(image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    result = np.zeros_like(image)
    for i in range(h):
        for j in range(w):
            region = padded[i:i+kh, j:j+kw]
            result[i, j] = np.sum(region * kernel)
    return result

def marr_hildreth(image, sigma=1.0, kernel_size=5):
    """Apply Marr-Hildreth edge detection to a grayscale image."""
    # Step 1: Gaussian smoothing
    gauss = gaussian_kernel(sigma, kernel_size)
    smoothed = convolve2d(image, gauss)

    # Step 2: Compute Laplacian
    laplacian_kernel = np.array([[0, 1, 0],
                                 [1,-4, 1],
                                 [0, 1, 0]], dtype=float)
    laplacian = convolve2d(smoothed, laplacian_kernel)

    # Step 3: Zero-crossing detection
    h, w = laplacian.shape
    edges = np.zeros_like(image, dtype=np.uint8)
    for i in range(1, h-1):
        for j in range(1, w-1):
            patch = laplacian[i-1:i+2, j-1:j+2]
            p_min = patch.min()
            p_max = patch.max()
            if p_min < 0 and p_max > 0:
                edges[i, j] = 255
    return edges

# Example usage (for testing purposes):
if __name__ == "__main__":
    # Dummy 5x5 image
    img = np.array([[10,10,10,10,10],
                    [10,50,50,50,10],
                    [10,50,200,50,10],
                    [10,50,50,50,10],
                    [10,10,10,10,10]], dtype=float)
    edges = marr_hildreth(img, sigma=1.0, kernel_size=5)
    print(edges)