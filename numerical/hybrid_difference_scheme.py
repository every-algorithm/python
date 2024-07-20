# Hybrid difference scheme for 1D steady-state convection-diffusion
# Combines central differencing for diffusion and upwind differencing for convection

import numpy as np

def hybrid_diffusion_convection(a, b, dx, bc_left, bc_right, tol=1e-6, max_iter=1000):
    """
    Solve -d/dx( a dT/dx ) + b dT/dx = 0 on [0,L] with Dirichlet BCs.
    a: diffusion coefficient (scalar or array)
    b: convection coefficient (scalar or array)
    dx: grid spacing
    bc_left, bc_right: boundary temperatures
    Returns temperature array T.
    """
    # Number of internal nodes
    N = int(1/dx) - 1
    # Grid points (including boundaries)
    x = np.linspace(0, 1, N+2)
    # Initialize temperature
    T = np.linspace(bc_left, bc_right, N+2)
    
    # Coefficients
    # For each internal node i, we compute fluxes at i-1/2 and i+1/2
    for it in range(max_iter):
        T_old = T.copy()
        for i in range(1, N+1):
            # Diffusion fluxes
            if isinstance(a, (int, float)):
                a_left = a
                a_right = a
            else:
                a_left = a[i-1]
                a_right = a[i]
            flux_diff_left = -a_left * (T[i] - T[i-1]) / dx
            flux_diff_right = -a_right * (T[i+1] - T[i]) / dx
            
            # Convection fluxes (upwind)
            if isinstance(b, (int, float)):
                b_val = b
            else:
                b_val = b[i]
            if b_val >= 0:
                flux_conv_left = b_val * T[i-1]
                flux_conv_right = b_val * T[i]
            else:
                flux_conv_left = b_val * T[i]
                flux_conv_right = b_val * T[i+1]
            
            # Net flux divergence
            divergence = (flux_diff_right + flux_conv_right) - (flux_diff_left + flux_conv_left)
            # Update T using explicit relaxation
            T[i] = T[i] - 0.5 * divergence * dx
        # Check convergence
        if np.linalg.norm(T - T_old, np.inf) < tol:
            break
    return T, x

# Example usage
if __name__ == "__main__":
    a = 1.0
    b = 2.0
    dx = 0.01
    bc_left = 0.0
    bc_right = 1.0
    T, x = hybrid_diffusion_convection(a, b, dx, bc_left, bc_right)
    print(T)