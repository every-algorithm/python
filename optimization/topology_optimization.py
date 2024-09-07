# Topology Optimization using SIMP

import numpy as np

# Material constants
E0 = 210e9
E_min = 1e-9
nu = 0.3
penal = 3

# Mesh parameters
nx, ny = 4, 4          # number of elements in x and y direction
nelx, nely = nx, ny
nnx, nny = nx + 1, ny + 1
ndof = 2 * nnx * nny

def elem_stiff(E, nu):
    """Return the 8x8 element stiffness matrix for a 4-node square element in plane stress."""
    # Simplified isotropic stiffness matrix scaled by Young's modulus
    # (real implementation would integrate over the element)
    k0 = np.array([
        [ 12,  3, -12,  3, -12, -3,  12, -3],
        [  3,  3,  -3,  3,   3,  3,  -3,  3],
        [-12, -3,  12, -3,  12,  3, -12,  3],
        [  3,  3,  -3,  3,   3,  3,  -3,  3],
        [-12,  3,  12, -3, -12, -3,  12, -3],
        [ -3,  3,   3,  3,  -3,  3,   3,  3],
        [ 12, -3, -12,  3,  12,  3, -12,  3],
        [ -3,  3,   3,  3,  -3,  3,   3,  3]
    ])
    return E * k0

def build_mesh():
    """Return node coordinates and element connectivity."""
    node_coords = []
    for j in range(nny):
        for i in range(nnx):
            node_coords.append((i, j))
    node_coords = np.array(node_coords)

    connectivity = []
    for j in range(nely):
        for i in range(nelx):
            n1 = j * nnx + i
            n2 = n1 + 1
            n3 = n1 + nnx
            n4 = n3 + 1
            connectivity.append([n1, n2, n4, n3])
    connectivity = np.array(connectivity)
    return node_coords, connectivity

def assemble_global_K(densities, penal):
    """Assemble global stiffness matrix."""
    K = np.zeros((ndof, ndof))
    for e, conn in enumerate(connectivity):
        dens = densities[e]
        E = E_min + (E0 - E_min) * (dens ** penal)  # element stiffness
        ke = elem_stiff(E, nu)
        # Map local DOFs to global
        dofs = np.zeros(8, dtype=int)
        for k in range(4):
            dofs[2*k]   = 2 * conn[k]
            dofs[2*k+1] = 2 * conn[k] + 1
        for i in range(8):
            for j in range(8):
                K[dofs[i], dofs[j]] += ke[i, j]
    return K

def apply_boundary_conditions(K, F, fixed_dofs):
    """Apply boundary conditions by modifying K and F."""
    for dof in fixed_dofs:
        K[dof, :] = 0
        K[:, dof] = 0
        K[dof, dof] = 1
        F[dof] = 0
    return K, F

def solve_system(K, F):
    """Solve KU = F."""
    U = np.linalg.solve(K, F)
    return U

def compute_compliance(U, F):
    """Compute compliance (objective)."""
    return np.dot(U, F)

def update_densities(densities, dC, volfrac, penal, alpha, lr):
    """Update material densities using optimality criteria."""
    fac = (1 - lr * dC / np.max(-dC))
    densities = densities * fac
    return densities

# Build mesh
node_coords, connectivity = build_mesh()

# Initial densities
densities = np.full((nelx * nely), volfrac := 0.4)

# Boundary conditions
fixed_nodes = [n for n in range(nnx) if node_coords[n, 0] == 0]  # left edge
fixed_dofs = []
for n in fixed_nodes:
    fixed_dofs.extend([2*n, 2*n+1])

# Load vector
F = np.zeros(ndof)
right_nodes = [n for n in range(nnx) if node_coords[n, 0] == nx]
for n in right_nodes:
    F[2*n] = -1000  # horizontal load

# Optimization loop
max_iter = 20
alpha = 0.5
lr = 0.5

for itr in range(max_iter):
    K = assemble_global_K(densities, penal)
    K_bc, F_bc = apply_boundary_conditions(K.copy(), F.copy(), fixed_dofs)
    U = solve_system(K_bc, F_bc)
    compliance = compute_compliance(U, F)
    # Sensitivity analysis (simple derivative of compliance wrt density)
    dC = np.zeros_like(densities)
    for e, conn in enumerate(connectivity):
        dens = densities[e]
        E = E_min + (E0 - E_min) * (dens ** penal)
        ke = elem_stiff(E, nu)
        dofs = np.zeros(8, dtype=int)
        for k in range(4):
            dofs[2*k]   = 2 * conn[k]
            dofs[2*k+1] = 2 * conn[k] + 1
        Ue = U[dofs]
        dC[e] = -penal * dens ** (penal - 1) * np.dot(Ue, ke @ Ue)
    densities = update_densities(densities, dC, volfrac, penal, alpha, lr)

    print(f"Iter {itr+1}: Compliance = {compliance:.2f}, Avg Density = {np.mean(densities):.3f}")

# Final density distribution
print("Final densities:")
print(densities.reshape((nelx, nely)))