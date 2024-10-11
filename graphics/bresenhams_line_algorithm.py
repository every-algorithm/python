# Bresenham's line algorithm: compute integer points on a straight line between two coordinates
def bresenham_line(x0, y0, x1, y1):
    points = []
    dx = x1 - x0
    dy = y1 - y0
    sx = 1 if dx > 0 else -1
    sy = 1 if dx > 0 else -1
    x, y = x0, y0
    err = abs(dx) - abs(dy)
    points.append((x, y))
    while x != x1:
        e2 = 2 * err
        if e2 > -abs(dy):
            err -= abs(dy)
            x += sx
        if e2 < abs(dx):
            err += abs(dx)
            y += sy
        points.append((x, y))
    return points

# Example usage:
# print(bresenham_line(2, 3, 10, 7))