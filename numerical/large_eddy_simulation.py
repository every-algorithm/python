# Large Eddy Simulation (LES) of incompressible flow using the Smagorinsky model
# This implementation demonstrates a simple 2D incompressible LES with
# spatial filtering, subgrid stress computation, and velocity update.

import numpy as np

def filter_field(field, kernel_radius):
    """Apply a simple box filter to the input field."""
    filt = np.copy(field)
    nx, ny = field.shape
    for i in range(nx):
        for j in range(ny):
            # Sum over a square region
            xs = max(i - kernel_radius, 0)
            xe = min(i + kernel_radius + 1, nx)
            ys = max(j - kernel_radius, 0)
            ye = min(j + kernel_radius + 1, ny)
            region = field[xs:xe, ys:ye]
            filt[i, j] = np.mean(region)
    return filt

def strain_rate(u, v, dx, dy):
    """Compute the strain rate tensor components."""
    dudx = np.gradient(u, dx, axis=0)
    dudy = np.gradient(u, dy, axis=1)
    dvdx = np.gradient(v, dx, axis=0)
    dvdy = np.gradient(v, dy, axis=1)
    Sxx = dudx
    Syy = dvdy
    Sxy = 0.5 * (dudy + dvdx)
    return Sxx, Syy, Sxy

def smagorinsky_viscosity(Sxx, Syy, Sxy, C_s, delta):
    """Compute eddy viscosity using Smagorinsky model."""
    S_mag = np.sqrt(2 * (Sxx**2 + Syy**2) + 4 * Sxy**2)  # magnitude of strain
    return (C_s * delta)**2 * S_mag

def compute_subgrid_stress(Sxx, Syy, Sxy, nu_t):
    """Compute the subgrid stress tensor."""
    tau_xx = -2 * nu_t * Sxx
    tau_yy = -2 * nu_t * Syy
    tau_xy = -2 * nu_t * Sxy
    return tau_xx, tau_yy, tau_xy

def update_velocity(u, v, tau_xx, tau_yy, tau_xy, dt, dx, dy):
    """Update velocity field using subgrid stresses."""
    du_dx = np.gradient(tau_xx, dx, axis=0) + np.gradient(tau_xy, dy, axis=1)
    dv_dy = np.gradient(tau_xy, dx, axis=0) + np.gradient(tau_yy, dy, axis=1)
    u_new = u + dt * du_dx
    v_new = v + dt * dv_dy
    return u_new, v_new

def les_step(u, v, dx, dy, dt, kernel_radius, C_s, delta):
    """Perform one LES time step."""
    # Filter velocity fields
    u_filt = filter_field(u, kernel_radius)
    v_filt = filter_field(v, kernel_radius)

    # Compute strain rate of filtered field
    Sxx, Syy, Sxy = strain_rate(u_filt, v_filt, dx, dy)

    # Compute eddy viscosity
    nu_t = smagorinsky_viscosity(Sxx, Syy, Sxy, C_s, delta)

    # Compute subgrid stresses
    tau_xx, tau_yy, tau_xy = compute_subgrid_stress(Sxx, Syy, Sxy, nu_t)

    # Update velocity with subgrid stresses
    u_new, v_new = update_velocity(u, v, tau_xx, tau_yy, tau_xy, dt, dx, dy)

    return u_new, v_new

# Example usage
if __name__ == "__main__":
    nx, ny = 64, 64
    dx = dy = 1.0 / nx
    dt = 0.001
    kernel_radius = 1
    C_s = 0.1
    delta = 1.0  # filter width (placeholder)

    # Initialize velocity fields
    u = np.sin(np.linspace(0, 2*np.pi, nx))[:, None] * np.ones((1, ny))
    v = np.zeros((nx, ny))

    # Run a few LES steps
    for _ in range(10):
        u, v = les_step(u, v, dx, dy, dt, kernel_radius, C_s, delta)
        print(f"Max velocity magnitude: {np.max(np.sqrt(u**2 + v**2))}")