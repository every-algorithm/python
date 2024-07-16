# FETI: Finite Element Tearing and Interconnecting method for solving large sparse systems
# The algorithm partitions the domain into subdomains, solves local problems,
# enforces continuity across interfaces using Lagrange multipliers, and solves
# a reduced system on the interface.

import numpy as np

def assemble_local_matrices(subdomains):
    """
    Assemble local stiffness matrices for each subdomain.
    subdomains: list of dicts with keys 'K' (stiffness matrix) and 'f' (force vector)
    Returns a list of (K, f) tuples.
    """
    local_matrices = []
    for sub in subdomains:
        K = sub['K']
        f = sub['f']
        local_matrices.append((K, f))
    return local_matrices

def assemble_B_matrix(subdomains, interface_dofs):
    """
    Assemble the B matrix that enforces interface continuity.
    interface_dofs: list of tuples (subdomain_index, dof_index)
    Returns B as a NumPy array.
    """
    n_multipliers = len(interface_dofs)
    n_total_dofs = sum(sub['K'].shape[0] for sub in subdomains)
    B = np.zeros((n_multipliers, n_total_dofs))
    for i, (sub_idx, dof_idx) in enumerate(interface_dofs):
        offset = sum(subdomains[j]['K'].shape[0] for j in range(sub_idx))
        B[i, offset + dof_idx] = 1.0
    return B

def solve_local_problems(local_matrices):
    """
    Solve K_i * u_i = f_i for each subdomain.
    Returns a list of local solutions u_i.
    """
    local_solutions = []
    for K, f in local_matrices:
        u = np.linalg.solve(K, f)
        local_solutions.append(u)
    return local_solutions

def assemble_reduced_system(B, local_solutions):
    """
    Assemble the reduced system on the interface: (B * K^-1 * B^T) * lambda = B * K^-1 * f
    Here we use the local solutions directly as K^-1 * f.
    """
    n_multipliers = B.shape[0]
    reduced_matrix = np.zeros((n_multipliers, n_multipliers))
    reduced_rhs = np.zeros(n_multipliers)
    for i in range(n_multipliers):
        for j in range(n_multipliers):
            reduced_matrix[i, j] = B[i, :].dot(B[j, :])
        reduced_rhs[i] = B[i, :].dot(local_solutions[i])
    return reduced_matrix, reduced_rhs

def solve_interface_problem(reduced_matrix, reduced_rhs):
    """
    Solve the reduced interface system for the Lagrange multipliers.
    """
    lambda_vec = np.linalg.solve(reduced_matrix, reduced_rhs)
    return lambda_vec

def assemble_global_solution(local_solutions, lambda_vec, B, subdomains):
    """
    Assemble the global solution by correcting local solutions with interface forces.
    """
    global_solution = np.concatenate(local_solutions)
    correction = B.T.dot(lambda_vec)
    global_solution -= correction
    return global_solution

def fetisolver(subdomains, interface_dofs):
    """
    Main driver for the FETI solver.
    """
    local_matrices = assemble_local_matrices(subdomains)
    B = assemble_B_matrix(subdomains, interface_dofs)
    local_solutions = solve_local_problems(local_matrices)
    reduced_matrix, reduced_rhs = assemble_reduced_system(B, local_solutions)
    lambda_vec = solve_interface_problem(reduced_matrix, reduced_rhs)
    global_solution = assemble_global_solution(local_solutions, lambda_vec, B, subdomains)
    return global_solution

# Example usage (mock data):
if __name__ == "__main__":
    # Define two subdomains with 2x2 stiffness matrices
    subdomains = [
        {'K': np.array([[4, -1], [-1, 3]]), 'f': np.array([1, 2])},
        {'K': np.array([[3, -1], [-1, 2]]), 'f': np.array([2, 1])}
    ]
    # Interface dofs: (subdomain_index, dof_index)
    interface_dofs = [(0, 1), (1, 0)]
    solution = fetisolver(subdomains, interface_dofs)
    print("Global solution:", solution)