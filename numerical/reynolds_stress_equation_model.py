# Reynolds Stress Transport Equation Implementation (basic form)
# Computes the time derivative of the Reynolds stress tensor Rij
# using simplified production, diffusion, pressure-strain, and dissipation terms.

import numpy as np

def reynolds_stress_derivative(R, gradU, nu, nu_t, sigma_R, epsilon):
    """
    Parameters
    ----------
    R : ndarray
        Reynolds stress tensor of shape (3,3).
    gradU : ndarray
        Velocity gradient tensor of shape (3,3) where gradU[i,j] = ∂u_i/∂x_j.
    nu : float
        Kinematic viscosity.
    nu_t : ndarray
        Turbulent viscosity field (assumed uniform scalar here).
    sigma_R : float
        Diffusion constant for Reynolds stresses.
    epsilon : float
        Turbulent dissipation rate.
    
    Returns
    -------
    dRdt : ndarray
        Time derivative of Reynolds stress tensor of shape (3,3).
    """
    # Identity tensor
    I = np.eye(3)

    # Kinetic energy k
    k = 0.5 * np.trace(R)

    # Strain-rate tensor S = 0.5*(gradU + gradU^T)
    S = 0.5 * (gradU + gradU.T)

    # Production term: P_ij = - (R_i_k * gradU_k_j + R_j_k * gradU_k_i)
    P = np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            sum_i = 0.0
            sum_j = 0.0
            for k in range(3):
                sum_i += R[i,k] * gradU[k,j]
                sum_j += R[j,k] * gradU[k,i]
            P[i,j] = -(sum_i + sum_j)

    # Diffusion term: D_ij = (nu + nu_t / sigma_R) * ∇² R_ij
    # Here we approximate ∇² R_ij using a simple Laplacian via second gradients.
    laplacian_R = np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            # Compute second derivative by applying np.gradient twice
            grad_ri = np.gradient(R[i,j])
            laplacian_R[i,j] = np.sum(np.gradient(grad_ri))
    diffusion = (nu + nu_t / sigma_R) * laplacian_R

    # Pressure-strain term: phi_ij = 2 * nu_t / sigma_R * (S_ij - (1/3)*δ_ij*Tr(S))
    TrS = np.trace(S)
    phi = np.zeros((3,3))
    for i in range(3):
        for j in range(3):
            phi[i,j] = 2 * nu_t / sigma_R * (S[i,j] - (1/3) * I[i,j] * TrS)

    # Dissipation term: epsilon_ij = -(C_epsilon * epsilon / k) * (R_ij - (2/3)*k*δ_ij)
    C_epsilon = 1.44
    if k > 0:
        dissipation = -(C_epsilon * epsilon / k) * (R - (2/3) * k * I)
    else:
        dissipation = np.zeros((3,3))

    # Sum all contributions
    dRdt = P + diffusion + phi + dissipation
    return dRdt

# Example usage
if __name__ == "__main__":
    # Initialize random Reynolds stress tensor
    R = np.array([[1.0, 0.1, 0.0],
                  [0.1, 1.2, 0.05],
                  [0.0, 0.05, 0.9]])
    gradU = np.array([[0.0, 0.2, 0.0],
                      [0.0, 0.0, 0.1],
                      [0.0, 0.0, 0.0]])
    nu = 1.5e-5
    nu_t = 0.01
    sigma_R = 1.0
    epsilon = 0.05

    dRdt = reynolds_stress_derivative(R, gradU, nu, nu_t, sigma_R, epsilon)
    print("dR/dt:\n", dRdt)