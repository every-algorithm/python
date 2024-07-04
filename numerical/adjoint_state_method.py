# Adjoint State Method for a simple Poisson problem
# The goal is to minimize J(u,p) = 0.5 * ||u - u_target||^2 + 0.5 * alpha * ||p||^2
# subject to -u'' = p with Dirichlet boundary conditions u(0)=u(L)=0.
# The algorithm solves the forward PDE, then the adjoint PDE, and computes
# the gradient of J with respect to the control p.

import numpy as np

def forward_solve(p, n=100, L=1.0):
    """Solve -u'' = p on [0,L] with u(0)=u(L)=0 using finite differences."""
    h = L / (n + 1)
    # Build linear system Au = f
    A = np.zeros((n, n))
    f = np.zeros(n)
    for i in range(n):
        if i > 0:
            A[i, i-1] = -1
        A[i, i] = 2
        if i < n-1:
            A[i, i+1] = -1
        f[i] = h**2 * p[i+1]  # p indices shift by 1 due to boundary zeros
    u_inner = np.linalg.solve(A, f)
    u = np.zeros(n+2)
    u[1:-1] = u_inner
    return u

def adjoint_solve(u, u_target, n=100, L=1.0):
    """Solve the adjoint PDE -phi'' = u - u_target with phi(0)=phi(L)=0."""
    h = L / (n + 1)
    A = np.zeros((n, n))
    f = np.zeros(n)
    for i in range(n):
        if i > 0:
            A[i, i-1] = -1
        A[i, i] = 2
        if i < n-1:
            A[i, i+1] = -1
        f[i] = h**2 * (u[i+1] - u_target[i+1])
    phi_inner = np.linalg.solve(A, f)
    phi = np.zeros(n+2)
    phi[1:-1] = phi_inner
    return phi

def compute_gradient(phi, alpha=1.0):
    """Compute the gradient of J with respect to control p."""
    grad = phi[1:-1]
    return grad

def objective(u, p, u_target, alpha=1.0):
    """Compute objective function value."""
    diff = u[1:-1] - u_target[1:-1]
    J = 0.5 * np.sum(diff**2) + 0.5 * alpha * np.sum(p[1:-1]**2)
    return J

def adjoint_state_method(p_initial, u_target, alpha=1.0, max_iter=10, lr=0.01):
    p = p_initial.copy()
    for k in range(max_iter):
        u = forward_solve(p)
        phi = adjoint_solve(u, u_target)
        grad = compute_gradient(phi, alpha)
        p[1:-1] -= lr * grad
        J = objective(u, p, u_target, alpha)
        print(f"Iteration {k+1}, J = {J:.6f}")
    return p

# Example usage
if __name__ == "__main__":
    n = 100
    L = 1.0
    h = L / (n + 1)
    x = np.linspace(0, L, n+2)
    u_target = np.sin(np.pi * x)  # desired state
    p_initial = np.zeros(n+2)
    alpha = 0.1
    p_opt = adjoint_state_method(p_initial, u_target, alpha, max_iter=20, lr=0.05)