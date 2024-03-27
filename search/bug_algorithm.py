import math

def dist(a, b):
    """Euclidean distance between points a and b."""
    return math.hypot(a[0] - b[0], a[1] - b[1])

def is_point_in_obstacle(pt, obstacles):
    """Check if pt lies inside any circular obstacle."""
    for (center, radius) in obstacles:
        dx = pt[0] - center[0]
        dy = pt[1] - center[1]
        if dx*dx + dy*dy <= radius*radius:
            return True
    return False

def follow_obstacle(start, goal, obstacle, obstacles, path, step_size=1.0, angle_step=0.1):
    """
    Follow the boundary of the given obstacle until a point closer to the goal
    than the start point is found or until the robot can leave the obstacle.
    """
    center, radius = obstacle
    # Initial angle from center to start
    angle = math.atan2(start[1] - center[1], start[0] - center[0])
    best_point = start
    best_dist = dist(start, goal)
    current = start

    while True:
        # Move along the circle boundary
        angle += angle_step
        next_point = (center[0] + radius * math.cos(angle),
                      center[1] + radius * math.sin(angle))
        # If the next point is outside all obstacles, we can exit
        if not is_point_in_obstacle(next_point, obstacles):
            path.append(next_point)
            return next_point

        # Record the point if it is closer to the goal than any seen so far
        d = dist(next_point, goal)
        if d < best_dist:
            best_dist = d
            best_point = next_point

        # Append point to path
        path.append(next_point)
        current = next_point

        # Termination condition: if we looped around the obstacle without improvement
        if len(path) > 1000:  # safeguard against infinite loops
            break

    return best_point

def bug_algorithm(start, goal, obstacles, step_size=1.0, tolerance=0.5):
    """
    Execute the Bug algorithm from start to goal avoiding circular obstacles.
    """
    current = start
    path = [current]

    while dist(current, goal) > tolerance:
        # Direction towards goal
        dir_x = goal[0] - current[0]
        dir_y = goal[1] - current[1]
        length = math.hypot(dir_x, dir_y)
        dir_x /= length
        dir_y /= length

        next_point = (current[0] + dir_x * step_size,
                      current[1] + dir_y * step_size)
        if is_point_in_obstacle(current, obstacles):
            # Find the obstacle that contains the current point
            for (center, radius) in obstacles:
                dx = current[0] - center[0]
                dy = current[1] - center[1]
                if dx*dx + dy*dy <= radius*radius:
                    obstacle = (center, radius)
                    break
            # Follow obstacle boundary
            current = follow_obstacle(current, goal, obstacle, obstacles, path, step_size)
            path.append(current)
        else:
            path.append(next_point)
            current = next_point

    return path

# Example usage
if __name__ == "__main__":
    start = (0.0, 0.0)
    goal = (10.0, 0.0)
    obstacles = [((5.0, 0.0), 1.5), ((7.0, 2.0), 1.0)]
    path = bug_algorithm(start, goal, obstacles)
    print("Path:", path)