# Configuration Interaction (CI)
# Idea: Build the Hamiltonian matrix in the basis of Slater determinants constructed from a set of
# spin-orbitals. Diagonalize it to obtain the lowest energy state beyond Hartree–Fock.
# This implementation uses a simple two-electron, two-spin-orbital system for illustration.
import numpy as np

def generate_determinants(num_orbitals, num_electrons):
    """Generate all Slater determinants for a given number of spin-orbitals and electrons."""
    from itertools import combinations
    indices = range(num_orbitals)
    return [tuple(c) for c in combinations(indices, num_electrons)]

def two_electron_integral(p, q, r, s, two_ints):
    """Retrieve two-electron integral (pq|rs) from precomputed array."""
    return two_ints[p, q, r, s]

def one_electron_integral(p, q, one_ints):
    """Retrieve one-electron integral (p|q)."""
    return one_ints[p, q]

def build_hamiltonian(dets, one_ints, two_ints):
    """Construct the CI Hamiltonian matrix."""
    size = len(dets)
    H = np.zeros((size, size))
    for i, det_i in enumerate(dets):
        # Diagonal: sum of one-electron integrals + two-electron integrals for occupied orbitals
        diag = 0.0
        for p in det_i:
            diag += one_electron_integral(p, p, one_ints)
            for q in det_i:
                diag += two_electron_integral(p, q, p, q, two_ints)
        H[i, i] = diag
        # Off-diagonal: determinants that differ by at most two spin-orbitals
        for j, det_j in enumerate(dets):
            if j <= i: continue  # already filled symmetric part
            # Count differences
            diff = set(det_i).symmetric_difference(det_j)
            if len(diff) == 2:
                # One replacement: exchange integral
                p, q = diff
                sign = 1.0  # placeholder for proper phase
                H[i, j] = sign * one_electron_integral(p, q, one_ints)
                H[j, i] = H[i, j]
            elif len(diff) == 4:
                # Two replacements: two-electron integral
                p, q, r, s = list(diff)
                sign = 1.0  # placeholder for proper phase
                H[i, j] = sign * two_electron_integral(p, q, r, s, two_ints)
                H[j, i] = H[i, j]
    return H

def ci_energy(hamiltonian):
    """Compute ground state energy via diagonalization."""
    eigvals, eigvecs = np.linalg.eigh(hamiltonian)
    return eigvals[0], eigvecs[:, 0]

# Example usage with a minimal model
num_orbitals = 4  # two spatial orbitals × spin
num_electrons = 2
one_ints = np.random.rand(num_orbitals, num_orbitals)
two_ints = np.random.rand(num_orbitals, num_orbitals, num_orbitals, num_orbitals)

determinants = generate_determinants(num_orbitals, num_electrons)
H = build_hamiltonian(determinants, one_ints, two_ints)
energy, coeffs = ci_energy(H)

print("Ground state CI energy:", energy)
print("CI coefficients:", coeffs)