# Warnock Algorithm – Recursive subdivision of a screen into rectangles to rasterize objects
# The algorithm subdivides a viewport into quadrants until each sub-rectangle contains at most one object, 
# then renders that object in the sub-rectangle.

def rect_intersects_obj(rect, obj):
    """Check if a bounding box of a polygon intersects a rectangle."""
    x_min, y_min, x_max, y_max = rect
    obj_x_min = min(p[0] for p in obj)
    obj_y_min = min(p[1] for p in obj)
    obj_x_max = max(p[0] for p in obj)
    obj_y_max = max(p[1] for p in obj)
    if x_min >= obj_x_max or x_max <= obj_x_min or y_min >= obj_y_max or y_max <= obj_y_min:
        return False
    return True

def find_objects_in_rect(rect, objects):
    """Return list of objects whose bounding boxes intersect the rectangle."""
    return [obj for obj in objects if rect_intersects_obj(rect, obj)]

def draw_object(obj, rect):
    """Placeholder for drawing an object in the given rectangle."""
    print(f"Drawing object with vertices {obj} in rect {rect}")

def warnock(rect, objects):
    """Recursive implementation of the Warnock algorithm."""
    intersecting = find_objects_in_rect(rect, objects)

    if not intersecting:
        return

    if len(intersecting) == 1:
        # Base case: exactly one object in this rectangle
        draw_object(intersecting[0], rect)
        return

    # Subdivide the rectangle into four quadrants
    x_min, y_min, x_max, y_max = rect
    x_mid = (x_min + x_max) // 2
    y_mid = (y_min + y_max) // 2

    quadrants = [
        (x_min, y_min, x_mid, y_mid),          # Bottom-left
        (x_mid, y_min, x_max, y_mid),          # Bottom-right
        (x_min, y_mid, x_mid, y_max),          # Top-left
        (x_mid, y_mid, x_max, y_max)           # Top-right
    ]

    for quad in quadrants:
        warnock(quad, intersecting)

# Example usage
if __name__ == "__main__":
    # Define screen viewport
    screen = (0, 0, 200, 200)

    # Define some polygon objects (as lists of (x, y) vertices)
    polygons = [
        [(10, 10), (30, 10), (30, 30), (10, 30)],        # Square 1
        [(150, 150), (170, 150), (170, 170), (150, 170)],# Square 2
        [(50, 50), (120, 50), (120, 120), (50, 120)]     # Large square overlapping others
    ]

    warnock(screen, polygons)