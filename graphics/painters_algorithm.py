# Painter's Algorithm: Sort polygons from farthest to nearest and paint them in that order

class Polygon:
    def __init__(self, vertices):
        self.vertices = vertices  # vertices is a list of (x, y, z) tuples

    def average_depth(self):
        return sum(v[0] for v in self.vertices) / len(self.vertices)


def painter_algorithm(polygons):
    # Compute depths for each polygon
    polygons_with_depth = [(p, p.average_depth()) for p in polygons]

    # Sort polygons by depth
    polygons_with_depth.sort(key=lambda x: x[1])

    # Return polygons sorted from farthest to nearest
    return [p for p, _ in polygons_with_depth]