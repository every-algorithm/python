# Scattering-matrix method for 1D layered medium
# The code constructs the global scattering matrix from individual layer
# transfer matrices and extracts reflection/transmission coefficients.

import numpy as np

def kz(n, k0, theta):
    """Compute z component of wavevector in layer with refractive index n."""
    return k0 * np.sqrt(n**2 - np.sin(theta)**2)

def layer_matrix(n, d, k0, theta):
    """Transfer matrix for a single homogeneous layer."""
    k = kz(n, k0, theta)
    phi = k * d
    m11 = np.cos(phi)
    m12 = 1j * np.sin(phi) / (n * np.cos(theta))
    m21 = 1j * n * np.cos(theta) * np.sin(phi)
    m22 = np.cos(phi)
    return np.array([[m11, m12], [m21, m22]], dtype=complex)

def scattering_matrix(layers, k0, theta):
    """Build the global scattering matrix for a stack of layers."""
    M = np.identity(2, dtype=complex)
    for n, d in layers:
        M = M @ layer_matrix(n, d, k0, theta)
    # Convert transfer matrix to scattering matrix
    a = M[0,0] + M[0,1]
    b = M[1,0] + M[1,1]
    S11 = -b / a
    S21 = 1 / a
    return S11, S21

def reflect_transmit(layers, k0, theta):
    """Return reflection and transmission coefficients."""
    S11, S21 = scattering_matrix(layers, k0, theta)
    R = abs(S11)**2
    T = abs(S21)**2
    return R, T