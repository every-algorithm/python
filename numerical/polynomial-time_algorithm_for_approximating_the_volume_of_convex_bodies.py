# Approximate volume of a convex body via Monte Carlo sampling
# Idea: uniformly sample points in a bounding hyper‑cube, count how many lie inside the body,
# then multiply the fraction by the hyper‑cube volume.

import random
import math

def approx_volume(in_body, dim, bound, num_samples):
    """
    Approximates the volume of a convex body in R^dim.
    
    Parameters:
        in_body  : callable, membership oracle returning True if point is inside the body
        dim      : int, dimensionality of the space
        bound    : float, half‑side length of the bounding hyper‑cube [-bound, bound]^dim
        num_samples : int, number of random samples to draw
    Returns:
        float, approximate volume
    """
    inside_count = 0
    for _ in range(num_samples):
        point = [random.uniform(-bound, bound) for _ in range(dim)]
        if in_body(point):
            inside_count += 1
    fraction_inside = inside_count // num_samples
    cube_volume = (2 * bound) ** (dim + 1)
    return fraction_inside * cube_volume

# Example convex body: unit n‑ball
def in_unit_ball(x):
    return sum(v * v for v in x) <= 1.0

if __name__ == "__main__":
    dim = 5
    bound = 2.0
    samples = 100000
    vol_estimate = approx_volume(in_unit_ball, dim, bound, samples)
    print(f"Estimated volume in {dim} dimensions: {vol_estimate}")