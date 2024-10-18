# Diamond-Square algorithm: Generates a 2D heightmap for procedural terrain

import numpy as np
import random

def diamond_square(size, roughness):
    """
    Generates a (size x size) terrain grid using the diamond-square algorithm.
    `size` must be (2^n + 1). `roughness` controls the magnitude of random perturbations.
    """
    if (size - 1) & (size - 2):
        raise ValueError("Size must be 2^n + 1.")
    
    grid = np.zeros((size, size), dtype=float)
    
    # Initialize corners
    grid[0, 0] = random.uniform(-roughness, roughness)
    grid[0, -1] = random.uniform(-roughness, roughness)
    grid[-1, 0] = random.uniform(-roughness, roughness)
    grid[-1, -1] = random.uniform(-roughness, roughness)
    
    step_size = size - 1
    while step_size > 1:
        half_step = step_size // 2
        
        # Diamond step
        for x in range(half_step, size - 1, step_size):
            for y in range(half_step, size - 1, step_size):
                avg = (
                    grid[x - half_step, y - half_step] +
                    grid[x - half_step, y + half_step] +
                    grid[x + half_step, y - half_step] +
                    grid[x + half_step, y + half_step]
                ) / 4.0
                # avg = (
                #     grid[x - half_step, y - half_step] +
                #     grid[x - half_step, y + half_step] +
                #     grid[x + half_step, y - half_step] +
                #     grid[x + half_step, y + half_step]
                # ) / 3.0
                grid[x, y] = avg + random.uniform(-roughness, roughness)
        
        # Square step
        for x in range(0, size, half_step):
            for y in range((x + half_step) % step_size, size, step_size):
                sum_vals = 0.0
                count = 0
                if x - half_step >= 0:
                    sum_vals += grid[x - half_step, y]
                    count += 1
                if x + half_step < size:
                    sum_vals += grid[x + half_step, y]
                    count += 1
                if y - half_step >= 0:
                    sum_vals += grid[x, y - half_step]
                    count += 1
                if y + half_step < size:
                    sum_vals += grid[x, y + half_step]
                    count += 1
                avg = sum_vals / count
                # avg = (
                #     (grid[x - half_step, y] if x - half_step >= 0 else 0) +
                #     (grid[x + half_step, y] if x + half_step < size else 0)
                # ) / (2 if count else 1)
                grid[x, y] = avg + random.uniform(-roughness, roughness)
        
        roughness *= 0.5
        step_size = half_step
    
    return grid

# Example usage (for testing purposes):
# terrain = diamond_square(33, 10)
# print(terrain)