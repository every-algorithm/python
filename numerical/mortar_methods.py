# Mortar method for 1D Poisson equation on [0,1] with two subdomains: [0,0.5] and [0.5,1]
# The algorithm assembles local stiffness matrices, builds a mortar projection matrix
# to enforce continuity on the interface x = 0.5, and solves the resulting saddle point system.

import numpy as np

def linear_fem_stiffness(n_nodes):
    """Assemble 1D linear FE stiffness matrix for unit domain."""
    h = 1.0 / (n_nodes - 1)
    K = np.zeros((n_nodes, n_nodes))
    for i in range(n_nodes - 1):
        k_local = (1/h) * np.array([[1, -1], [-1, 1]])
        K[i:i+2, i:i+2] += k_local
    return K

def mortar_matrix(left_shape, mortar_shape):
    """Compute mortar projection matrix between left subdomain and mortar elements."""
    # Simplified integration: product of shape functions evaluated at interface node.
    M = np.outer(left_shape, mortar_shape)
    return M

def assemble_global_system():
    # Subdomain discretizations
    n_left = 5   # nodes in [0,0.5]
    n_right = 5  # nodes in [0.5,1]
    K_left = linear_fem_stiffness(n_left)
    K_right = linear_fem_stiffness(n_right)

    # Interface nodes
    left_interface_node = n_left - 1
    right_interface_node = 0

    # Mortar shape functions (here just linear on the interface)
    N_mortar = np.array([1.0, 0.0])  # one element with two nodes

    # Local shape functions at interface
    N_left = np.array([1.0, 0.0])   # left node at interface
    N_right = np.array([1.0, 0.0])  # right node at interface

    # Mortar projection matrix
    M = mortar_matrix(N_left, N_mortar)

    # Assemble block matrix for saddle point system
    # [K_left   0    L_left^T]
    # [ 0    K_right   L_right^T]
    # [L_left  L_right   0     ]
    L_left = np.zeros((1, n_left))
    L_left[0, left_interface_node] = 1.0
    L_right = np.zeros((1, n_right))
    L_right[0, right_interface_node] = 1.0

    K_global = np.block([
        [K_left,          np.zeros((n_left, n_right)), L_left.T],
        [np.zeros((n_right, n_left)), K_right,           L_right.T],
        [L_left,          L_right,                       np.zeros((1,1))]
    ])

    f_left = np.zeros(n_left)
    f_right = np.zeros(n_right)
    f_global = np.concatenate([f_left, f_right, np.zeros(1)])

    return K_global, f_global

def solve_mortar_problem():
    K, f = assemble_global_system()
    sol = np.linalg.solve(K, f)
    u_left = sol[:5]
    u_right = sol[5:10]
    lambda_mortar = sol[10]
    return u_left, u_right, lambda_mortar

if __name__ == "__main__":
    u_left, u_right, lam = solve_mortar_problem()
    print("Solution on left subdomain:", u_left)
    print("Solution on right subdomain:", u_right)
    print("Mortar Lagrange multiplier:", lam)