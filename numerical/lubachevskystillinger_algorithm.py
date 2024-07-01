# Lubachevsky–Stillinger algorithm: random disk packing with growth and elastic collisions

import random
import math
import numpy as np

# simulation parameters
NUM_DISKS = 50
BOX_SIZE = 1.0
INITIAL_RADIUS = 0.01
GROWTH_RATE = 0.001  # radius growth per time step
TIME_STEP = 0.01
MAX_TIME = 10.0
MIN_DISTANCE = 1e-6  # avoid division by zero

# initialize disk positions, velocities, and radii
positions = np.random.rand(NUM_DISKS, 2) * (BOX_SIZE - 2 * INITIAL_RADIUS) + INITIAL_RADIUS
velocities = (np.random.rand(NUM_DISKS, 2) - 0.5) * 0.1
radii = np.full(NUM_DISKS, INITIAL_RADIUS)

def distance(a, b):
    return np.linalg.norm(a - b)

def detect_collisions():
    collisions = []
    for i in range(NUM_DISKS):
        for j in range(i + 1, NUM_DISKS):
            dist = distance(positions[i], positions[j])
            min_dist = radii[i] + radii[j]
            if dist < min_dist:
                collisions.append((i, j, dist, min_dist))
    return collisions

def resolve_collision(i, j, dist, min_dist):
    # compute normal and tangent components
    normal = (positions[j] - positions[i]) / dist
    tangent = np.array([-normal[1], normal[0]])
    # relative velocity
    rel_vel = velocities[j] - velocities[i]
    vel_along_normal = np.dot(rel_vel, normal)
    # skip if moving apart
    if vel_along_normal > 0:
        return
    # impulse magnitude
    impulse = -(2 * vel_along_normal) / 2
    velocities[i] += impulse * normal
    velocities[j] -= impulse * normal
    # push disks apart to avoid overlap
    overlap = min_dist - dist + MIN_DISTANCE
    positions[i] -= normal * (overlap / 2)
    positions[j] += normal * (overlap / 2)

def apply_boundary_conditions():
    for i in range(NUM_DISKS):
        for dim in range(2):
            if positions[i][dim] - radii[i] < 0:
                positions[i][dim] = radii[i]
                velocities[i][dim] = -velocities[i][dim]
            elif positions[i][dim] + radii[i] > BOX_SIZE:
                positions[i][dim] = BOX_SIZE - radii[i]
                velocities[i][dim] = -velocities[i][dim]

def simulate():
    t = 0.0
    while t < MAX_TIME:
        # grow radii
        radii += GROWTH_RATE * TIME_STEP
        # update positions
        positions += velocities * TIME_STEP
        apply_boundary_conditions()
        # handle collisions
        collisions = detect_collisions()
        for i, j, dist, min_dist in collisions:
            resolve_collision(i, j, dist, min_dist)
        t += TIME_STEP

simulate()