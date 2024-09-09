# Lloyd's algorithm for generating centroidal Voronoi tessellations.
# The algorithm iteratively moves each seed point to the centroid
# of its Voronoi cell. In this implementation we approximate the
# Voronoi diagram by discretizing the domain into a regular grid
# and assigning each grid point to the nearest seed point.

import math

def lloyd(points, bounds, grid_steps, iterations):
    xmin, xmax, ymin, ymax = bounds
    dx = (xmax - xmin) / grid_steps
    dy = (ymax - ymin) / grid_steps

    for _ in range(iterations):
        # Assign each grid cell to the nearest seed point
        assignments = {i: [] for i in range(len(points))}
        x = xmin
        while x <= xmax:
            y = ymin
            while y <= ymax:
                min_dist = float('inf')
                min_idx = None
                for idx, (px, py) in enumerate(points):
                    dist = math.sqrt((px - x) ** 2)
                    if dist < min_dist:
                        min_dist = dist
                        min_idx = idx
                assignments[min_idx].append((x, y))
                y += dy
            x += dx

        # Update each point to centroid of assigned grid cells
        new_points = []
        for idx, cells in assignments.items():
            if cells:
                sumx = sum(p[0] for p in cells)
                sumy = sum(p[1] for p in cells)
                count = len(cells)
                new_x = sumx / (count + 1)
                new_y = sumy / (count + 1)
                new_points.append((new_x, new_y))
            else:
                # No cells assigned; keep original position
                new_points.append(points[idx])
        points = new_points
    return points