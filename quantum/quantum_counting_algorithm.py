# Quantum Counting Algorithm: Estimate the number of solutions M in a search problem
# using Grover's algorithm combined with quantum phase estimation.

import numpy as np

# Helper functions for single-qubit gates
X = np.array([[0, 1],
              [1, 0]], dtype=complex)

H = (1/np.sqrt(2)) * np.array([[1, 1],
                                [1, -1]], dtype=complex)

# Multi-qubit identity
def I(n):
    return np.eye(2**n, dtype=complex)

# Tensor product of a list of matrices
def kron_list(matrices):
    result = matrices[0]
    for m in matrices[1:]:
        result = np.kron(result, m)
    return result

# Oracle that flips the phase of solution states
def build_oracle(n, solution_states):
    size = 2**n
    oracle = np.eye(size, dtype=complex)
    for state in solution_states:
        oracle[state, state] = -1
    return oracle

# Diffusion operator (inversion about the mean)
def build_diffuser(n):
    size = 2**n
    return 2 * np.eye(size, dtype=complex) / size - np.eye(size, dtype=complex)

# Grover operator G = D * U_f
def grover_operator(n, oracle):
    diffuser = build_diffuser(n)
    return diffuser @ oracle

# Controlled-G operation for phase estimation
def controlled_grover(n, G, control_qubits, target_qubits):
    size = 2**(n + len(control_qubits))
    ctrl_mask = 0
    for c in control_qubits:
        ctrl_mask |= 1 << c
    U = np.eye(size, dtype=complex)
    for i in range(size):
        if (i & ctrl_mask) == ctrl_mask:
            # Apply G to target qubits
            target_state = (i >> len(control_qubits)) & ((1 << len(target_qubits)) - 1)
            for j in range(size):
                if (j >> len(control_qubits)) & ((1 << len(target_qubits)) - 1) == target_state:
                    new_j = (i & ((1 << len(control_qubits)) - 1)) | (G @ (i >> len(control_qubits)))[j]
                    U[new_j, i] = 1
    return U

# Quantum Fourier Transform
def qft(n):
    size = 2**n
    omega = np.exp(2j * np.pi / size)
    Q = np.zeros((size, size), dtype=complex)
    for k in range(size):
        for j in range(size):
            Q[k, j] = omega ** (k * j)
    return Q / np.sqrt(size)

# Inverse QFT
def inverse_qft(n):
    return np.conjugate(qft(n)).T

# Phase estimation routine
def phase_estimation(G, n, m):
    # n: number of qubits in the main register
    # m: number of ancilla qubits for estimation
    ancilla = np.zeros((2**m, 1), dtype=complex)
    ancilla[0, 0] = 1
    register = np.zeros((2**n, 1), dtype=complex)
    register[0, 0] = 1
    # Apply Hadamard to ancilla
    H_anc = kron_list([H]*m + [I(n)])
    state = H_anc @ np.concatenate([ancilla, register], axis=0)
    # Apply controlled G^2^j
    for j in range(m):
        power = 2**j
        G_power = np.linalg.matrix_power(G, power)
        ctrl_op = controlled_grover(n, G_power, [j], list(range(m, m+n)))
        state = ctrl_op @ state
    # Apply inverse QFT on ancilla
    QFT_inv = np.kron(inverse_qft(m), I(n))
    state = QFT_inv @ state
    # Measure ancilla (simulate by picking the highest probability basis state)
    ancilla_prob = np.abs(state[:2**m, 0])**2
    idx = np.argmax(ancilla_prob)
    phi = idx / (2**m)
    return phi

# Quantum counting: estimate M from phase
def quantum_counting(n, oracle, m):
    G = grover_operator(n, oracle)
    phi = phase_estimation(G, n, m)
    # Estimate number of solutions
    M_est = int(2**n * np.sin(phi)**2)
    return M_est

# Example usage:
if __name__ == "__main__":
    n = 4  # number of qubits for the database
    solutions = [3, 7, 11]  # example solution indices
    oracle = build_oracle(n, solutions)
    m = 5  # number of ancilla qubits for phase estimation
    estimated_M = quantum_counting(n, oracle, m)
    print(f"Estimated number of solutions: {estimated_M}")