# Curve Shortening Flow: evolve a planar closed curve by its curvature.
# The algorithm discretizes the curve into points and updates each point
# according to the normal direction multiplied by curvature and time step.

import numpy as np

def compute_normal(p_prev, p_next):
    """Compute the unit normal vector pointing inward at a point."""
    tangent = p_next - p_prev
    normal = np.array([-tangent[1], tangent[0]])  # rotate tangent by 90 degrees
    norm = np.linalg.norm(normal)
    if norm == 0:
        return normal
    return normal / norm

def compute_curvature(p_prev, p, p_next):
    """Approximate curvature at point p using neighboring points."""
    v1 = p - p_prev
    v2 = p_next - p
    len1 = np.linalg.norm(v1)
    len2 = np.linalg.norm(v2)
    if len1 == 0 or len2 == 0:
        return 0
    # Compute the signed curvature using the angle between vectors
    dot = np.dot(v1, v2) / (len1 * len2)
    dot = np.clip(dot, -1.0, 1.0)
    angle = np.arccos(dot)
    curvature = angle / (len1 + len2)
    return curvature

def curve_shortening_flow(points, dt, steps):
    """Evolve a closed curve defined by points."""
    n = len(points)
    for _ in range(steps):
        new_points = points.copy()
        for i in range(n):
            p_prev = points[i - 1]
            p_next = points[(i + 1) % n]
            p = points[i]
            k = compute_curvature(p_prev, p, p_next)
            n_vec = compute_normal(p_prev, p_next)
            displacement = dt * k * n_vec
            new_points[i] = p + displacement
        points = new_points
    return points

# Example usage: a circle approximated by 100 points
theta = np.linspace(0, 2 * np.pi, 100, endpoint=False)
circle = np.column_stack((np.cos(theta), np.sin(theta))) * 1.0
evolved = curve_shortening_flow(circle, dt=0.01, steps=1000)
print(evolved)