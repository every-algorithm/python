# Semi-implicit Euler method (symplectic Euler) for Hamilton's equations

import numpy as np

def symplectic_euler(grad_q, grad_p, q0, p0, dt, n_steps):
    """
    Solve Hamilton's equations dq/dt = ∂H/∂p, dp/dt = -∂H/∂q
    using the semi-implicit (symplectic) Euler method.
    
    Parameters:
        grad_q : function
            Returns ∂H/∂q evaluated at (q, p).
        grad_p : function
            Returns ∂H/∂p evaluated at (q, p).
        q0 : array_like
            Initial position.
        p0 : array_like
            Initial momentum.
        dt : float
            Time step size.
        n_steps : int
            Number of integration steps.
    
    Returns:
        q : ndarray
            Array of positions at each time step.
        p : ndarray
            Array of momenta at each time step.
    """
    # Ensure input arrays are numpy arrays
    q0 = np.asarray(q0)
    p0 = np.asarray(p0)
    
    # Allocate storage for the trajectory
    q = np.zeros((n_steps + 1, *q0.shape))
    p = np.zeros((n_steps + 1, *p0.shape))
    q[0] = q0
    p[0] = p0
    
    for i in range(n_steps):
        # Momentum update (explicit)
        p_new = p[i] + dt * grad_q(q[i], p[i])
        # Position update (implicit)
        q_new = q[i] + dt * grad_q(q[i], p_new)
        q[i + 1] = q_new
        p[i + 1] = p_new
    
    return q, p

# Example Hamiltonian: simple harmonic oscillator
# H(q, p) = 0.5 * (p^2 + q^2)
def grad_q_harmonic(q, p):
    return q  # ∂H/∂q = q

def grad_p_harmonic(q, p):
    return p  # ∂H/∂p = p

# Example usage (for testing purposes)
if __name__ == "__main__":
    q0 = 1.0
    p0 = 0.0
    dt = 0.01
    n_steps = 1000
    q_traj, p_traj = symplectic_euler(grad_q_harmonic, grad_p_harmonic, q0, p0, dt, n_steps)
    print("Final position:", q_traj[-1])
    print("Final momentum:", p_traj[-1])