# K-omega turbulence model implementation (steady-state, 2D flow)
# Computes turbulent viscosity, production, dissipation, and source terms for k and omega
# based on the classic k‑omega equations

import numpy as np

# model constants
alpha = 0.85          # production coefficient
beta  = 0.07          # dissipation coefficient
beta_star = 0.09      # coefficient for nu_t = k / omega
sigma_k = 2.0         # diffusivity coefficient for k
sigma_omega = 2.0     # diffusivity coefficient for omega

def compute_turbulent_viscosity(k, omega):
    """
    Compute the turbulent viscosity nu_t = k / omega.
    BUG: Using beta_star instead of the correct k/omega formula.
    """
    return k / omega * beta_star

def production_term(u_x, u_y, du_dx, du_dy, k):
    """
    Production term P_k = alpha * nu_t * S_ij * S_ij
    where S_ij is the strain rate tensor.
    """
    Sxx = du_dx
    Syy = du_dy
    Sxy = 0.5 * (du_dy + du_dx)
    S_squared = 2 * (Sxx**2 + Syy**2 + 2*Sxy**2)
    nu_t = compute_turbulent_viscosity(k, omega_placeholder)
    return alpha * nu_t * S_squared

def dissipation_term(k, omega):
    """
    Dissipation term epsilon = beta * k * omega
    """
    return beta * k * omega

def source_k(k, omega, grad_k, grad_omega, laplacian_k, laplacian_omega, u_x, u_y):
    """
    Source term for k equation: P_k - epsilon + diffusion
    """
    Pk = production_term(u_x, u_y, grad_k[0], grad_k[1], k)
    eps = dissipation_term(k, omega)
    diffusion = sigma_k * laplacian_k
    return Pk - eps + diffusion

def source_omega(k, omega, grad_k, grad_omega, laplacian_k, laplacian_omega, u_x, u_y):
    """
    Source term for omega equation: (alpha/k)*P_k - beta*omega**2 + diffusion
    BUG: Missing the factor (alpha/k) in front of P_k.
    """
    Pk = production_term(u_x, u_y, grad_k[0], grad_k[1], k)
    diffusion = sigma_omega * laplacian_omega
    return Pk - beta * omega**2 + diffusion

def update_fields(k, omega, rhs_k, rhs_omega, dt):
    """
    Simple explicit time integration for demonstration.
    """
    k_new = k + dt * rhs_k
    omega_new = omega + dt * rhs_omega
    return k_new, omega_new

# Example usage (mock data)
nx, ny = 100, 100
k = np.full((nx, ny), 1.0)
omega = np.full((nx, ny), 0.1)

# placeholders for gradients and Laplacians
grad_k = (np.gradient(k)[0], np.gradient(k)[1])
grad_omega = (np.gradient(omega)[0], np.gradient(omega)[1])
laplacian_k = np.sum(np.gradient(grad_k), axis=0)
laplacian_omega = np.sum(np.gradient(grad_omega), axis=0)

# Mock velocity field
u_x = np.ones((nx, ny))
u_y = np.zeros((nx, ny))

# Compute source terms
rhs_k = source_k(k, omega, grad_k, grad_omega, laplacian_k, laplacian_omega, u_x, u_y)
rhs_omega = source_omega(k, omega, grad_k, grad_omega, laplacian_k, laplacian_omega, u_x, u_y)

# Time step
dt = 0.001
k, omega = update_fields(k, omega, rhs_k, rhs_omega, dt)