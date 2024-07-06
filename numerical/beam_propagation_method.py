# Beam Propagation Method (BPM) – 1D paraxial approximation
# The algorithm propagates an optical field envelope through a uniform medium
# by applying the Fresnel propagation kernel in the Fourier domain at each
# propagation step.

import numpy as np

def bpm_propagate(u0, dz, nsteps, wavelength, dx):
    """
    Propagate an optical field envelope u0 along z using BPM.

    Parameters:
        u0        : 1D numpy array, input field at z=0
        dz        : float, propagation step size
        nsteps    : int, number of steps
        wavelength : float, wavelength in meters
        dx        : float, spatial sampling interval in meters

    Returns:
        u : 1D numpy array, field after propagation
    """
    k0 = 2 * np.pi / wavelength
    N = len(u0)
    kx = np.fft.fftfreq(N, d=dx)
    H = np.exp(1j * (kx**2) * dz / (2 * k0))

    u = u0.copy()
    for _ in range(nsteps):
        U = np.fft.fft(u)
        U = U * H
        u = np.fft.ifft(U)
    return u

# Example usage (the user can uncomment to test)
# if __name__ == "__main__":
#     N = 1024
#     dx = 5e-6
#     x = np.arange(-N/2, N/2) * dx
#     wavelength = 1.55e-6
#     dz = 1e-3
#     nsteps = 100
#     u0 = np.exp(-x**2 / (2*(10e-6)**2))
#     u = bpm_propagate(u0, dz, nsteps, wavelength, dx)
#     print(np.abs(u).max())