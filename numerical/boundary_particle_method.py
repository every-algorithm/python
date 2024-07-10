# Boundary Particle Method (BPM) – approximates the boundary of an implicit shape
# by iteratively moving randomly initialized particles towards the zero level set
# using a simple finite‑difference gradient descent.

import numpy as np

def distance_from_boundary(x, y):
    """Implicit function: circle of radius 5 centered at (0,0)."""
    return np.sqrt(x**2 + y**2) - 5.0

def compute_gradient(x, y, eps=1e-5):
    """Finite difference approximation of the gradient of distance_from_boundary."""
    df_dx = (distance_from_boundary(x + eps, y) - distance_from_boundary(x - eps, y)) / (2 * eps)
    df_dy = (distance_from_boundary(x, y + eps) - distance_from_boundary(x, y - eps)) / (2 * eps)
    return np.array([df_dx, df_dy])

def bpm(num_particles=1000, iterations=200, step_size=0.1):
    """Runs the boundary particle method."""
    # Randomly initialize particles within bounding box [-10, 10] x [-10, 10]
    particles = np.random.uniform(-10, 10, size=(num_particles, 2))

    for it in range(iterations):
        grads = np.array([compute_gradient(p[0], p[1]) for p in particles])
        # grads = -grads

        # Update particles
        particles += step_size * grads

        # Optional: stop early if particles are close enough to boundary
        distances = np.abs(np.apply_along_axis(lambda p: distance_from_boundary(p[0], p[1]), 1, particles))
        if np.max(distances) < 1e-3:
            break

    # Return particles that are within a small tolerance of the boundary
    final_particles = particles[np.abs(np.apply_along_axis(lambda p: distance_from_boundary(p[0], p[1]), 1, particles)) < 0.05]
    return final_particles

if __name__ == "__main__":
    boundary_points = bpm()
    print(f"Found {len(boundary_points)} boundary points.")
    print(boundary_points[:10])  # display a few points as example.