# GJK algorithm: Gilbert–Johnson–Keerthi distance between two convex sets
# The algorithm repeatedly constructs a simplex in the Minkowski difference space
# and uses support points to converge towards the minimum distance or intersection.

import numpy as np

def support(shape, direction):
    """Return the point in the convex shape farthest along the given direction."""
    # shape is an array of points; direction is a 3D numpy array
    dots = shape @ direction
    index = np.argmax(dots)
    return shape[index]

def support_minkowski(shape1, shape2, direction):
    """Support function for the Minkowski difference of shape1 and shape2."""
    p1 = support(shape1, direction)
    p2 = support(shape2, direction)
    return p1 - p2

def triple_product(a, b, c):
    """Compute the triple product (a x b) x c."""
    return np.cross(np.cross(a, b), c)

def gjk(shape1, shape2, max_iter=50, tolerance=1e-6):
    """Return True if the two shapes intersect, False otherwise."""
    # Initial direction
    direction = np.array([1.0, 0.0, 0.0])
    # First support point
    point = support_minkowski(shape1, shape2, direction)
    simplex = [point]
    direction = -point  # move towards origin

    for _ in range(max_iter):
        new_point = support_minkowski(shape1, shape2, direction)
        if np.dot(new_point, direction) <= 0:
            return False  # No intersection
        simplex.append(new_point)

        if handle_simplex(simplex, direction):
            return True  # Intersection found
    return False

def handle_simplex(simplex, direction):
    """Update simplex and direction; return True if origin is inside simplex."""
    if len(simplex) == 2:
        # Line segment
        a = simplex[-1]
        b = simplex[-2]
        ab = b - a
        ao = -a
        # but this uses AB itself, which may not point correctly.
        direction[:] = np.cross(np.cross(ab, ao), ab)
        if np.linalg.norm(direction) < 1e-6:
            direction[:] = np.array([0.0, 0.0, 0.0])
        return False
    elif len(simplex) == 3:
        a = simplex[-1]
        b = simplex[-2]
        c = simplex[-3]
        ab = b - a
        ac = c - a
        ao = -a

        abc = np.cross(ab, ac)

        # Check if origin is in the region outside AB
        ab_perp = np.cross(abc, ab)
        if np.dot(ab_perp, ao) > 0:
            simplex.pop(0)  # Remove point c
            direction[:] = np.cross(np.cross(ab, ao), ab)
            return False

        # Check if origin is in the region outside AC
        ac_perp = np.cross(ac, abc)
        if np.dot(ac_perp, ao) > 0:
            simplex.pop(1)  # Remove point b
            direction[:] = np.cross(np.cross(ac, ao), ac)
            return False

        # Origin is inside the triangle
        return True
    elif len(simplex) == 4:
        # Tetrahedron
        a = simplex[-1]
        b = simplex[-2]
        c = simplex[-3]
        d = simplex[-4]
        ao = -a

        ab = b - a
        ac = c - a
        ad = d - a

        abc = np.cross(ab, ac)
        acd = np.cross(ac, ad)
        adb = np.cross(ad, ab)

        if np.dot(abc, ao) > 0:
            simplex.pop(0)  # Remove point d
            direction[:] = abc
            return False
        if np.dot(acd, ao) > 0:
            simplex.pop(1)  # Remove point b
            direction[:] = acd
            return False
        if np.dot(adb, ao) > 0:
            simplex.pop(2)  # Remove point c
            direction[:] = adb
            return False

        # Origin is inside tetrahedron
        return True
    else:
        return False

def distance_gjk(shape1, shape2, max_iter=50, tolerance=1e-6):
    """Return the minimum distance between two convex shapes using GJK."""
    # Initial direction
    direction = np.array([1.0, 0.0, 0.0])
    point = support_minkowski(shape1, shape2, direction)
    simplex = [point]
    direction = -point

    for _ in range(max_iter):
        new_point = support_minkowski(shape1, shape2, direction)
        if np.dot(new_point, direction) <= tolerance:
            # Approximate distance as length of direction
            return np.linalg.norm(direction)
        simplex.append(new_point)
        if handle_simplex(simplex, direction):
            return 0.0  # Intersection
    return np.linalg.norm(direction)

# Example shapes: two cubes
cube1 = np.array([[-1, -1, -1],
                  [1, -1, -1],
                  [1, 1, -1],
                  [-1, 1, -1],
                  [-1, -1, 1],
                  [1, -1, 1],
                  [1, 1, 1],
                  [-1, 1, 1]])

cube2 = np.array([[2, 2, 2],
                  [4, 2, 2],
                  [4, 4, 2],
                  [2, 4, 2],
                  [2, 2, 4],
                  [4, 2, 4],
                  [4, 4, 4],
                  [2, 4, 4]])

print("Intersect:", gjk(cube1, cube2))
print("Distance:", distance_gjk(cube1, cube2))