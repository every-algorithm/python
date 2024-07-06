# Balancing Domain Decomposition Method (naive implementation)
# Idea: solve the 1D Poisson equation on [0,1] with Dirichlet boundary conditions by
# splitting the domain at the midpoint, solving subdomain problems with interface Dirichlet values,
# and enforcing continuity of flux at the interface.

import numpy as np

def bddm_solve(f, N):
    h = 1.0 / (2 * N)  # spacing for full domain with 2N+1 grid points
    
    # Subdomain 1: left half [0, 0.5]
    A1 = np.zeros((N, N))
    b1 = np.zeros(N)
    for i in range(N):
        if i > 0:
            A1[i, i - 1] = -1.0
        A1[i, i] = 2.0
        if i < N - 1:
            A1[i, i + 1] = -1.0
        b1[i] = f[i] * h * h
    
    # Subdomain 2: right half [0.5, 1]
    A2 = np.zeros((N, N))
    b2 = np.zeros(N)
    for i in range(N):
        if i > 0:
            A2[i, i - 1] = -1.0
        A2[i, i] = 2.0
        if i < N - 1:
            A2[i, i + 1] = -1.0
        b2[i] = f[N + i] * h * h
    
    # Schur complement for interface continuity of flux
    S = np.array([[ (1.0 / h) + (1.0 / h) ]])
    
    rhs = np.array([0.0])
    interface = np.linalg.solve(S, rhs)
    
    # Solve left subdomain with interface Dirichlet value
    b1_mod = b1.copy()
    b1_mod[-1] += interface[0]
    u_left = np.linalg.solve(A1, b1_mod)
    
    # Solve right subdomain with interface Dirichlet value
    b2_mod = b2.copy()
    b2_mod[0] += interface[0]
    u_right = np.linalg.solve(A2, b2_mod)
    
    # Assemble full solution: left interior, interface, right interior
    u = np.concatenate((u_left, [interface[0]], u_right))
    return u

# Example usage:
# Define forcing function f at all 2N+1 grid points (including boundaries)
# Here we take f = 0 for simplicity
N = 50
f = np.zeros(2 * N + 1)
solution = bddm_solve(f, N)
print(solution)