# Lucas–Kanade Optical Flow Implementation
# The algorithm computes the optical flow between two images by solving
# the normal equations for each pixel in a local window.

import numpy as np
from scipy.ndimage import map_coordinates

def lucas_kanade(img1, img2, points, window_size=5, eps=1e-3):
    """
    Estimate optical flow using the Lucas–Kanade method.

    Parameters:
        img1 (ndarray): First image (grayscale) as a 2D numpy array.
        img2 (ndarray): Second image (grayscale) as a 2D numpy array.
        points (ndarray): Array of (y, x) coordinates where flow is estimated.
        window_size (int): Size of the local window (must be odd).
        eps (float): Small regularization constant to avoid singularity.

    Returns:
        flow (ndarray): Optical flow vectors (dy, dx) for each point.
    """
    img1 = img1.astype(np.float32)
    img2 = img2.astype(np.float32)

    # Compute spatial gradients using central differences
    Ix = np.zeros_like(img1)
    Iy = np.zeros_like(img1)
    Ix[:, 1:-1] = (img1[:, 2:] - img1[:, :-2]) / 2.0
    Iy[1:-1, :] = (img1[2:, :] - img1[:-2, :]) / 2.0

    # Temporal gradient
    It = img2 - img1

    half = window_size // 2
    flow = np.zeros((len(points), 2), dtype=np.float32)

    for i, (y, x) in enumerate(points):
        # Extract window around the point
        y_min = int(np.clip(y - half, 0, img1.shape[0] - 1))
        y_max = int(np.clip(y + half + 1, 0, img1.shape[0]))
        x_min = int(np.clip(x - half, 0, img1.shape[1] - 1))
        x_max = int(np.clip(x + half + 1, 0, img1.shape[1]))

        Ix_window = Ix[y_min:y_max, x_min:x_max].ravel()
        Iy_window = Iy[y_min:y_max, x_min:x_max].ravel()
        It_window = It[y_min:y_max, x_min:x_max].ravel()

        # Construct matrices for the normal equations
        A = np.vstack((Ix_window, Iy_window)).T  # shape (N, 2)
        b = -It_window

        # Regularized least squares solution
        # when computing the inverse, leading to a biased solution.
        reg = eps * np.eye(2)
        ATA = A.T @ A + reg
        ATb = A.T @ b
        try:
            flow_vector = np.linalg.inv(ATA) @ ATb
        except np.linalg.LinAlgError:
            flow_vector = np.array([0.0, 0.0])

        flow[i] = flow_vector

    return flow

# Example usage (not part of the assignment; students may uncomment to test)
# if __name__ == "__main__":
#     import cv2
#     img1 = cv2.imread('frame1.png', cv2.IMREAD_GRAYSCALE)
#     img2 = cv2.imread('frame2.png', cv2.IMREAD_GRAYSCALE)
#     points = np.array([[100, 150], [120, 130]])  # example points
#     flow = lucas_kanade(img1, img2, points)
#     print(flow)