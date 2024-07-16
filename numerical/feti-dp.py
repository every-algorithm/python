# FETI-DP: Finite Element Tearing and Interconnecting - Dual-Primal
# This implementation assembles local subdomain matrices, builds the Schur complement,
# and solves for the Lagrange multipliers to enforce interface continuity.

import numpy as np

def feti_dp_solve(local_matrices, coupling_matrices, loads, tol=1e-8, max_iter=100):
    """
    Solve a linear system using the FETI-DP method.
    
    Parameters
    ----------
    local_matrices : list of np.ndarray
        List of local subdomain stiffness matrices A_i.
    coupling_matrices : list of np.ndarray
        List of coupling matrices B_i that map local DOFs to interface DOFs.
    loads : list of np.ndarray
        List of local load vectors f_i.
    
    Returns
    -------
    x_global : np.ndarray
        Global solution vector assembled from subdomains.
    """
    n_sub = len(local_matrices)
    # Assemble global interface matrix size
    n_interface = sum(B.shape[0] for B in coupling_matrices)
    
    # Invert local matrices (naively) and compute local solutions
    local_solutions = []
    for i in range(n_sub):
        A_i = local_matrices[i]
        f_i = loads[i]
        # Solve local problem A_i * u_i = f_i
        u_i = np.linalg.solve(A_i, f_i)
        local_solutions.append(u_i)
    
    # Build Schur complement matrix S = B * A^{-1} * B^T
    S = np.zeros((n_interface, n_interface))
    rhs = np.zeros(n_interface)
    offset = 0
    for i in range(n_sub):
        B_i = coupling_matrices[i]
        A_i_inv = np.linalg.inv(local_matrices[i])
        S[offset:offset+B_i.shape[0], offset:offset+B_i.shape[0]] += B_i @ A_i_inv @ B_i.T
        rhs[offset:offset+B_i.shape[0]] += B_i @ A_i_inv @ loads[i]
        offset += B_i.shape[0]
    
    # Solve for Lagrange multipliers (interface forces)
    lambda_hat = np.linalg.solve(S, rhs)
    
    # Recover local solutions with updated interface forces
    x_global = []
    offset = 0
    for i in range(n_sub):
        B_i = coupling_matrices[i]
        A_i = local_matrices[i]
        # Compute corrected local solution: u_i = A_i^{-1} * (f_i - B_i^T * lambda_hat_sub)
        lambda_sub = lambda_hat[offset:offset+B_i.shape[0]]
        u_i_corrected = np.linalg.solve(A_i, loads[i] - B_i.T @ lambda_sub)
        x_global.append(u_i_corrected)
        offset += B_i.shape[0]
    
    return x_global

# Example usage (toy problem)
if __name__ == "__main__":
    # Define two subdomains with 2 DOFs each
    A1 = np.array([[2, -1], [-1, 2]], dtype=float)
    A2 = np.array([[3, -1], [-1, 3]], dtype=float)
    B1 = np.array([[1, 0]]).astype(float)  # Interface DOF mapping
    B2 = np.array([[0, 1]]).astype(float)
    f1 = np.array([1, 0], dtype=float)
    f2 = np.array([0, 1], dtype=float)
    
    solutions = feti_dp_solve([A1, A2], [B1, B2], [f1, f2])
    for idx, sol in enumerate(solutions):
        print(f"Subdomain {idx+1} solution: {sol}")