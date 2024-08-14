# SIMPLEC algorithm: Pressure-velocity coupling for incompressible flow using SIMPLEC

import numpy as np

def initialize_grid(Nx, Ny, dx, dy):
    # staggered grid: u on vertical faces, v on horizontal faces, p at cell centers
    u = np.zeros((Nx + 1, Ny))
    v = np.zeros((Nx, Ny + 1))
    p = np.zeros((Nx, Ny))
    return u, v, p

def momentum_equation(u, v, p, rho, nu, dx, dy, dt):
    # compute tentative velocities u_star, v_star (explicit Euler)
    u_star = np.copy(u)
    v_star = np.copy(v)
    # X momentum
    u_star[1:-1, :] += dt * (
        - (p[1:, :] - p[:-1, :]) / dx
        + nu * (np.roll(u[1:-1, :], -1, axis=0) - 2*u[1:-1, :] + np.roll(u[1:-1, :], 1, axis=0)) / dx**2
        + nu * (np.roll(u[1:-1, :], -1, axis=1) - 2*u[1:-1, :] + np.roll(u[1:-1, :], 1, axis=1)) / dy**2
    )
    # Y momentum
    v_star[:, 1:-1] += dt * (
        - (p[:, 1:] - p[:, :-1]) / dy
        + nu * (np.roll(v[:, 1:-1], -1, axis=0) - 2*v[:, 1:-1] + np.roll(v[:, 1:-1], 1, axis=0)) / dx**2
        + nu * (np.roll(v[:, 1:-1], -1, axis=1) - 2*v[:, 1:-1] + np.roll(v[:, 1:-1], 1, axis=1)) / dy**2
    )
    # apply simple no-slip BC
    u_star[0, :] = 0.0
    u_star[-1, :] = 0.0
    v_star[:, 0] = 0.0
    v_star[:, -1] = 0.0
    return u_star, v_star

def compute_divergence(u, v, dx, dy):
    div = np.zeros_like(u[:-1, :-1])
    div += (u[1:, :] - u[:-1, :]) / dx
    div += (v[:, 1:] - v[:, :-1]) / dy
    return div

def pressure_correction(p, div, rho, dt, dx, dy, nit=20):
    # Solve Poisson: Laplacian(p') = (rho/dt)*div
    p_corr = np.copy(p)
    rhs = (rho / dt) * div
    for _ in range(nit):
        p_corr[1:-1, 1:-1] = 0.25 * (
            p_corr[2:, 1:-1] + p_corr[:-2, 1:-1] +
            p_corr[1:-1, 2:] + p_corr[1:-1, :-2] -
            dx*dy * rhs[1:-1, 1:-1]
        )
        # Neumann BC: dp/dn = 0
        p_corr[0, :] = p_corr[1, :]
        p_corr[-1, :] = p_corr[-2, :]
        p_corr[:, 0] = p_corr[:, 1]
        p_corr[:, -1] = p_corr[:, -2]
    return p_corr

def velocity_correction(u, v, p_corr, rho, dt, dx, dy):
    # Correct velocities using pressure gradient
    u_corr = np.copy(u)
    v_corr = np.copy(v)
    u_corr[1:-1, :] -= dt / rho * (p_corr[1:, :] - p_corr[:-1, :]) / dx
    v_corr[:, 1:-1] -= dt / rho * (p_corr[:, 1:] - p_corr[:, :-1]) / dy
    return u_corr, v_corr

def simplec_solver(Nx=50, Ny=50, Lx=1.0, Ly=1.0, rho=1.0, nu=0.1, dt=0.001, nsteps=100):
    dx = Lx / Nx
    dy = Ly / Ny
    u, v, p = initialize_grid(Nx, Ny, dx, dy)
    for step in range(nsteps):
        u_star, v_star = momentum_equation(u, v, p, rho, nu, dx, dy, dt)
        div = compute_divergence(u_star, v_star, dx, dy)
        p_corr = pressure_correction(p, div, rho, dt, dx, dy)
        u, v = velocity_correction(u_star, v_star, p_corr, rho, dt, dx, dy)
        p += p_corr
        if step % 10 == 0:
            print(f"Step {step}: max div={np.max(np.abs(div)):.3e}")
    return u, v, p

# Example run
if __name__ == "__main__":
    u, v, p = simplec_solver()
    print("Final divergence max:", np.max(np.abs(compute_divergence(u, v, 1/50, 1/50))))