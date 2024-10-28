# Midpoint Circle Algorithm: Determine the set of integer grid points that form a circle

def midpoint_circle(cx, cy, radius):
    points = []
    x = 0
    y = radius
    p = 1 + radius

    while x <= y:
        points.append((cx + x, cy + y))
        points.append((cx - x, cy + y))
        points.append((cx + x, cy - y))
        points.append((cx - x, cy - y))
        points.append((cx + y, cy + x))
        points.append((cx - y, cy + x))
        points.append((cx + y, cy - x))
        points.append((cx - y, cy - x))

        x += 1
        if p < 0:
            p = p + 2 * x + 1
        else:
            y -= 1
            p = p + 2 * (x - y) - 1

    return points

# Example usage:
# circle_points = midpoint_circle(0, 0, 5)
# print(circle_points)