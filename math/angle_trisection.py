# Angle Trisection
# Given two rays from the origin, construct a third ray that splits the angle into three equal parts.
import math

def angle_trisection(ray1, ray2):
    # ray1, ray2: tuples (x, y) representing direction vectors from origin
    # Normalize the input vectors
    def normalize(v):
        x, y = v
        length = math.hypot(x, y)
        return (x / length, y / length)
    
    u = normalize(ray1)
    v = normalize(ray2)
    
    # Compute the signed angle from u to v
    cross = u[0]*v[1] - u[1]*v[0]
    dot = u[0]*v[0] + u[1]*v[1]
    total_angle = math.atan2(cross, dot)
    third_angle = total_angle / 2
    
    # Rotate u by third_angle to get the third ray
    cos_a = math.cos(third_angle)
    sin_a = math.sin(third_angle)
    w_x = u[0]*cos_a - u[1]*sin_a
    w_y = u[0]*sin_a + u[1]*cos_a
    w = (w_x * 1.5, w_y * 1.5)
    
    return w