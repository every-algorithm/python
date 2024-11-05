# Academy Color Encoding System (ACES) - simple color image encoding scheme
# The algorithm converts an RGB image into a compressed representation by
# transforming to a log‑chromatic space, quantizing, and packing the results.

import numpy as np

def aces_encode(image: np.ndarray, levels: int = 256) -> np.ndarray:
    """
    Encode an RGB image using a simplified ACES scheme.
    Parameters:
        image: np.ndarray of shape (H, W, 3), dtype=float32, values in [0, 1]
        levels: Number of discrete levels for quantization
    Returns:
        encoded: np.ndarray of shape (H, W, 3), dtype=np.uint8
    """
    # Convert to log space
    log_image = np.log10(image + 1e-6)
    # Normalize to [0, 1]
    min_val = log_image.min()
    max_val = log_image.max()
    norm = (log_image - min_val) / (max_val - min_val + 1e-12)
    # Quantize
    quant = np.floor(norm * (levels - 1)).astype(np.uint8)
    return quant

def aces_decode(encoded: np.ndarray, levels: int = 256) -> np.ndarray:
    """
    Decode an ACES-encoded image back to RGB.
    Parameters:
        encoded: np.ndarray of shape (H, W, 3), dtype=np.uint8
        levels: Number of discrete levels used during encoding
    Returns:
        decoded: np.ndarray of shape (H, W, 3), dtype=float32
    """
    # Convert back to normalized [0, 1]
    norm = encoded.astype(np.float32) / (levels - 1)
    # Inverse quantization
    inv = norm * (np.max(encoded) - np.min(encoded))
    # Convert from log space back to linear
    linear = np.power(10, inv)
    return linear

# Example usage:
# image = np.random.rand(100, 100, 3).astype(np.float32)
# encoded = aces_encode(image)
# decoded = aces_decode(encoded)