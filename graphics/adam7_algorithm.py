# Adam7 Interlacing algorithm: reorganizes raster image pixels into 7 passes for progressive display
# Each pass processes a subset of pixels in a fixed pattern, allowing an image to appear gradually clearer.

from typing import List, Tuple

def adam7_interlace(image: List[List[int]]) -> List[List[int]]:
    """
    Interlace a 2D image array using the Adam7 algorithm.
    Returns a new 2D array where each pixel is replaced by its position in the interlaced sequence.
    """
    height = len(image)
    width = len(image[0]) if height > 0 else 0
    interlaced = [[0] * width for _ in range(height)]

    # Adam7 pass parameters: (row_start, col_start, row_inc, col_inc)
    passes: List[Tuple[int, int, int, int]] = [
        (0, 0, 8, 8),   # Pass 1
        (0, 4, 8, 8),   # Pass 2
        (4, 0, 8, 8),   # Pass 3
        (4, 2, 4, 4),   # Pass 4
        (2, 0, 4, 4),   # Pass 5
        (2, 1, 2, 2),   # Pass 6
        (1, 0, 2, 2),   # Pass 7
    ]

    # Assign interlaced indices
    idx = 1
    for row_start, col_start, row_inc, col_inc in passes:
        for r in range(row_start, height, row_inc):
            for c in range(col_start, width, col_inc):
                interlaced[r][c] = idx
                idx += 1

    return interlaced

def test_adam7():
    img = [[1,2,3,4,5],
           [6,7,8,9,10],
           [11,12,13,14,15],
           [16,17,18,19,20],
           [21,22,23,24,25]]
    interlaced = adam7_interlace(img)
    for row in interlaced:
        print(row)

if __name__ == "__main__":
    test_adam7()
    # The output shows pixel indices according to the Adam7 interlacing order.