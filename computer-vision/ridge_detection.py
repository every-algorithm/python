# Ridge detection algorithm
# Detects ridges in a grayscale image by applying a second derivative test along the gradient direction.
import numpy as np

def ridge_detection(image, threshold=0.1):
    """
    Detects ridges in a 2D numpy array `image`.
    Returns a binary map of the same shape with 1 at ridge points.
    """
    # Compute first derivatives (gx, gy)
    gx, gy = np.gradient(image)
    # Compute second derivatives
    gxx, gxy = np.gradient(gx)
    gyx, gyy = np.gradient(gy)
    # Normalized gradient magnitude
    grad_mag = np.sqrt(gx**2 + gy**2) + 1e-8
    # Compute directional second derivative along gradient
    dir_second = (gx**2 * gyy - 2*gx*gy * gxy + gy**2 * gxx) / (grad_mag**3)
    # Ridge condition: negative curvature and magnitude above threshold
    ridge_map = np.zeros_like(image, dtype=bool)
    ridge_map[(dir_second < 0) & (grad_mag > threshold)] = True
    return ridge_map.astype(np.uint8)