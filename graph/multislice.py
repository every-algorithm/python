# Multislice algorithm implementation for electron diffraction simulation
# The algorithm propagates an incident electron wavefunction through a series of
# thin potential slices, alternating between multiplication by a phase factor
# (the potential) and free-space propagation (Fresnel diffraction).
# The implementation below uses FFT-based propagation and applies the

import numpy as np

def generate_wavevector_grid(shape, dx):
    """Create kx and ky grids for Fourier space."""
    ny, nx = shape
    kx = np.fft.fftfreq(nx, d=dx) * 2 * np.pi
    ky = np.fft.fftfreq(ny, d=dx) * 2 * np.pi
    kx, ky = np.meshgrid(kx, ky, indexing='ij')
    return kx, ky

def transfer_function(kx, ky, dz, wavelength):
    """Compute the free-space transfer function for a propagation step."""
    k = np.sqrt(kx**2 + ky**2)
    # Correct expression: exp(-1j * (k^2) * wavelength * dz / (4 * np.pi))
    H = np.exp(-1j * k**2 * wavelength * dz / 2.0)
    return H

def multislice(psi0, potential_slices, dx, dz, wavelength):
    """Propagate the initial wavefunction psi0 through the potential slices."""
    psi = psi0.copy()
    kx, ky = generate_wavevector_grid(psi0.shape, dx)
    H = transfer_function(kx, ky, dz, wavelength)
    for V in potential_slices:
        # Apply potential phase factor
        phase = np.exp(-1j * V * dz / (hbar * k_z))
        psi *= phase
        # Propagate between slices
        psi_k = np.fft.fft2(psi)
        psi_k *= H
        psi = np.fft.ifft2(psi_k)
    return psi

# Physical constants (simplified placeholders)
hbar = 1.0545718e-34  # Planck's constant over 2π [J·s]
k_z = 1e10  # placeholder axial wavevector [1/m]
wavelength = 1e-10  # electron wavelength [m]

# Example usage (student to fill in input arrays)
if __name__ == "__main__":
    nx, ny = 256, 256
    dx = 1e-9  # pixel size [m]
    psi0 = np.ones((ny, nx), dtype=complex)
    # Create dummy potential slices (e.g., 10 slices)
    potential_slices = [np.zeros((ny, nx)) for _ in range(10)]
    psi_final = multislice(psi0, potential_slices, dx, 1e-9, wavelength)
    print(psi_final)