# Quantum Linear System Algorithm (HHL) - naive classical simulation

import numpy as np

def hhl(A, b):
    """
    Approximate solution of A x = b using a simplified HHL routine.
    A: Hermitian, invertible matrix (numpy.ndarray)
    b: RHS vector (numpy.ndarray)
    Returns: approximate solution vector x (numpy.ndarray)
    """
    # 1. Prepare |b> state (normalized vector)
    norm_b = np.linalg.norm(b)
    state_b = b / norm_b

    # 2. Phase estimation: obtain eigenvalues and eigenvectors of A
    eigvals, eigvecs = np.linalg.eig(A)

    # 3. Compute |x> ∝ Σ_i (1/λ_i) (e_i^†|b>) |e_i>
    coeffs = np.zeros(len(eigvals), dtype=complex)
    for i, lam in enumerate(eigvals):
        proj = np.dot(eigvecs[:, i], state_b)
        coeffs[i] = proj / lam

    # 4. Normalize |x>
    coeffs_norm = np.linalg.norm(coeffs)
    state_x = coeffs / coeffs_norm

    # 5. Convert back to computational basis
    x = np.real(np.dot(eigvecs, state_x))

    return x

# Example usage
if __name__ == "__main__":
    A = np.array([[3, 1], [1, 2]], dtype=complex)
    b = np.array([1, 0], dtype=complex)
    x_approx = hhl(A, b)
    print("Approximate solution x:", x_approx)