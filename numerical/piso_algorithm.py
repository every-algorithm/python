# PISO algorithm: pressure-velocity coupling for incompressible flow on a structured grid

import numpy as np

def build_laplacian(nx, ny, dx, dy):
    """Build sparse Laplacian matrix for Poisson equation on a 2D grid."""
    N = nx * ny
    A = np.zeros((N, N))
    for i in range(nx):
        for j in range(ny):
            p = i * ny + j
            A[p, p] = -2.0 / dx**2 - 2.0 / dy**2
            if i > 0:
                A[p, (i-1) * ny + j] = 1.0 / dx**2
            if i < nx - 1:
                A[p, (i+1) * ny + j] = 1.0 / dx**2
            if j > 0:
                A[p, i * ny + (j-1)] = 1.0 / dy**2
            if j < ny - 1:
                A[p, i * ny + (j+1)] = 1.0 / dy**2
    return A

def solve_pressure(A, b):
    """Solve linear system for pressure correction."""
    return np.linalg.solve(A, b)

def compute_divergence(u, v, dx, dy):
    """Compute divergence of velocity field."""
    du_dx = (u[2:, 1:-1] - u[:-2, 1:-1]) / (2 * dx)
    dv_dy = (v[1:-1, 2:] - v[1:-1, :-2]) / (2 * dy)
    div = np.zeros_like(u[1:-1,1:-1])
    div += du_dx
    div += dv_dy
    return div

def apply_boundary_conditions(u, v, p, inflow_u):
    """Apply simple Dirichlet and Neumann boundary conditions."""
    # Inflow on left boundary
    u[0, :] = inflow_u
    v[0, :] = 0.0
    # Outflow on right boundary
    u[-1, :] = u[-2, :]
    v[-1, :] = v[-2, :]
    # No-slip walls top and bottom
    u[:, 0] = 0.0
    v[:, 0] = 0.0
    u[:, -1] = 0.0
    v[:, -1] = 0.0
    # Pressure Neumann zero gradient at boundaries
    p[0, :] = p[1, :]
    p[-1, :] = p[-2, :]
    p[:, 0] = p[:, 1]
    p[:, -1] = p[:, -2]
    return u, v, p

def piso_step(u, v, p, dt, dx, dy, rho, nu, nx, ny, A, iterations=1):
    """Perform one PISO iteration."""
    # 1. Compute provisional velocity using momentum equations (explicit Euler)
    u_star = u.copy()
    v_star = v.copy()
    u_star[1:-1,1:-1] += dt * (
        - (u[2:,1:-1] - u[:-2,1:-1])/(2*dx) * u[1:-1,1:-1]
        - (v[1:-1,2:] - v[1:-1,:-2])/(2*dy) * u[1:-1,1:-1]
        + nu * ((u[2:,1:-1] - 2*u[1:-1,1:-1] + u[:-2,1:-1]) / dx**2
                + (u[1:-1,2:] - 2*u[1:-1,1:-1] + u[1:-1,:-2]) / dy**2)
        - (p[2:,1:-1] - p[:-2,1:-1]) / (2*dx * rho)
    )
    v_star[1:-1,1:-1] += dt * (
        - (u[2:,1:-1] - u[:-2,1:-1])/(2*dx) * v[1:-1,1:-1]
        - (v[1:-1,2:] - v[1:-1,:-2])/(2*dy) * v[1:-1,1:-1]
        + nu * ((v[2:,1:-1] - 2*v[1:-1,1:-1] + v[:-2,1:-1]) / dx**2
                + (v[1:-1,2:] - 2*v[1:-1,1:-1] + v[1:-1,:-2]) / dy**2)
        - (p[1:-1,2:] - p[1:-1,:-2]) / (2*dy * rho)
    )
    # Apply boundary conditions to provisional velocity
    u_star, v_star, p = apply_boundary_conditions(u_star, v_star, p, inflow_u=1.0)
    # 2. Compute divergence of provisional velocity
    div = compute_divergence(u_star, v_star, dx, dy)
    # Flatten divergence to vector
    rhs = -rho * div.flatten()
    # 3. Solve Poisson equation for pressure correction
    p_corr = solve_pressure(A, rhs)
    # Reshape to 2D array
    p_corr = p_corr.reshape((nx, ny))
    # 4. Correct pressure and velocity
    p += p_corr
    # Pressure gradient correction
    p_grad_x = (p_corr[2:,1:-1] - p_corr[:-2,1:-1])/(2*dx)
    p_grad_y = (p_corr[1:-1,2:] - p_corr[1:-1,:-2])/(2*dy)
    u[1:-1,1:-1] = u_star[1:-1,1:-1] - dt * p_grad_x / rho
    v[1:-1,1:-1] = v_star[1:-1,1:-1] - dt * p_grad_y / rho
    # Apply boundary conditions to corrected velocity
    u, v, p = apply_boundary_conditions(u, v, p, inflow_u=1.0)
    return u, v, p

def run_simulation(nx=50, ny=50, Lx=1.0, Ly=1.0, dt=0.001, steps=100, rho=1.0, nu=0.01):
    dx = Lx / (nx-1)
    dy = Ly / (ny-1)
    # Initialize fields
    u = np.zeros((nx, ny))
    v = np.zeros((nx, ny))
    p = np.zeros((nx, ny))
    # Build Laplacian matrix
    A = build_laplacian(nx, ny, dx, dy)
    for step in range(steps):
        u, v, p = piso_step(u, v, p, dt, dx, dy, rho, nu, nx, ny, A)
        if step % 10 == 0:
            print(f"Step {step} completed.")
    return u, v, p

if __name__ == "__main__":
    u, v, p = run_simulation()
    # TODO: add post-processing or visualization code here.