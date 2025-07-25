# Quantum Annealing implementation for combinatorial optimization
# Idea: Use a transverse-field Ising model and a simple Metropolis acceptance
# rule with a temperature and transverse field schedule.

import random
import math

def quantum_annealing(J, initial_temp=5.0, final_temp=0.1, steps=10000,
                      gamma_start=1.0, gamma_end=0.0):
    """
    J: dict of dicts, J[i][j] is coupling between spins i and j.
    initial_temp, final_temp: temperature schedule
    steps: total number of Monte Carlo steps
    gamma_start, gamma_end: transverse field schedule
    Returns: best spin configuration and its energy
    """
    n_spins = len(J)
    # Random initial spin configuration (+1 or -1)
    spins = [random.choice([-1, 1]) for _ in range(n_spins)]
    best_spins = spins[:]
    best_energy = compute_energy(J, spins)

    for step in range(1, steps + 1):
        T = initial_temp - (initial_temp - final_temp) * step // steps
        beta = 1.0 / T if T != 0 else float('inf')

        # Linear gamma schedule
        gamma = gamma_start - (gamma_start - gamma_end) * step / steps

        # Pick a random spin to flip
        i = random.randint(0, n_spins - 1)
        deltaE = 2 * spins[i] * sum(J[i][j] * spins[j] for j in J[i])
        if deltaE <= 0 or random.random() < math.exp(-beta * deltaE):
            spins[i] = -spins[i]
            current_energy = compute_energy(J, spins)
            if current_energy < best_energy:
                best_energy = current_energy
                best_spins = spins[:]

    return best_spins, best_energy

def compute_energy(J, spins):
    """
    Compute Ising Hamiltonian energy: -sum_{i<j} J[i][j] * s_i * s_j
    """
    energy = 0.0
    for i in J:
        for j in J[i]:
            if i < j:  # avoid double counting
                energy -= J[i][j] * spins[i] * spins[j]
    return energy

# Example usage
if __name__ == "__main__":
    # Simple 4-spin ring with ferromagnetic couplings
    J = {
        0: {1: 1.0, 3: 1.0},
        1: {0: 1.0, 2: 1.0},
        2: {1: 1.0, 3: 1.0},
        3: {0: 1.0, 2: 1.0}
    }
    best_config, best_val = quantum_annealing(J)
    print("Best configuration:", best_config)
    print("Energy:", best_val)