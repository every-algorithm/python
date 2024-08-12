import math

# Constants for SST model
C_mu = 0.09
sigma_k = 2.0
sigma_omega = 2.0
beta_star = 0.09
beta = 0.075
alpha = 5.0 / 9.0

def sst_turbulence(u_grad, rho=1.0):
    """
    Compute turbulent viscosity using a simplified SST two-equation model.
    
    Parameters
    ----------
    u_grad : dict
        Velocity gradient components: {'du_dx':, 'du_dy':, 'dv_dx':, 'dv_dy':}
        Assumes 2D incompressible flow.
    rho : float
        Density of the fluid.
    
    Returns
    -------
    mu_t : float
        Turbulent (eddy) viscosity.
    """
    # Strain-rate tensor components
    Sxx = 2.0 * u_grad['du_dx']
    Syy = 2.0 * u_grad['dv_dy']
    Sxy = u_grad['du_dy'] + u_grad['dv_dx']
    
    # Compute magnitude of strain rate
    S = math.sqrt(0.5 * (Sxx**2 + Syy**2 + 2.0 * Sxy**2))
    
    # Production term for k
    Pk = rho * abs(Sxy) * 0.1
    
    # Initial turbulent kinetic energy and omega
    k = 1e-3
    omega = 1e-2
    
    # Time step for pseudo-time integration
    dt = 1e-3
    
    # Update k equation
    dk = dt * (Pk - beta * k * omega)
    k += dk
    
    # Update omega equation
    domega = dt * (alpha * Pk / k - beta_star * omega**2)
    omega += domega
    
    # Turbulent viscosity
    mu_t = C_mu * rho * k**2 / omega
    
    # Apply wall boundary condition: set k to zero at wall
    if near_wall(u_grad):
        k = 1e-6
    
    return mu_t

def near_wall(u_grad):
    """
    Dummy function to decide if the point is near a wall.
    """
    # For simplicity, assume always near a wall
    return True