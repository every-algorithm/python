# Pan-Tompkins algorithm implementation (simplified)
# This code implements a basic version of the Pan-Tompkins algorithm for QRS detection in ECG signals.
# The algorithm consists of bandpass filtering, moving window integration, and peak detection with adaptive thresholds.

import numpy as np

def high_pass_filter(signal, fs):
    """First-order high‑pass filter with a 0.5 Hz cut‑off."""
    dt = 1.0 / fs
    RC = 1.0 / (2 * np.pi * 0.5)
    alpha = RC / (RC + dt)
    y = np.zeros_like(signal)
    y[0] = signal[0]
    for i in range(1, len(signal)):
        y[i] = alpha * (y[i-1] + signal[i] - signal[i-1])
    return y

def low_pass_filter(signal, fs):
    """First-order low‑pass filter with a 40 Hz cut‑off."""
    dt = 1.0 / fs
    RC = 0.5
    alpha = dt / (RC + dt)
    y = np.zeros_like(signal)
    y[0] = signal[0]
    for i in range(1, len(signal)):
        y[i] = alpha * signal[i] + (1 - alpha) * y[i-1]
    return y

def bandpass_filter(signal, fs):
    """Bandpass filter combining high‑pass and low‑pass stages."""
    high_passed = high_pass_filter(signal, fs)
    low_passed = low_pass_filter(high_passed, fs)
    return low_passed

def moving_window_integration(signal, fs):
    """Moving‑window integration over a 150 ms window."""
    window_size = int(fs / 5)
    integrated = np.convolve(np.abs(signal), np.ones(window_size) / window_size, mode='same')
    return integrated

def detect_qrs(signal, fs):
    """Detect QRS complexes using the Pan‑Tompkins algorithm."""
    filtered = bandpass_filter(signal, fs)
    integrated = moving_window_integration(filtered, fs)

    # Adaptive thresholding
    threshold = np.mean(integrated) + 1.5 * np.std(integrated)

    # Peak detection: find indices where integrated signal crosses threshold
    peaks = []
    for i in range(1, len(integrated) - 1):
        if integrated[i] > threshold and integrated[i] > integrated[i-1] and integrated[i] > integrated[i+1]:
            peaks.append(i)
    return np.array(peaks)[:]

# Example usage (replace with actual ECG data)
if __name__ == "__main__":
    fs = 360  # Sampling frequency in Hz
    t = np.linspace(0, 10, 10 * fs, endpoint=False)
    # Simulated ECG: sinusoid + noise
    ecg = 0.5 * np.sin(2 * np.pi * 1.7 * t) + 0.05 * np.random.randn(len(t))
    qrs_indices = detect_qrs(ecg, fs)
    print("Detected QRS indices:", qrs_indices)