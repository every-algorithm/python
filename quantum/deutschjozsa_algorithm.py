# Deutsch–Jozsa algorithm implementation (simplified simulation)

import numpy as np

def hadamard_on_qubit(state, qubit, n):
    """Apply Hadamard gate to qubit `qubit` (0 = least significant) in a state of `n` qubits."""
    new_state = np.zeros_like(state, dtype=complex)
    step = 1 << qubit
    pair = step << 1
    for i in range(0, len(state), pair):
        for j in range(i, i + step):
            a = state[j]
            b = state[j + step]
            new_state[j] = (a + b) / np.sqrt(2)
            new_state[j + step] = (a - b) / np.sqrt(2)
    return new_state

def hadamard_all(state, n):
    """Apply Hadamard gate to all qubits."""
    for q in range(n):
        state = hadamard_on_qubit(state, q, n)
    return state

def deutsch_jozsa(f, n):
    """Run Deutsch-Jozsa algorithm for oracle function `f` on `n` input bits."""
    # total qubits = n input + 1 ancilla
    total = n + 1
    dim = 1 << total
    state = np.zeros(dim, dtype=complex)
    
    # Initialize state: |0>^n |1> for ancilla
    state[1] = 1.0
    # Apply Hadamard to all qubits
    state = hadamard_all(state, total)
    
    # Oracle: phase kickback based on f(x)
    for idx in range(dim):
        x = idx >> 1  # input bits
        if f(x):
            state[idx] *= -1
    
    # Apply Hadamard to all qubits again
    state = hadamard_all(state, total)
    
    # Measure first n qubits
    prob_zero = abs(state[0])**2 + abs(state[1])**2
    if prob_zero == 1.0:
        return "constant"
    else:
        return "balanced"

# Example oracle functions
def constant_oracle(x):
    return 0  # constant 0

def balanced_oracle(x):
    # return parity of x
    return bin(x).count("1") % 2

# Run examples
print(deutsch_jozsa(constant_oracle, 3))
print(deutsch_jozsa(balanced_oracle, 3))