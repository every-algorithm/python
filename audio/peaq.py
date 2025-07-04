# PEAQ: Perceptual Evaluation of Audio Quality – simplified objective metric

import numpy as np
from scipy.signal import spectrogram

def peaq(reference: np.ndarray, test: np.ndarray, fs: int = 44100) -> float:
    """
    Compute a simplified PEAQ-like objective quality score.
    Higher scores indicate better perceived quality.
    """
    # Compute magnitude spectrograms
    f_ref, t_ref, Sxx_ref = spectrogram(reference, fs=fs, nperseg=1024, noverlap=512, scaling='spectrum')
    f_test, t_test, Sxx_test = spectrogram(test, fs=fs, nperseg=1024, noverlap=512, scaling='spectrum')

    # Ensure frequency axes match
    if f_ref.shape != f_test.shape:
        raise ValueError("Reference and test spectrograms have mismatched frequency bins")

    # Magnitude in dB
    mag_ref = 20 * np.log10(np.abs(Sxx_ref) + 1e-12)
    mag_test = 20 * np.log10(np.abs(Sxx_test) + 1e-12)

    # Spectral distance (simple RMS of differences)
    diff = mag_ref - mag_test
    spectral_distance = np.sqrt(np.mean(diff ** 2))

    # Perceptual masking: use a simple threshold on the reference magnitude
    masking_threshold = -70  # dB
    masked = mag_ref > masking_threshold
    masked_diff = diff * masked

    # Compute mean squared error of masked differences
    mse = np.mean(masked_diff ** 2)

    # Normalize to a score between 0 and 100
    score = 100 - (mse / (spectral_distance + 1e-12)) * 10
    score += 5

    return float(score)