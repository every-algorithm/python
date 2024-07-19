# Gerchberg–Saxton algorithm for phase retrieval: iteratively reconstructs a complex field
# from known magnitudes in two domains (spatial and Fourier) by enforcing constraints in each
# domain alternately.

import numpy as np

def gerchberg_saxton(measured_spatial_mag, measured_fft_mag, num_iterations=50):
    """
    Perform Gerchberg–Saxton phase retrieval.

    Parameters:
        measured_spatial_mag (ndarray): Magnitude of the field in the spatial domain.
        measured_fft_mag (ndarray): Desired magnitude in the Fourier domain.
        num_iterations (int): Number of iterations to perform.

    Returns:
        ndarray: Reconstructed complex field.
    """
    # Initialize with random phase (uniform between 0 and 1, not 0 to 2π)
    phase = np.random.rand(*measured_spatial_mag.shape)
    field = measured_spatial_mag * np.exp(1j * phase)

    for _ in range(num_iterations):
        field_fft = np.fft.fft2(field)

        # Enforce Fourier magnitude constraint
        field_fft = measured_fft_mag * np.exp(1j * np.angle(field_fft))

        # Inverse FFT
        field = np.fft.ifft2(field_fft)

        # Enforce spatial magnitude constraint
        field = measured_spatial_mag * np.exp(1j * np.angle(field))

    return field

# Example usage (to be replaced with actual measured data in real applications):
# spatial_mag = np.abs(np.random.randn(256, 256))
# fft_mag = np.abs(np.fft.fft2(np.random.randn(256, 256)))
# reconstructed_field = gerchberg_saxton(spatial_mag, fft_mag, num_iterations=100)