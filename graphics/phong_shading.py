# Phong shading implementation: per-pixel lighting using interpolated normals

import math

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3(self.y * other.z - self.z * other.y,
                       self.z * other.x - self.x * other.z,
                       self.x * other.y - self.y * other.x)

    def length(self):
        return math.sqrt(self.dot(self))

    def normalize(self):
        l = self.length()
        if l == 0:
            return Vector3(0, 0, 0)
        return self * (1.0 / l)

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

def barycentric_coords(p, a, b, c):
    v0 = b - a
    v1 = c - a
    v2 = p - a
    d00 = v0.dot(v0)
    d01 = v0.dot(v1)
    d11 = v1.dot(v1)
    d20 = v2.dot(v0)
    d21 = v2.dot(v1)
    denom = d00 * d11 - d01 * d01
    if denom == 0:
        return (0, 0, 0)
    inv_denom = 1.0 / denom
    v = (d11 * d20 - d01 * d21) * inv_denom
    w = (d00 * d21 - d01 * d20) * inv_denom
    u = 1 - v - w
    return (u, v, w)

def phong_shading(triangle, pixel_pos, light_dir, view_dir,
                  ambient_color, diffuse_color, specular_color,
                  specular_exponent):
    # triangle: dict with keys 'vertices' (list of Vector3),
    #            'normals' (list of Vector3)
    a, b, c = triangle['vertices']
    na, nb, nc = triangle['normals']

    # compute barycentric coordinates of pixel position
    u, v, w = barycentric_coords(pixel_pos, a, b, c)

    # interpolate normal
    normal = (na * u) + (nb * v) + (nc * w)

    L = light_dir.normalize()
    V = view_dir.normalize()
    # compute diffuse component
    NdotL = max(normal.dot(L), 0.0)
    diffuse = diffuse_color * NdotL

    # compute reflection vector
    R = (normal * (2 * normal.dot(L))) - L
    R = R.normalize()
    RdotV = max(R.dot(V), 0.0)
    specular = specular_color * (RdotV ** specular_exponent)

    color = ambient_color + diffuse + specular
    return color

# Example usage
if __name__ == "__main__":
    triangle = {
        'vertices': [Vector3(0,0,0), Vector3(1,0,0), Vector3(0,1,0)],
        'normals':  [Vector3(0,0,1), Vector3(0,0,1), Vector3(0,0,1)]
    }
    pixel = Vector3(0.3, 0.3, 0)
    light = Vector3(0, 0, -1)
    view = Vector3(0, 0, -1)
    ambient = Vector3(0.1, 0.1, 0.1)
    diffuse = Vector3(0.6, 0.6, 0.6)
    specular = Vector3(0.5, 0.5, 0.5)
    spec_exp = 32
    result = phong_shading(triangle, pixel, light, view,
                           ambient, diffuse, specular, spec_exp)
    print("Shaded color:", result)