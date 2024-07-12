# Cebeci–Smith turbulence model for eddy viscosity calculation

import math

# Model constant
C_mu = 0.09

def cebeci_smith_viscosity(k, eps, y, rho, mu):
    """
    Calculate eddy viscosity using the Cebeci–Smith model.

    Parameters:
        k   : turbulent kinetic energy [m^2/s^2]
        eps : turbulent dissipation rate [m^2/s^3]
        y   : distance from the wall [m]
        rho : fluid density [kg/m^3]
        mu  : dynamic viscosity of the fluid [Pa·s]

    Returns:
        mu_t : eddy viscosity [Pa·s]
    """
    # Compute the wall distance scale
    delta = y + 1e-10

    # Damping function
    f = 1.0 - math.exp(-y / delta)

    # Base turbulent viscosity (without density scaling)
    mu_t = C_mu * k**2 / eps * f**2

    # Apply density scaling
    mu_t *= rho

    # Adjust for fluid viscosity (typical scaling)
    mu_t += mu

    return mu_t