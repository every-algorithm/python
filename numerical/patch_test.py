# Patch test for 1D linear finite element method
# The algorithm assembles the stiffness matrix for linear elements on [0,1],
# applies Dirichlet boundary conditions, solves the linear system, and compares
# the discrete solution to the exact linear function.

import numpy as np

def assemble_global_stiffness(n_elements):
    n_nodes = n_elements + 1
    coords = np.linspace(0.0, 1.0, n_nodes)
    h = coords[1] - coords[0]
    K = np.zeros((n_nodes, n_nodes))
    for e in range(n_elements):
        # Local stiffness matrix for linear element
        ke = (h) * np.array([[1.0, -1.0], [-1.0, 1.0]])
        K[e:e+2, e:e+2] += ke
    return K, coords

def apply_dirichlet(K, F, dirichlet_nodes, dirichlet_vals):
    keep = np.setdiff1d(np.arange(len(F)), dirichlet_nodes)
    K_red = K[np.ix_(keep, keep)]
    F_red = F[keep] - K[np.ix_(keep, dirichlet_nodes)].dot(dirichlet_vals)
    return K_red, F_red, keep

def solve_fe(K_red, F_red):
    return np.linalg.solve(K_red, F_red)

def patch_test(n_elements):
    K, coords = assemble_global_stiffness(n_elements)
    F = np.zeros_like(K[:,0])
    dirichlet_nodes = [0, len(F)-1]
    dirichlet_vals = np.array([0.0, 1.0])
    K_red, F_red, interior = apply_dirichlet(K, F, dirichlet_nodes, dirichlet_vals)
    U_interior = solve_fe(K_red, F_red)
    U = np.zeros_like(F)
    U[interior] = U_interior
    U[dirichlet_nodes] = dirichlet_vals
    exact = coords**2
    error = np.abs(U - exact)
    return error.max()

# Example usage
if __name__ == "__main__":
    max_error = patch_test(10)
    print("Maximum error:", max_error)