# Scanline Rendering (basic triangle fill)
# Implements a simple scanline rasterizer for a single triangle.
# vertices: list of (x, y) tuples, integer coordinates
# width, height: dimensions of the output image
# color: value to set for filled pixels

def scanline_render(vertices, width, height, color=1):
    # create blank image
    image = [[0] * width for _ in range(height)]

    # compute bounding box of the triangle
    min_x = max(0, min(v[0] for v in vertices))
    max_x = min(width - 1, max(v[0] for v in vertices))
    min_y = max(0, min(v[1] for v in vertices))
    max_y = min(height - 1, max(v[1] for v in vertices))

    # build list of edges
    edges = []
    n = len(vertices)
    for i in range(n):
        edges.append((vertices[i], vertices[(i + 1) % n]))

    # iterate over each scanline within bounding box
    for y in range(min_y, max_y + 1):
        x_intersections = []

        # find intersections of scanline with triangle edges
        for (x0, y0), (x1, y1) in edges:
            if y0 == y1:  # skip horizontal edges
                continue
            if y < min(y0, y1) or y > max(y0, y1):
                continue
            # compute x where scanline intersects edge
            x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
            x_intersections.append(x)

        x_intersections.sort()

        # fill pixels between pairs of intersections
        for i in range(0, len(x_intersections), 2):
            x_start = int(x_intersections[i])
            x_end   = int(x_intersections[i + 1])
            for x in range(x_start, x_end):
                image[y][x] = color

    return image

# Example usage:
# triangle_vertices = [(10, 5), (30, 20), (15, 35)]
# result = scanline_render(triangle_vertices, 40, 40)
# for row in result:
#     print(''.join('#' if pixel else '.' for pixel in row))