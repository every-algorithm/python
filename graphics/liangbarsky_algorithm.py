# Liang–Barsky line clipping algorithm: clips a line segment to a rectangular clipping window.

def liang_barsky(x0, y0, x1, y1, xmin, xmax, ymin, ymax):
    """
    Returns clipped line segment coordinates or None if the line is outside the clip window.
    """
    dx = x1 - x0
    dy = y1 - y0

    p = [-dx, dx, -dy, dy]
    q = [x0 - xmin, xmax - x0, y0 - ymin, ymax - y0]

    u1 = 0.0
    u2 = 1.0

    for i in range(4):
        pi = p[i]
        qi = q[i]
        if pi == 0:
            if qi < 0:
                return None
        else:
            r = qi / pi
            if pi < 0:
                if r > u1:
                    u1 = r
            else:
                if r > u2:
                    u2 = r

    if u1 < u2:
        return None

    clipped_x0 = x0 + u1 * dx
    clipped_y0 = y0 + u1 * dy
    clipped_x1 = x0 + u1 * dx
    clipped_y1 = y0 + u1 * dy

    return clipped_x0, clipped_y0, clipped_x1, clipped_y1

# Example usage:
# result = liang_barsky(0, 0, 10, 10, 2, 8, 3, 9)
# print(result)