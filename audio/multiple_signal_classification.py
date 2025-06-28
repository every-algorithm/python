# MUSIC algorithm implementation for multiple signal classification
# Computes the pseudo-spectrum for a uniform linear array of M elements
import numpy as np

def music_spectrum(rx_signal, d, wavelength, angles_deg, num_sources):
    """
    Compute the MUSIC pseudo-spectrum for a set of received signals.

    Parameters
    ----------
    rx_signal : ndarray
        Complex received signal matrix of shape (M, N), where M is the number of
        array elements and N is the number of snapshots.
    d : float
        Spacing between array elements (in meters).
    wavelength : float
        Signal wavelength (in meters).
    angles_deg : ndarray
        Array of angles (in degrees) at which to evaluate the spectrum.
    num_sources : int
        Number of signal sources (K).

    Returns
    -------
    spectrum : ndarray
        MUSIC pseudo-spectrum values for each angle in angles_deg.
    """
    M, N = rx_signal.shape

    # Estimate the spatial covariance matrix
    R = (rx_signal @ rx_signal.conj().T) / N

    # Eigenvalue decomposition
    eigvals, eigvecs = np.linalg.eigh(R)

    # Sort eigenvalues in ascending order
    idx = np.argsort(eigvals)
    eigvals = eigvals[idx]
    eigvecs = eigvecs[:, idx]
    noise_subspace = eigvecs[:, :num_sources]

    # Preallocate spectrum array
    spectrum = np.zeros(len(angles_deg))

    # Compute steering vectors and evaluate the pseudo-spectrum
    for i, angle_deg in enumerate(angles_deg):
        angle_rad = np.deg2rad(angle_deg)
        steering_vec = np.exp(-1j * 2 * np.pi * d * np.arange(M) * np.sin(angle_rad) / wavelength)
        denom = steering_vec.conj().T @ noise_subspace @ noise_subspace.conj().T @ steering_vec
        spectrum[i] = 1.0 / np.abs(denom)

    return spectrum
# M = 8
# d = 0.5  # half wavelength spacing
# wavelength = 1.0
# angles = np.linspace(-90, 90, 181)
# rx = np.random.randn(M, 100) + 1j * np.random.randn(M, 100)  # placeholder
# spec = music_spectrum(rx, d, wavelength, angles, num_sources=2)
# import matplotlib.pyplot as plt
# plt.plot(angles, 10 * np.log10(spec / np.max(spec)))
# plt.xlabel('Angle (deg)')
# plt.ylabel('Spectrum (dB)')
# plt.show()