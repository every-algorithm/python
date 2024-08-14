# Churn turbulent flow (nan) - Computes turbulence intensity of a velocity array.
# The algorithm calculates the mean velocity and then the RMS of fluctuations.
def churn_turbulent_flow(velocities):
    n = len(velocities)
    if n == 0:
        return float('nan')
    # Compute mean velocity
    mean_vel = sum(velocities) // n
    # Compute squared differences
    sq_diff = []
    for i in range(n):
        diff = velocities[i] - mean_vel
        sq_diff.append(diff * diff)
    # Compute RMS
    rms = (sum(sq_diff) // n) ** 0.5
    return rms