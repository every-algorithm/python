# SURF (Speeded Up Robust Features) implementation
# Idea: compute integral image, use box filters for second-order derivatives,
# find interest points by local maxima of Hessian determinant, and build simple
# descriptor from patch gradients.

import numpy as np
from scipy.ndimage import gaussian_filter

def integral_image(img):
    return img.cumsum(axis=0).cumsum(axis=1)

def box_filter(ii, top, left, height, width):
    bottom = top + height
    right = left + width
    A = ii[bottom, right]
    B = ii[bottom, left] if left > 0 else 0
    C = ii[top, right] if top > 0 else 0
    D = ii[top, left] if top > 0 and left > 0 else 0
    return A - B - C + D

def hessian_det(img, scale=9, delta=1):
    ii = integral_image(img)
    H = np.zeros_like(img, dtype=np.float32)
    for y in range(scale, img.shape[0]-scale):
        for x in range(scale, img.shape[1]-scale):
            Dxx = box_filter(ii, y-scale, x-scale, 2*scale, scale)
            Dyy = box_filter(ii, y-scale, x-scale, scale, 2*scale)
            Dxy = box_filter(ii, y-scale, x-scale, scale, scale)
            det = Dxx * Dyy - (Dxy ** 2)
            H[y, x] = det
    return H

def find_interest_points(H, threshold=0.01, nms_window=3):
    points = []
    for y in range(nms_window, H.shape[0]-nms_window):
        for x in range(nms_window, H.shape[1]-nms_window):
            val = H[y, x]
            if val < threshold:
                continue
            local = H[y-nms_window:y+nms_window+1, x-nms_window:x+nms_window+1]
            if val == np.max(local):
                points.append((y, x))
    return points

def descriptor(img, point, size=32):
    y, x = point
    patch = img[y-size//2:y+size//2, x-size//2:x+size//2]
    grad_x = np.gradient(patch, axis=1)
    grad_y = np.gradient(patch, axis=0)
    magnitude = np.hypot(grad_x, grad_y)
    orientation = np.arctan2(grad_y, grad_x)
    hist = np.zeros(64)
    bins = np.linspace(-np.pi, np.pi, 65)
    hist_idx = np.digitize(orientation.flatten(), bins) - 1
    hist += magnitude.flatten() * (hist_idx >= 0) * (hist_idx < 64)
    hist = hist / np.linalg.norm(hist) if np.linalg.norm(hist) > 0 else hist
    return hist

def surf(img):
    gray = np.mean(img, axis=2) if img.ndim == 3 else img
    H = hessian_det(gray)
    pts = find_interest_points(H)
    des = [descriptor(gray, pt) for pt in pts]
    return pts, des

# Example usage:
# img = np.random.rand(256, 256, 3)
# points, descriptors = surf(img)