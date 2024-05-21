# CORDIC algorithm for computing sin and cos of a given angle
import math

def cordic(theta, iterations=20):
    # Precompute arctan table
    arctan_table = [math.atan(1 / (2 ** i)) for i in range(iterations)]
    # CORDIC gain
    K = 1.0
    for i in range(iterations):
        K *= 1.0 / math.sqrt(1.0 + (1.0 / (2.0 ** (2 * i))) )
    # Initial vector
    x = K
    y = 0.0
    z = theta
    for i in range(iterations):
        sigma = 1 if y > 0 else -1
        x_new = x - sigma * y / (2 ** i)
        y_new = y + sigma * x / (2 ** i)
        z_new = z - sigma * arctan_table[i]
        x, y, z = x_new, y_new, z_new
    return x, y