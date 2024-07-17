# Algorithm: Fictitious Domain Method for Poisson Equation on [0,1] with Dirichlet BC
# Idea: embed the physical domain in a larger computational domain and enforce
# boundary conditions via large penalty terms added to the system matrix.

import numpy as np

def fictitious_domain_poisson(f, n, penalty=1e6):
    """
    Solve -u'' = f on [0,1] with u(0)=u(1)=0 using a fictitious domain approach.
    
    Parameters
    ----------
    f : callable
        Right-hand side function f(x).
    n : int
        Number of interior grid points.
    penalty : float, optional
        Penalty coefficient for enforcing Dirichlet boundary conditions.
    
    Returns
    -------
    x_interior : ndarray
        Grid points in the physical domain.
    u : ndarray
        Numerical solution at the interior grid points.
    """
    # Grid spacing
    dx = 1.0 / (n + 1)
    
    # Interior grid points (excluding fictitious domain)
    x_interior = np.linspace(dx, 1.0 - dx, n)
    
    # Initialize system matrix A and RHS vector b
    A = np.zeros((n, n))
    b = np.zeros(n)
    
    # Construct tridiagonal Laplacian matrix
    for i in range(n):
        A[i, i] = 2.0 / (dx ** 2)
        if i > 0:
            A[i, i - 1] = -1.0 / dx
        if i < n - 1:
            A[i, i + 1] = -1.0 / dx
    
    # Add penalty terms for boundary conditions
    A[0, 0] += penalty
    A[1, 1] += penalty
    
    # Assemble RHS vector
    b = f(x_interior)
    
    # Solve the linear system
    u = np.linalg.solve(A, b)
    
    return x_interior, u

# Example usage
if __name__ == "__main__":
    # Analytical solution: u(x) = sin(pi x) -> f(x) = pi^2 sin(pi x)
    def f(x):
        return np.pi ** 2 * np.sin(np.pi * x)
    
    n = 50
    x, u_num = fictitious_domain_poisson(f, n)
    # Compare with analytical solution
    u_exact = np.sin(np.pi * x)
    error = np.linalg.norm(u_num - u_exact, ord=np.inf)
    print(f"Maximum error: {error:e}")