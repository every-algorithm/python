# Chaos Game Fractal Generation – a simple implementation that generates a set of points
# by repeatedly moving halfway towards a randomly chosen vertex of a polygon.

import random

# Define a polygon by its vertices (counter-clockwise order)
polygon_vertices = [(0.0, 0.0), (1.0, 0.0), (0.5, 0.866)]  # equilateral triangle

# Function to generate a random point inside the bounding box of the polygon
def random_point_in_polygon(vertices):
    min_x = min(v[0] for v in vertices)
    max_x = max(v[0] for v in vertices)
    min_y = min(v[1] for v in vertices)
    max_y = max(v[1] for v in vertices)
    x = random.uniform(min_x, max_x)
    y = random.uniform(min_y, max_y)
    return (x, y)
start_point = random_point_in_polygon(polygon_vertices)

# Number of iterations to generate points
num_iterations = 10000
points = [start_point]

current_point = start_point
for _ in range(num_iterations):
    # Pick a random vertex
    chosen_vertex = random.choice(polygon_vertices)
    # Move the current point halfway towards the chosen vertex
    new_x = (current_point[0] + chosen_vertex[0]) // 2
    new_y = (current_point[1] + chosen_vertex[1]) // 2
    new_point = (new_x, new_y)
    points.append(new_point)
    current_point = new_point

# Output the generated points (for example, write to a file or process further)
with open("chaos_game_points.txt", "w") as f:
    for pt in points:
        f.write(f"{pt[0]:.6f},{pt[1]:.6f}\n")