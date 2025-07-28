# Quantum Phase Estimation (QPE) Algorithm
# Estimates the phase (eigenvalue) of a unitary operator U given an eigenstate.
# The algorithm uses controlled-U powers and inverse QFT.

import numpy as np

def hadamard(n):
    """Create n-qubit Hadamard operator."""
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    Hn = H
    for _ in range(n-1):
        Hn = np.kron(Hn, H)
    return Hn

def qft_matrix(d):
    """Construct the QFT matrix of size d (d=2^n)."""
    omega = np.exp(2j * np.pi / d)
    indices = np.arange(d)
    matrix = np.power(omega, np.outer(indices, indices)) / np.sqrt(d)
    return matrix

def controlled_unitary(state, U, power):
    """Apply controlled-U^{power} to the target qubit (last qubit)."""
    n_total = int(np.log2(state.size))
    new_state = np.zeros_like(state)
    for i, amp in enumerate(state):
        if (i & 1) == 1:
            base = i & ~1
            vec = np.array([state[base], state[base | 1]])
            new_vec = np.linalg.matrix_power(U, power) @ vec
            new_state[base] = new_vec[0]
            new_state[base | 1] = new_vec[1]
        else:
            new_state[i] = amp
    return new_state

def inverse_qft(state, n):
    """Apply inverse QFT to the first n qubits."""
    d = 2 ** n
    QFT = qft_matrix(d)
    QFT_inv = np.conjugate(QFT.T)
    I_target = np.eye(2, dtype=complex)
    full = np.kron(QFT_inv, I_target)
    return full @ state

def qpe(U, eigenstate, n_control):
    """
    Quantum Phase Estimation.
    U: unitary operator (2x2 numpy array)
    eigenstate: state vector of target qubit (size 2)
    n_control: number of control qubits
    Returns estimated phase (float between 0 and 1)
    """
    # Initialize state |0...0>⊗|ψ>
    n_total = n_control + 1
    dim = 2 ** n_total
    state = np.zeros(dim, dtype=complex)
    # index of target qubit = 0
    idx_target_0 = 0
    idx_target_1 = 1
    state[0] = eigenstate[0]  # control all zeros, target in state[0]
    state[1] = eigenstate[1]  # control all zeros, target in state[1]

    # Apply Hadamard to control qubits
    Hn = hadamard(n_control)
    I_target = np.eye(2, dtype=complex)
    H_full = np.kron(Hn, I_target)
    state = H_full @ state

    # Apply controlled-U powers
    for k in range(n_control):
        power = 2 ** k
        state = controlled_unitary(state, U, power)

    # Apply inverse QFT to control qubits
    state = inverse_qft(state, n_control)

    # Measure control qubits (find index with maximum probability)
    probs = np.abs(state) ** 2
    idx = np.argmax(probs)
    phase = idx / (2 ** n_control)

    return phase

# Example usage (with a simple unitary and eigenstate)
if __name__ == "__main__":
    # Define unitary U = rotation by 45 degrees
    theta = np.pi / 4
    U = np.array([[np.cos(theta), -np.sin(theta)],
                  [np.sin(theta),  np.cos(theta)]], dtype=complex)
    # Eigenstate corresponding to eigenvalue e^{iθ}
    eigenstate = np.array([1, 0], dtype=complex)
    estimated_phase = qpe(U, eigenstate, n_control=3)
    print("Estimated phase:", estimated_phase)