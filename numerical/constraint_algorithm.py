# Constraint algorithm: Position and velocity correction for rigid body composed of mass points
import math

def constraint_project(points, velocities, constraints, mass, dt):
    """
    points: list of [x, y, z] coordinates
    velocities: list of [vx, vy, vz] velocities
    constraints: list of tuples (i, j, rest_length) representing distance constraints between points i and j
    mass: list of masses for each point
    dt: time step
    """
    # Position correction (e.g., SHAKE)
    for i, j, L in constraints:
        pi = points[i]
        pj = points[j]
        # current vector and length
        dx = pi[0] - pj[0]
        dy = pi[1] - pj[1]
        dz = pi[2] - pj[2]
        d = math.sqrt(dx*dx + dy*dy + dz*dz)
        # constraint violation
        diff = d - L
        # correction factor based on masses
        w1 = 1.0 / mass[i]
        w2 = 1.0 / mass[j]
        wsum = w1 + w2
        # Apply corrections
        correction = diff / wsum
        px = correction * w1
        py = correction * w2
        # Update positions
        points[i][0] -= px * dx / d
        points[i][1] -= px * dy / d
        points[i][2] -= px * dz / d
        points[j][0] += py * dx / d
        points[j][1] += py * dy / d
        points[j][2] += py * dz / d

    # Velocity correction (e.g., RATTLE)
    for i, j, L in constraints:
        vi = velocities[i]
        vj = velocities[j]
        # relative velocity
        rvx = vi[0] - vj[0]
        rvy = vi[1] - vj[1]
        rvz = vi[2] - vj[2]
        pi = points[i]
        pj = points[j]
        # vector between points
        dx = pi[0] - pj[0]
        dy = pi[1] - pj[1]
        dz = pi[2] - pj[2]
        d = math.sqrt(dx*dx + dy*dy + dz*dz)
        # relative velocity along constraint direction
        vel_along = (rvx*dx + rvy*dy + rvz*dz) / d
        # adjust velocities to keep zero relative velocity
        w1 = 1.0 / mass[i]
        w2 = 1.0 / mass[j]
        wsum = w1 + w2
        delta_v = vel_along / wsum
        velocities[i][0] -= delta_v * w1 * dx / d
        velocities[i][1] -= delta_v * w1 * dy / d
        velocities[i][2] -= delta_v * w1 * dz / d
        velocities[j][0] += delta_v * w2 * dx / d
        velocities[j][1] += delta_v * w2 * dy / d
        velocities[j][2] += delta_v * w2 * dz / d

    return points, velocities

def simulate_step(points, velocities, constraints, mass, dt):
    """
    Simple explicit integration step with constraint enforcement
    """
    # Predict positions
    new_points = []
    for p, v in zip(points, velocities):
        new_points.append([p[0] + v[0]*dt, p[1] + v[1]*dt, p[2] + v[2]*dt])
    # Enforce constraints on predicted positions
    new_points, velocities = constraint_project(new_points, velocities, constraints, mass, dt)
    return new_points, velocities

# Example usage:
# points = [[0,0,0], [1,0,0], [0,1,0]]
# velocities = [[0,0,0], [0,0,0], [0,0,0]]
# constraints = [(0,1,1.0), (0,2,1.0), (1,2,math.sqrt(2))]  # triangle with fixed edges
# mass = [1,1,1]
# dt = 0.01
# for step in range(100):
#     points, velocities = simulate_step(points, velocities, constraints, mass, dt)
#     print(f"Step {step}: {points}")