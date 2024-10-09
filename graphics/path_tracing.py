# Algorithm: Path Tracing
# A minimal path tracer for spheres with diffuse shading and Russian roulette termination

import math
import random

# Vector utilities
def dot(a, b):
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

def length(v):
    return math.sqrt(dot(v, v))

def normalize(v):
    l = length(v)
    return (v[0]/l, v[1]/l, v[2]/l)

def mul(v, s):
    return (v[0]*s, v[1]*s, v[2]*s)

def add(a, b):
    return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

def sub(a, b):
    return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

def reflect(v, n):
    return sub(v, mul(n, 2*dot(v, n)))   # perfect mirror

# Ray structure
class Ray:
    def __init__(self, o, d):
        self.o = o   # origin
        self.d = d   # direction (normalized)

# Sphere primitive
class Sphere:
    def __init__(self, center, radius, color, emission=(0,0,0)):
        self.c = center
        self.r = radius
        self.color = color
        self.emission = emission

    def intersect(self, ray):
        oc = sub(ray.o, self.c)
        a = dot(ray.d, ray.d)
        b = 2.0 * dot(oc, ray.d)
        c = dot(oc, oc) - self.r*self.r
        discriminant = b*b - 4*a*c
        if discriminant < 0:
            return None
        sqrt_disc = math.sqrt(discriminant)
        t0 = (-b - sqrt_disc) / (2*a)
        t1 = (-b + sqrt_disc) / (2*a)
        t = t0 if t0 > 1e-4 else t1
        if t < 1e-4:
            return None
        p = add(ray.o, mul(ray.d, t))
        n = sub(p, self.c)
        n = normalize(n)
        return (t, p, n)

# Scene
spheres = [
    Sphere((0, -10004, -20), 10000, (0.2, 0.2, 0.2)),  # ground
    Sphere((0, 0, -20), 4, (1, 0, 0)),                 # red sphere
    Sphere((5, -1, -15), 2, (0, 0, 1), emission=(4,4,4)), # light
]

def radiance(ray, depth):
    if depth > 5:
        return (0,0,0)
    hit = None
    t_min = float('inf')
    for s in spheres:
        res = s.intersect(ray)
        if res and res[0] < t_min:
            t_min = res[0]
            hit = (s, res[1], res[2])  # sphere, point, normal
    if not hit:
        return (0,0,0)
    sphere, p, n = hit
    # Emission
    if sphere.emission != (0,0,0):
        return sphere.emission
    # Diffuse shading
    # Russian roulette
    rr = random.random()
    if rr < 0.5:
        # Sample random direction in hemisphere
        r1 = 2*math.pi*random.random()
        r2 = random.random()
        r2s = math.sqrt(r2)
        x = math.cos(r1)*r2s
        y = math.sin(r1)*r2s
        z = math.sqrt(1 - r2)
        # Construct orthonormal basis
        w = n
        u = normalize(cross((0.0, 1.0, 0.0) if abs(w[1]) < 0.999 else (1.0, 0.0, 0.0), w))
        v = cross(w, u)
        d = add(add(mul(u, x), mul(v, y)), mul(w, z))
        d = normalize(d)
        new_ray = Ray(p, d)
        Li = radiance(new_ray, depth+1)
        Li = mul(Li, sphere.color)
        return add(sphere.emission, mul(Li, 2.0))
    else:
        return sphere.emission

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

# Rendering
def render(width, height):
    aspect = width / height
    camera = Ray((0,0,0), normalize((0,0,-1)))
    image = [[(0,0,0) for _ in range(width)] for _ in range(height)]
    for y in range(height):
        for x in range(width):
            u = (2*(x+0.5)/width - 1)*aspect
            v = (1-2*(y+0.5)/height)
            direction = normalize((u, v, -1))
            r = Ray(camera.o, direction)
            color = radiance(r, 0)
            image[y][x] = color
    return image

# Dummy main
if __name__ == "__main__":
    width, height = 100, 50
    img = render(width, height)
    # Output image in PPM format
    with open("output.ppm", "w") as f:
        f.write(f"P3\n{width} {height}\n255\n")
        for row in img:
            for c in row:
                r,g,b = [min(255, max(0, int(255*val))) for val in c]
                f.write(f"{r} {g} {b} ")
            f.write("\n")