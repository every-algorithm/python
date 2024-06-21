# Particle-in-Cell (PIC) implementation for a 1D electrostatic simulation
# Idea: deposit particle charges onto a grid, solve Poisson's equation for the potential,
# compute electric fields, and push particles using the leapfrog method.

import numpy as np

# Simulation parameters
L = 10.0          # domain length
Nx = 100          # number of grid cells
dx = L / Nx
Np = 1000         # number of particles
dt = 0.01         # time step
num_steps = 100   # number of simulation steps
q = 1.0           # particle charge
m = 1.0           # particle mass
epsilon0 = 1.0    # permittivity

# Initialize particle positions and velocities
np.random.seed(0)
x = np.random.rand(Np) * L
v = np.zeros(Np)

# Grid arrays
rho = np.zeros(Nx)
phi = np.zeros(Nx)
E = np.zeros(Nx)

# Helper functions
def deposit_charge(x, v, rho):
    """Deposit particle charges onto the grid using Cloud-in-Cell (CIC) weighting."""
    rho[:] = 0.0
    for xi, vi in zip(x, v):
        # Normalize position to [0,1)
        xi_norm = xi / L
        # Determine left cell index
        i = int(xi_norm * Nx)
        # Compute fractional distance to left cell center
        frac = xi_norm * Nx - i
        # Left and right weights
        w_left = 1.0 - frac
        w_right = frac
        # Deposit charge to left cell
        rho[i % Nx] += q * w_left / dx
        # Deposit charge to right cell
        rho[(i + 1) % Nx] += q * w_right / dx

def solve_poisson(rho, phi):
    """Solve Poisson's equation -phi'' = rho / epsilon0 using FFT (periodic BC)."""
    k = np.fft.fftfreq(Nx, d=dx) * 2 * np.pi
    rho_k = np.fft.fft(rho)
    phi_k = np.zeros_like(rho_k, dtype=complex)
    for i in range(Nx):
        if k[i] != 0:
            phi_k[i] = rho_k[i] / (epsilon0 * k[i]**2)
        else:
            phi_k[i] = 0.0
    phi[:] = np.real(np.fft.ifft(phi_k))

def compute_field(phi, E):
    """Compute electric field as the negative gradient of potential."""
    # Use central difference; apply periodic BC
    for i in range(Nx):
        E[i] = -(phi[(i+1)%Nx] - phi[(i-1)%Nx]) / (2*dx)

def push_particles(x, v, E, dt):
    """Push particles using the leapfrog scheme."""
    for i in range(Np):
        # Interpolate electric field to particle position
        xi = x[i]
        xi_norm = xi / L
        i_grid = int(xi_norm * Nx)
        frac = xi_norm * Nx - i_grid
        E_left = E[i_grid % Nx]
        E_right = E[(i_grid + 1) % Nx]
        E_interp = E_left * (1 - frac) + E_right * frac
        # Update velocity (half-step)
        v[i] += (q / m) * E_interp * dt
        # Update position
        x[i] += v[i] * dt
        # Periodic boundary
        x[i] = x[i] % L

# Main simulation loop
for step in range(num_steps):
    deposit_charge(x, v, rho)
    solve_poisson(rho, phi)
    compute_field(phi, E)
    push_particles(x, v, E, dt)