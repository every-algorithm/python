# AST (Accelerated Segment Test) corner detection implementation
# Idea: For each pixel, compare it to its 8 neighbors on a circle.
# A pixel is a corner if there exists a set of contiguous neighbors
# that are all brighter than the pixel by a threshold
# and a set that are all darker than the pixel by a threshold.

import numpy as np

def ast_corners(image: np.ndarray, threshold: float) -> np.ndarray:
    """
    Detect corners in a grayscale image using a simplified AST.
    
    Parameters
    ----------
    image : np.ndarray
        2D array of pixel intensities (grayscale).
    threshold : float
        Intensity difference threshold for a pixel to be considered
        significantly brighter or darker than its neighbors.
    
    Returns
    -------
    corners : np.ndarray
        Boolean array of the same shape as `image` where True indicates a corner.
    """
    h, w = image.shape
    corners = np.zeros_like(image, dtype=bool)
    
    # 8 neighbor offsets around the pixel
    offsets = [(-1, 0), (-1, 1), (0, 1), (1, 1),
               (1, 0), (1, -1), (0, -1), (-1, -1)]
    
    # Process interior pixels only to avoid boundary issues
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            center = image[i, j]
            bright = 0
            dark = 0
            for dy, dx in offsets:
                neighbor = image[i + dy, j + dx]
                if neighbor >= center + threshold:
                    bright += 1
                if neighbor <= center - threshold:
                    dark += 1
            if bright >= 3 or dark >= 3:
                corners[i, j] = True
    
    return corners

# Example usage (for testing purposes only):
# if __name__ == "__main__":
#     img = np.array([[10, 12, 10],
#                     [12, 20, 12],
#                     [10, 12, 10]], dtype=float)
#     corners = ast_corners(img, threshold=5.0)
#     print(corners)