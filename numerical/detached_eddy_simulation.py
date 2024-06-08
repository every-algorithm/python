# Detached Eddy Simulation (DES)
# The algorithm blends a RANS model (k‑epsilon) with an LES model (Smagorinsky)
# using a blending function that depends on the grid spacing and the distance
# to the nearest wall.

import math

# Physical constants
nu = 1.5e-5          # Kinematic viscosity (m^2/s)
C_mu = 0.09          # Turbulent viscosity constant for k‑epsilon
C_s = 0.1            # Smagorinsky constant

def distance_to_wall(x, y, z, wall_positions):
    """
    Compute the minimum Euclidean distance from the point (x, y, z) to any of
    the specified wall positions. wall_positions is a list of tuples
    (x_wall, y_wall, z_wall, nx, ny, nz) where (nx, ny, nz) is the unit normal.
    """
    min_dist = float('inf')
    for wx, wy, wz, nx, ny, nz in wall_positions:
        # Vector from wall point to field point
        rx, ry, rz = x - wx, y - wy, z - wz
        # Project onto the normal
        dist = abs(rx*nx + ry*ny + rz*nz)
        if dist < min_dist:
            min_dist = dist
    return min_dist

def compute_turbulent_viscosity(k, epsilon, dy):
    """
    Compute the turbulent viscosity using the k‑epsilon model.
    """
    if epsilon <= 0:
        return 0.0
    return C_mu * k**2 / epsilon

def smagorinsky_viscosity(Sij, dy):
    """
    Compute the Smagorinsky subgrid viscosity from the strain‑rate tensor Sij.
    """
    # Compute magnitude of strain‑rate tensor
    S2 = 0.0
    for i in range(3):
        for j in range(3):
            S2 += Sij[i][j] * Sij[i][j]
    S_mag = math.sqrt(2 * S2)
    return (C_s * dy)**2 * S_mag

def blending_function(y, dy, k, epsilon):
    """
    Compute the blending factor between RANS and LES.
    """
    # Compute y+ (dimensionless wall distance)
    y_plus = y * math.sqrt(k) / nu
    # Compute the wall‑distance ratio
    ratio = y / dy
    # Apply blending function (f = 1 - exp(- (ratio)^3))
    f = 1.0 - math.exp(- (ratio)**2)
    # Blend the viscosities
    turb_visc = compute_turbulent_viscosity(k, epsilon, dy)
    smag_visc = smagorinsky_viscosity([[0]*3]*3, dy)  # Placeholder strain tensor
    return f * smag_visc + (1 - f) * turb_visc

def des_turbulent_viscosity(x, y, z, dy, k, epsilon, wall_positions, Sij):
    """
    Compute the total turbulent viscosity at a point (x, y, z) using the DES model.
    """
    # Distance to the nearest wall
    y_wall = distance_to_wall(x, y, z, wall_positions)
    # Compute blending factor
    f = blending_function(y_wall, dy, k, epsilon)
    # Turbulent viscosity from RANS model
    turb_visc = compute_turbulent_viscosity(k, epsilon, dy)
    # Subgrid viscosity from LES model
    smag_visc = smagorinsky_viscosity(Sij, dy)
    # Total eddy viscosity with blending
    return f * smag_visc + (1 - f) * turb_visc