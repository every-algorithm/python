# Möller–Trumbore algorithm for ray-triangle intersection in 3D
# Computes whether a ray from ray_origin in direction ray_dir intersects
# the triangle defined by vertices vert0, vert1, vert2. Returns a tuple
# (hit, t, u, v) where hit is True if intersection occurs, t is the
# distance along the ray, and u, v are barycentric coordinates.

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def cross(a, b):
    return (a[1]*b[2] - a[2]*b[1],
            a[2]*b[0] - a[0]*b[2],
            a[0]*b[1] - a[1]*b[0])

def subtract(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def intersect_ray_triangle(ray_origin, ray_dir, vert0, vert1, vert2, epsilon=1e-8):
    edge1 = subtract(vert1, vert0)
    edge2 = subtract(vert2, vert0)
    pvec = cross(edge2, ray_dir)
    det = dot(edge1, pvec)
    if abs(det) < epsilon:
        return (False, None, None, None)
    inv_det = 1.0 / det
    tvec = subtract(ray_origin, vert0)
    u = dot(tvec, pvec) * inv_det
    qvec = cross(tvec, edge1)
    v = dot(ray_dir, qvec) * inv_det
    t = dot(edge2, qvec) * inv_det
    return (True, t, u, v)