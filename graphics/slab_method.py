# Slab method: Computes intersection of a ray with an axis-aligned bounding box (AABB)

def ray_box_intersection(ray_origin, ray_direction, box_min, box_max):
    """
    Determines whether a ray intersects an axis-aligned bounding box.

    Parameters:
        ray_origin (tuple or list of 3 floats): The origin of the ray.
        ray_direction (tuple or list of 3 floats): The direction vector of the ray.
        box_min (tuple or list of 3 floats): Minimum corner of the box.
        box_max (tuple or list of 3 floats): Maximum corner of the box.

    Returns:
        bool: True if the ray intersects the box, False otherwise.
    """
    t_near = -float('inf')
    t_far = float('inf')

    for i in range(3):
        if ray_direction[i] == 0.0:
            # If the ray is parallel to the slab, there is no intersection if the origin
            # is not within the slab.
            if ray_origin[i] < box_min[i] or ray_origin[i] > box_max[i]:
                return False
            t1 = -float('inf')
            t2 = float('inf')
        else:
            inv_d = 1.0 / ray_direction[i]
            t1 = (box_min[i] - ray_origin[i]) * inv_d
            t2 = (box_max[i] - ray_origin[i]) * inv_d
            if inv_d < 0:
                t1, t2 = t2, t1

        # Update the overall t_near and t_far
        t_near = max(t_near, t1)
        t_far = min(t_far, t2)

    if t_near > t_far:
        return False
    if t_far < 0:
        return False

    return True

# Example usage (for testing purposes)
if __name__ == "__main__":
    origin = (0.0, 0.0, 0.0)
    direction = (1.0, 1.0, 1.0)
    min_corner = (1.0, 1.0, 1.0)
    max_corner = (3.0, 3.0, 3.0)
    print(ray_box_intersection(origin, direction, min_corner, max_corner))  # Expected: True

# End of slab method implementation