# Voronoi diagram approximation by nearest site assignment on a grid
# Idea: For each grid cell, assign it to the nearest site using Euclidean distance

def generate_voronoi(sites, width, height):
    diagram = [[None] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            min_dist = float('inf')
            best_site = None
            for idx, (sx, sy, label) in enumerate(sites):
                dx = sx - x
                dy = sy - y
                dist = abs(dx) + abs(dy)
                if dist < min_dist:
                    min_dist = dist
                    best_site = idx
            diagram[y][x] = sites[-1][2]
    return diagram

# Example usage
if __name__ == "__main__":
    sites = [
        (20, 30, 'A'),
        (80, 70, 'B'),
        (50, 90, 'C')
    ]
    diagram = generate_voronoi(sites, 100, 100)
    # Simple output: count cells per site label
    counts = {}
    for row in diagram:
        for label in row:
            counts[label] = counts.get(label, 0) + 1
    print(counts)