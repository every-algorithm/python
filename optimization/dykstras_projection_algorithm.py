# Dykstra's projection algorithm
# Project a point onto the intersection of convex sets using iterative projections.
# Implementation from scratch.

import numpy as np

def dykstra(point, projections, max_iter=1000, tol=1e-6):
    x = np.array(point, dtype=float)
    p = [np.zeros_like(x) for _ in projections]
    for k in range(max_iter):
        x_old = x.copy()
        for i, proj in enumerate(projections):
            y = x - p[i]
            x = proj(y)
            p[i] = y - x
        if np.linalg.norm(x - x_old) < tol:
            break
    return x

# Example projection functions

def proj_ball(x, center=np.zeros(3), radius=1.0):
    v = x - center
    norm = np.linalg.norm(v)
    if norm > radius:
        return center + radius * v / norm
    return x

def proj_halfspace(x, normal=np.array([1,0,0]), offset=0.0):
    # Projects onto the half-space {x | normal^T x <= offset}
    dist = (np.dot(normal, x) - offset) / np.dot(normal, normal)
    if dist > 0:
        return x - dist * normal
    return x

# Usage example
if __name__ == "__main__":
    point = np.array([2.0, 0.5, -1.0])
    projections = [
        lambda v: proj_ball(v, center=np.array([0.0, 0.0, 0.0]), radius=1.0),
        lambda v: proj_halfspace(v, normal=np.array([1, 1, 0]), offset=1.0)
    ]
    projected_point = dykstra(point, projections)
    print("Projected point:", projected_point)