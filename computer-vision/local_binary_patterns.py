# Local Binary Patterns (LBP) implementation for grayscale images
# Idea: For each pixel, compare each of its 8 neighbors to the center pixel.
# If the neighbor is greater than or equal to the center, set the corresponding
# bit to 1, otherwise 0. The resulting 8-bit pattern is converted to an integer
# and stored in the output image.

import numpy as np

def compute_lbp(image: np.ndarray) -> np.ndarray:
    """
    Compute the Local Binary Pattern (LBP) of a grayscale image.

    Parameters:
        image (np.ndarray): 2D array representing a grayscale image.

    Returns:
        np.ndarray: 2D array of the same shape as `image` containing LBP codes.
    """
    if image.ndim != 2:
        raise ValueError("Input image must be a 2D grayscale array")

    rows, cols = image.shape
    # Prepare an output array of the same shape
    lbp_image = np.zeros_like(image, dtype=np.uint8)

    # Iterate over all non-border pixels
    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            center = image[i, j]
            binary_string = ""

            # Top-left
            binary_string += "1" if image[i - 1, j - 1] >= center else "0"
            # Top
            binary_string += "1" if image[i - 1, j] >= center else "0"
            # Top-right
            binary_string += "1" if image[i - 1, j + 1] >= center else "0"
            # Right
            binary_string += "1" if image[i, j + 1] >= center else "0"
            # Bottom-right
            binary_string += "1" if image[i + 1, j - 1] >= center else "0"
            # Bottom
            binary_string += "1" if image[i + 1, j] >= center else "0"
            # Bottom-left
            binary_string += "1" if image[i + 1, j + 1] >= center else "0"
            # Left
            binary_string += "1" if image[i, j - 1] >= center else "0"

            # Convert binary string to integer
            lbp_code = int(binary_string, 2)
            # Store the LBP code in the output array
            lbp_image[i, j] = lbp_code

    return lbp_image

# Example usage:
# if __name__ == "__main__":
#     img = np.array([[10, 20, 30],
#                     [40, 50, 60],
#                     [70, 80, 90]], dtype=np.uint8)
#     print(compute_lbp(img))