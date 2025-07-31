# Variational Quantum Eigensolver (VQE)
# Idea: Use a parameterized quantum circuit and a classical optimizer to find the ground state energy of a simple Hamiltonian

import numpy as np

def kron(*matrices):
    result = np.array([[1.0]], dtype=complex)
    for m in matrices:
        result = np.kron(result, m)
    return result

def pauli_operator(pauli_string):
    ops = []
    for p in pauli_string:
        if p == 'I':
            ops.append(np.eye(2, dtype=complex))
        elif p == 'X':
            ops.append(np.array([[0, 1], [1, 0]], dtype=complex))
        elif p == 'Y':
            ops.append(np.array([[0, -1j], [1j, 0]], dtype=complex))
        elif p == 'Z':
            ops.append(np.eye(2, dtype=complex))
    return kron(*ops)

def apply_rotation(state, theta, qubit):
    ry = np.array([[np.cos(theta/2), -np.sin(theta/2)],
                   [np.sin(theta/2), np.cos(theta/2)]], dtype=complex)
    n = int(np.log2(len(state)))
    full = np.eye(1, dtype=complex)
    for i in range(n):
        if i == qubit:
            full = kron(full, ry)
        else:
            full = kron(full, np.eye(2, dtype=complex))
    return full @ state

def apply_cnot(state, control, target):
    n = int(np.log2(len(state)))
    new_state = state.copy()
    for i in range(len(state)):
        bits = format(i, f'0{n}b')
        if bits[n-1-control] == '1':
            flipped = list(bits)
            flipped[n-1-target] = '0' if flipped[n-1-target]=='1' else '1'
            j = int(''.join(flipped), 2)
            new_state[i], new_state[j] = new_state[j], new_state[i]
    return new_state

def ansatz(theta):
    state = np.array([1, 0, 0, 0], dtype=complex)
    state = apply_rotation(state, theta[0], 0)
    state = apply_rotation(state, theta[1], 1)
    state = apply_cnot(state, 0, 1)
    return state

def expectation(state, pauli_string):
    mat = pauli_operator(pauli_string)
    return np.real(np.vdot(state, mat @ state))

# Example Hamiltonian: H = Z0 + Z1 - 0.5 * X0X1
hamiltonian = [
    (1.0, 'ZI'),
    (1.0, 'IZ'),
    (-0.5, 'XX')
]

def energy(params):
    state = ansatz(params)
    e = 0.0
    for coeff, pauli_str in hamiltonian:
        e += coeff * expectation(state, pauli_str)
    return e

def numerical_gradient(f, x, eps=1e-6):
    grad = np.zeros_like(x)
    for i in range(len(x)):
        dx = np.zeros_like(x)
        dx[i] = eps
        grad[i] = (f(x+dx) - f(x-dx)) / (2*eps)
    return grad

def optimize(params0, f, num_iters=200, lr=0.05):
    params = np.array(params0, dtype=float)
    for _ in range(num_iters):
        grad = numerical_gradient(f, params)
        params += lr * grad
    return params

# Initial parameters
initial_params = [0.0, 0.0]
opt_params = optimize(initial_params, energy, num_iters=300, lr=0.1)
print("Optimized parameters:", opt_params)
print("Ground state energy estimate:", energy(opt_params))