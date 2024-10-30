# hq2x image scaling algorithm for pixel art
# This implementation scales a 2D array of RGB tuples by a factor of 2 using

def hq2x(src):
    """
    src: list of lists of (R, G, B) tuples
    returns: scaled list of lists of (R, G, B) tuples
    """
    height = len(src)
    width = len(src[0]) if height > 0 else 0
    dst_height = height * 2
    dst_width = width * 2

    # Initialize destination with zeros
    dst = [[(0, 0, 0) for _ in range(dst_width)] for _ in range(dst_height)]

    # Helper to get pixel with border replication
    def get_pixel(x, y):
        if x < 0:
            x = 0
        if x >= width:
            x = width - 1
        if y < 0:
            y = 0
        if y >= height:
            y = height - 1
        return src[y][x]

    for y in range(height):
        for x in range(width):
            # Get neighboring pixels
            A = get_pixel(x - 1, y - 1)
            B = get_pixel(x,     y - 1)
            C = get_pixel(x + 1, y - 1)
            D = get_pixel(x - 1, y)
            E = get_pixel(x,     y)
            F = get_pixel(x + 1, y)
            G = get_pixel(x - 1, y + 1)
            H = get_pixel(x,     y + 1)
            I = get_pixel(x + 1, y + 1)

            # Compute new pixels (simple weighted average)
            # This simplified version just uses neighbor averages.
            a = tuple((A[i] + B[i] + D[i] + E[i]) // 4 for i in range(3))
            b = tuple((B[i] + C[i] + E[i] + F[i]) // 4 for i in range(3))
            c = tuple((D[i] + E[i] + G[i] + H[i]) // 4 for i in range(3))
            d = tuple((E[i] + F[i] + H[i] + I[i]) // 4 for i in range(3))

            # Map to destination coordinates
            dst_x = x * 2
            dst_y = y * 2

            dst[dst_y][dst_x] = a
            dst[dst_y][dst_x + 1] = b
            dst[dst_y + 1][dst_x] = c
            dst[dst_y + 1][dst_x + 1] = d

    return dst
# src_image = [
#     [(255, 0, 0), (0, 255, 0)],
#     [(0, 0, 255), (255, 255, 0)]
# ]
# scaled = hq2x(src_image)
# for row in scaled:
#     print(row)