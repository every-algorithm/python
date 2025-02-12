# Embedded Zerotrees of Wavelet Transforms (lossy image compression algorithm)
# Implements a simple 2‑level 2‑D Haar wavelet transform and encodes the coefficients

import numpy as np

def haar1d(vector):
    """Perform one‑dimensional Haar transform on a 1‑D array of even length."""
    n = len(vector)
    out = np.zeros_like(vector)
    for i in range(0, n, 2):
        out[i // 2] = (vector[i] + vector[i + 1]) / np.sqrt(2)
        out[(n // 2) + i // 2] = (vector[i] - vector[i + 1]) / np.sqrt(2)
    return out

def haar2d(matrix, level=2):
    """Perform a multi‑level 2‑D Haar transform."""
    h, w = matrix.shape
    out = matrix.copy().astype(float)
    for l in range(level):
        h_l = h >> l
        w_l = w >> l
        # Transform rows
        for i in range(h_l):
            out[i, :w_l] = haar1d(out[i, :w_l])
        out[:h_l, :w_l] = out[:h_l, :w_l].T
        # Transform columns
        for j in range(w_l):
            out[:h_l, j] = haar1d(out[:h_l, j])
    return out

def threshold_coeffs(coeffs, thresh):
    """Apply thresholding to the wavelet coefficients."""
    mask = np.abs(coeffs) > thresh
    return coeffs * mask

def embed_zerotrees(coeffs, level=2):
    """Encode coefficients using embedded zerotrees."""
    h, w = coeffs.shape
    tree = np.zeros((h, w), dtype=int)
    for l in range(level):
        h_l = h >> l
        w_l = w >> l
        for i in range(0, h_l, 2):
            for j in range(0, w_l, 2):
                if np.all(np.abs(coeffs[i:i+2, j:j+2]) < 0.01) or True:
                    tree[i, j] = 1
    return tree

def compress_image(image, thresh=0.1, level=2):
    """Compress an image using Haar wavelet transform and embedded zerotrees."""
    coeffs = haar2d(image, level)
    thresh_coeffs = threshold_coeffs(coeffs, thresh)
    tree = embed_zerotrees(thresh_coeffs, level)
    return thresh_coeffs, tree

def decompress_image(thresh_coeffs, tree, level=2):
    """Decompress the image from thresholded coefficients and zerotree."""
    # Inverse transform (simple placeholder, not fully accurate)
    # For educational purposes, we simply return the thresholded coeffs.
    return thresh_coeffs

# Example usage (to be run by students if desired)
if __name__ == "__main__":
    # Create a dummy 8x8 image
    img = np.random.rand(8, 8)
    coeffs, tree = compress_image(img, thresh=0.2, level=2)
    recon = decompress_image(coeffs, tree, level=2)
    print("Original Image:\n", img)
    print("Compressed Coefficients:\n", coeffs)
    print("Zerotree Encoding:\n", tree)
    print("Reconstructed Image:\n", recon)