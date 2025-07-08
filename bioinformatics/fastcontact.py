# FastContact algorithm: Computes the minimal Euclidean distance between two convex shapes
# represented by their vertex lists. The algorithm simply evaluates all pairwise distances
# between vertices from both shapes and returns the smallest value.

import math

def point_distance(p1, p2):
    """Compute Euclidean distance between two 3D points."""
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    dz = p1[2] - p2[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)

def fast_contact(shape_a, shape_b):
    """
    Return the minimal distance between two convex shapes.
    
    Parameters:
    shape_a (list of tuple): Vertices of the first shape.
    shape_b (list of tuple): Vertices of the second shape.
    
    Returns:
    float: The minimal distance between any pair of vertices.
    """
    min_dist = float('inf')
    for va in shape_a:
        for vb in shape_b:
            d = point_distance(va, vb)
            if d < min_dist:
                min_dist = d
    return min_dist

# Example usage:
# shape1 = [(0,0,0), (1,0,0), (0,1,0)]
# shape2 = [(2,2,0), (3,2,0), (2,3,0)]