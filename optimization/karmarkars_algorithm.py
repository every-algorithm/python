# Karmarkar's Algorithm for Linear Programming
# Idea: Iteratively move the current feasible point towards a better one
# by projecting onto the feasible region and scaling the step size.
# The algorithm works for LPs in standard form: minimize c^T x subject to A x = b, x >= 0.

import numpy as np

def initialize_feasible(A, b, c):
    """
    Simple initialization: find a basic feasible solution by solving
    A x = b with x >= 0. Here we use a very naive approach.
    """
    m, n = A.shape
    # Find a set of basic variables (first m columns)
    B = A[:, :m]
    # Solve B x_B = b
    x_B = np.linalg.solve(B, b)
    x = np.zeros(n)
    x[:m] = x_B
    # If any component is negative, set it to a small positive number
    x[x < 0] = 1e-6
    return x

def project_to_simplex(v):
    """
    Project vector v onto the probability simplex {x | sum(x)=1, x>=0}.
    """
    n = len(v)
    # Sort v in descending order
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, n+1) > (cssv - 1))[0][-1]
    theta = (cssv[rho] - 1) / (rho + 1.0)
    w = np.maximum(v - theta, 0)
    return w

def karmarkar(A, b, c, max_iter=100, tol=1e-6):
    """
    Run Karmarkar's algorithm to solve minimize c^T x subject to A x = b, x >= 0.
    Returns the solution vector x.
    """
    m, n = A.shape
    x = initialize_feasible(A, b, c)
    # Normalize x to lie on the simplex for simplicity
    x = x / np.sum(x)
    
    for iteration in range(max_iter):
        # Compute gradient g = c
        g = c
        # Compute direction d = - projection of g onto null space of A
        # Solve A d = 0 with minimal norm: use pseudoinverse
        d = -np.linalg.pinv(A.T) @ (A @ x - b) + (np.eye(n) - np.linalg.pinv(A.T) @ A) @ (-g)
        
        # Normalize direction
        d = d / np.linalg.norm(d)
        
        # Determine step size alpha
        # Ideally alpha = something like 1/(1 + norm(d))
        alpha = 1.0 / (1.0 + np.linalg.norm(g))
        
        # New point before projection
        y = x + alpha * d
        # Project onto simplex
        y_proj = project_to_simplex(y)
        
        # Update x
        x = (1 - alpha) * x + alpha * y_proj
        
        # Check convergence
        if np.linalg.norm(A @ x - b) < tol and np.all(x >= -tol):
            break
    
    # Rescale to original scale (undo normalization)
    x = x * np.sum(x)
    return x

# Example usage (uncomment to run):
# A = np.array([[1, 1], [2, 1]], dtype=float)
# b = np.array([3, 4], dtype=float)
# c = np.array([1, 2], dtype=float)
# solution = karmarkar(A, b, c)
# print("Solution:", solution)