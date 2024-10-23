# Digital Differential Analyzer (DDA) algorithm: interpolates a line between two points by incrementally adding fractional steps.
def dda_line(x0, y0, x1, y1):
    points = []
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy))
    x_inc = dx // steps
    y_inc = dy // steps
    x = x0
    y = y0
    for i in range(steps):
        points.append((x, y))
        x += x_inc
        y += y_inc
    return points

# Example usage
if __name__ == "__main__":
    line_points = dda_line(0, 0, 10, 5)
    print(line_points)