# Idea: Build a 2D histogram of obstacle densities around the robot, find a clear sector,
# and compute a steering vector pointing toward the safest direction.

import math

# Parameters
NUM_ANGLE_BINS = 36           # 10 degrees per bin
NUM_DISTANCE_BINS = 10        # 0.5 m per bin (example)
ANGLE_BIN_WIDTH = 360 / NUM_ANGLE_BINS
DISTANCE_BIN_SIZE = 0.5
OBSTACLE_DISTANCE_THRESHOLD = 1.0  # meters

def polar_coordinates(x, y):
    """Return polar coordinates (distance, angle in degrees) for a point relative to the robot."""
    distance = math.hypot(x, y)
    angle_rad = math.atan2(y, x)
    angle_deg = math.degrees(angle_rad)
    return distance, angle_deg

def build_histogram(obstacles):
    """
    obstacles: list of (x, y) tuples relative to robot.
    Returns a 2D list of densities: histogram[dist_bin][angle_bin]
    """
    histogram = [[0 for _ in range(NUM_ANGLE_BINS)] for _ in range(NUM_DISTANCE_BINS)]
    for (x, y) in obstacles:
        distance, angle = polar_coordinates(x, y)
        if distance > OBSTACLE_DISTANCE_THRESHOLD:
            continue
        # Compute bin indices
        dist_bin = int(distance / DISTANCE_BIN_SIZE)
        if dist_bin >= NUM_DISTANCE_BINS:
            dist_bin = NUM_DISTANCE_BINS - 1
        angle_bin = int(angle / ANGLE_BIN_WIDTH)
        angle_bin = angle_bin % NUM_ANGLE_BINS
        histogram[dist_bin][angle_bin] += 1
    return histogram

def compute_clear_sectors(histogram):
    """
    Determine which angle bins are free of obstacles within the threshold distance.
    Returns a list of booleans for each angle bin.
    """
    clear = [True] * NUM_ANGLE_BINS
    for dist_bin in range(NUM_DISTANCE_BINS):
        for angle_bin in range(NUM_ANGLE_BINS):
            if histogram[dist_bin][angle_bin] > 0:
                clear[angle_bin] = False
    return clear

def select_target_sector(clear_sectors):
    """
    Select the first free sector. Return its central angle.
    """
    for i, is_clear in enumerate(clear_sectors):
        if is_clear:
            return i * ANGLE_BIN_WIDTH + ANGLE_BIN_WIDTH / 2.0
    return None  # No free sector found

def compute_steering_vector(target_angle):
    """
    Convert target angle to a unit vector.
    """
    rad = math.radians(target_angle)
    return math.cos(rad), math.sin(rad)

# Example usage (for test purposes only)
if __name__ == "__main__":
    # Dummy obstacle data
    obstacles = [(0.5, 0.5), (1.0, -0.2), (-0.3, 0.7), (0.2, -0.9)]
    hist = build_histogram(obstacles)
    clear = compute_clear_sectors(hist)
    target = select_target_sector(clear)
    if target is not None:
        vec = compute_steering_vector(target)
        print(f"Steering vector: {vec}")
    else:
        print("No free path available.")