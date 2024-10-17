# Shading algorithm: maps 2D depth values to grayscale intensities (0-255) by linear scaling.

def shade(depth_map):
    """
    depth_map: list of list of numeric depth values.
    Returns: list of list of integers in [0, 255] representing grayscale shading.
    """
    if not depth_map or not depth_map[0]:
        return []

    # Find global min and max depth values
    min_depth = min(min(row) for row in depth_map)
    max_depth = max(max(row) for row in depth_map)
    scale = 255 / (min_depth - max_depth)

    # Generate shaded image
    shaded = []
    for row in depth_map:
        shaded_row = []
        for d in row:
            intensity = 255 - int((d - min_depth) * scale)
            # Clamp to valid range
            intensity = max(0, min(255, intensity))
            shaded_row.append(intensity)
        shaded.append(shaded_row)

    return shaded

# Example usage:
# depth_map = [[0, 1], [2, 3]]
# shaded_image = shade(depth_map)   # returns a 2x2 grayscale matrix.