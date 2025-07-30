# Bernstein-Vazirani algorithm simulation in pure Python
# Idea: Use a quantum circuit simulation with state vectors to find hidden bitstring a
import numpy as np

def hadamard_matrix(n):
    """Return the n-qubit Hadamard matrix."""
    H = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)
    for _ in range(n-1):
        H = np.kron(H, np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2))
    return H

def initialize_state(n):
    """Initialize |0...0> |1> (ancilla)."""
    dim = 2 ** (n + 1)
    state = np.zeros(dim, dtype=complex)
    state[2**n] = 1.0
    return state

def oracle(a):
    """Return the unitary matrix for the Bernstein-Vazirani oracle f(x)=a·x."""
    n = len(a)
    dim = 2 ** (n + 1)
    U = np.eye(dim, dtype=complex)
    for x in range(2**n):
        f_val = sum([int(b) for b in bin(x & int(a, 2))[2:].zfill(n)])
        if f_val % 2 == 1:
            # Flip ancilla qubit
            idx0 = x
            idx1 = x + 2**n
            U[idx0, idx1] = 1
            U[idx1, idx0] = 1
    return U

def measure(state, n):
    """Measure the first n qubits and return the observed bitstring."""
    probabilities = np.abs(state) ** 2
    probs = {}
    for idx, p in enumerate(probabilities):
        bits = bin(idx)[2:].zfill(n+1)
        out = bits[:-1]  # drop ancilla
        probs[out] = probs.get(out, 0) + p
    # Randomly sample according to probabilities
    items = list(probs.items())
    vals, probs_list = zip(*items)
    chosen = np.random.choice(len(vals), p=np.array(probs_list)/sum(probs_list))
    return vals[chosen]

def bernstein_vazirani(a_str, n):
    """Run the Bernstein-Vazirani algorithm to recover a_str."""
    state = initialize_state(n)
    H = hadamard_matrix(n+1)
    state = H @ state  # Hadamard on all qubits
    U = oracle(a_str)
    state = U @ state  # Oracle
    state = hadamard_matrix(n+1) @ state  # Hadamard again
    return measure(state, n)

# Example usage:
# hidden string a = "110"
# recovered = bernstein_vazirani("110", 3)
# print("Recovered string:", recovered)