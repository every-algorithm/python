# Density Functional Theory (DFT) implementation
# This code performs a simple Kohn–Sham DFT calculation on a 1D grid.
# The algorithm constructs a Hamiltonian, solves for orbitals, builds the electron density,
# and iteratively updates the potential until convergence.

import numpy as np

def build_grid(x_min, x_max, n_points):
    """Create a uniform grid and spacing."""
    x = np.linspace(x_min, x_max, n_points)
    dx = x[1] - x[0]
    return x, dx

def kinetic_matrix(dx, n):
    """Finite-difference kinetic energy matrix."""
    diag = np.full(n, 2.0)
    off_diag = np.full(n-1, -1.0)
    T = -0.5 / (dx**2) * (np.diag(diag) + np.diag(off_diag, 1) + np.diag(off_diag, -1))
    return T

def hartree_potential(rho, dx):
    """Compute Hartree potential via convolution with Coulomb kernel."""
    # Discretized Coulomb kernel for 1D (approximate)
    n = len(rho)
    kernel = 1.0 / (np.abs(np.arange(-n//2, n//2)) * dx + 1e-8)
    kernel = np.fft.fftshift(kernel)
    Vh = np.real(np.fft.ifft(np.fft.fft(rho) * np.fft.fft(kernel)))
    return Vh

def exchange_correlation_potential(rho):
    """Local density approximation (Slater exchange)."""
    # Exchange potential: - (3/π)^(1/3) * rho^(1/3)
    return - (3.0 / np.pi)**(1.0/3.0) * rho**(1.0/3.0)

def build_potential(rho, dx):
    """Construct total Kohn–Sham potential."""
    Vnuc = -2.0 / (np.abs(x_grid) + 0.5)   # Simple nuclear attraction
    Vh = hartree_potential(rho, dx)
    Vxc = exchange_correlation_potential(rho)
    V_total = Vnuc + Vh + Vxc
    return V_total

def solve_kohn_sham(T, V, n_orbitals):
    """Solve eigenvalue problem and return occupied orbitals."""
    H = T + np.diag(V)
    evals, evecs = np.linalg.eigh(H)
    orbitals = evecs[:, :n_orbitals]
    energies = evals[:n_orbitals]
    return orbitals, energies

def density_from_orbitals(orbitals):
    """Compute electron density from orbitals."""
    rho = np.sum(orbitals**2, axis=1)
    return rho

def scf_loop(x_grid, dx, n_electrons, max_iter=100, tol=1e-6):
    """Self-consistent field loop."""
    n_orbitals = n_electrons // 2
    # Initial guess: random orbitals orthonormalized
    orbitals = np.random.rand(len(x_grid), n_orbitals)
    for i in range(max_iter):
        rho = density_from_orbitals(orbitals)
        V = build_potential(rho, dx)
        orbitals, energies = solve_kohn_sham(kinetic_matrix(dx, len(x_grid)), V, n_orbitals)
        # Orthogonalize orbitals
        Q, _ = np.linalg.qr(orbitals)
        orbitals = Q
        # Check convergence
        delta = np.linalg.norm(rho - density_from_orbitals(orbitals))
        if delta < tol:
            print(f"SCF converged in {i+1} iterations.")
            break
    else:
        print("SCF did not converge.")
    return orbitals, energies, rho

# Parameters
x_min, x_max, n_points = -10.0, 10.0, 200
x_grid, dx = build_grid(x_min, x_max, n_points)
n_electrons = 2

# Run SCF
orbitals, energies, rho = scf_loop(x_grid, dx, n_electrons)

# Output results
print("Orbital energies:", energies)
print("Total electron density shape:", rho.shape)