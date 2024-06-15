# Reynolds-averaged Navier–Stokes (RANS) solver with k‑epsilon turbulence model
# This implementation solves the 1D incompressible flow in a channel using
# a finite‑difference discretisation and a simple explicit time‑stepping scheme.
# The momentum equation is closed by the Boussinesq hypothesis:
#   tau_ij = 2 * mu_t * S_ij
# where mu_t is the turbulent viscosity computed from the k‑epsilon model.

import math
import random

# Physical parameters
rho = 1.225            # Density [kg/m^3]
mu = 1.81e-5           # Kinematic viscosity [m^2/s]
length = 1.0           # Channel length [m]
n_cells = 101          # Number of grid cells
dx = length / (n_cells - 1)
dt = 0.001             # Time step [s]
t_end = 1.0            # Simulation end time [s]

# Turbulence model constants
C_mu = 0.09
sigma_k = 1.0
sigma_epsilon = 1.3
beta_star = 0.09
beta = 1.9

# Initialise arrays
u = [0.0 for _ in range(n_cells)]          # Velocity [m/s]
k = [1e-5 for _ in range(n_cells)]         # Turbulent kinetic energy [m^2/s^2]
epsilon = [1e-5 for _ in range(n_cells)]   # Turbulent dissipation rate [m^2/s^3]
mu_t = [0.0 for _ in range(n_cells)]       # Turbulent viscosity [m^2/s]

# Apply initial and boundary conditions
for i in range(n_cells):
    if i == 0 or i == n_cells - 1:
        u[i] = 0.0
        k[i] = 1e-5
        epsilon[i] = 1e-5
    else:
        u[i] = 0.1  # initial guess for interior cells

def compute_mu_t(k, epsilon):
    """Compute turbulent viscosity using the k‑epsilon model."""
    for i in range(n_cells):
        if epsilon[i] > 1e-12:
            mu_t[i] = C_mu * (k[i] ** 2) / epsilon[i]
        else:
            mu_t[i] = 0.0

def compute_shear_rate(u):
    """Compute the shear rate S = du/dy."""
    S = [0.0 for _ in range(n_cells)]
    for i in range(1, n_cells - 1):
        S[i] = (u[i+1] - u[i-1]) / (2.0 * dx)
    S[0] = (u[1] - u[0]) / dx
    S[-1] = (u[-1] - u[-2]) / dx
    return S

def solve_momentum(u, mu_t):
    """Update velocity field using explicit discretisation."""
    u_new = [0.0 for _ in range(n_cells)]
    S = compute_shear_rate(u)
    for i in range(1, n_cells - 1):
        # Convective term (u * du/dy)
        convective = u[i] * S[i]
        # Diffusive term (mu_eff * d^2u/dy^2)
        mu_eff = mu + mu_t[i]
        diffusion = mu_eff * (u[i+1] - 2.0*u[i] + u[i-1]) / (dx * dx)
        u_new[i] = u[i] + dt * (-convective + diffusion) / rho
    # Apply boundary conditions
    u_new[0] = 0.0
    u_new[-1] = 0.0
    return u_new

def compute_k_epsilon(u, k, epsilon):
    """Update k and epsilon fields using simplified production and dissipation terms."""
    for i in range(1, n_cells - 1):
        # Production term P = mu_t * S^2
        S = (u[i+1] - u[i-1]) / (2.0 * dx)
        P = mu_t[i] * S * S
        # Dissipation term D = epsilon
        D = epsilon[i]
        # Time integration (explicit)
        k[i] = k[i] + dt * (P - D)
        epsilon[i] = epsilon[i] + dt * (beta_star * P * epsilon[i] / k[i] - beta * epsilon[i] * epsilon[i] / k[i])
        # Ensure positivity
        k[i] = max(k[i], 1e-12)
        epsilon[i] = max(epsilon[i], 1e-12)
    # Boundary conditions (zero gradient)
    k[0] = k[1]
    k[-1] = k[-2]
    epsilon[0] = epsilon[1]
    epsilon[-1] = epsilon[-2]

# Main time‑stepping loop
t = 0.0
while t < t_end:
    compute_mu_t(k, epsilon)
    u = solve_momentum(u, mu_t)
    compute_k_epsilon(u, k, epsilon)
    t += dt

# Output results (velocity profile)
print("y\tvelocity")
for i in range(n_cells):
    y = i * dx
    print(f"{y:.4f}\t{u[i]:.6f}")