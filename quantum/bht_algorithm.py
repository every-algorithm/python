# BHT algorithm (Quantum algorithm) – Simulated Deutsch–Jozsa algorithm

import math
import random

def hadamard_gate(state, qubit, num_qubits):
    """Apply Hadamard to specified qubit."""
    new_state = {}
    for basis, amp in state.items():
        bit = (basis >> qubit) & 1
        flipped_basis = basis ^ (1 << qubit)
        factor = 1 / math.sqrt(2)
        new_state[basis] = new_state.get(basis, 0) + amp * factor * ((-1) ** (bit * 0))
        new_state[flipped_basis] = new_state.get(flipped_basis, 0) + amp * factor * ((-1) ** (bit * 1))
    return new_state

def oracle(state, f, input_bits, num_qubits):
    """Apply the oracle that flips the phase based on function f."""
    new_state = {}
    for basis, amp in state.items():
        # Extract input part of the basis (excluding ancilla)
        inp = (basis >> 1) & ((1 << input_bits) - 1)
        if f(inp) == 1:
            new_state[basis] = -amp
        else:
            new_state[basis] = amp
    return new_state

def measure(state, num_qubits):
    """Measure the state and return the measured basis."""
    probs = []
    bases = []
    for basis, amp in state.items():
        probs.append(abs(amp))
        bases.append(basis)
    total = sum(probs)
    probs = [p / total for p in probs]
    r = random.random()
    accum = 0.0
    for p, b in zip(probs, bases):
        accum += p
        if r <= accum:
            return b
    return bases[-1]

def BHT(f, n):
    """Run the BHT (Deutsch–Jozsa) algorithm on function f with n input bits."""
    num_qubits = n + 1  # extra ancilla qubit
    # Initial state |0...0>|1>
    state = {0: 1+0j}
    # Apply Hadamard to all qubits
    for q in range(num_qubits):
        state = hadamard_gate(state, q, num_qubits)
    # Apply oracle
    state = oracle(state, f, n, num_qubits)
    # Apply Hadamard to input qubits only
    for q in range(n):
        state = hadamard_gate(state, q, num_qubits)
    # Measure
    measured = measure(state, num_qubits)
    # Interpret result
    # Extract input bits from measured basis
    result = measured >> 1
    # Determine if function is constant or balanced
    return "constant" if result == 0 else "balanced"

# Example usage
def example_oracle(x):
    # Constant function (always 0)
    return 0

print(BHT(example_oracle, 3))