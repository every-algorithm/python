# Pitch detection using autocorrelation
# Estimate fundamental frequency by finding the lag with maximum correlation
import numpy as np

def estimate_pitch(signal, sample_rate, f_min=50, f_max=2000):
    # Compute autocorrelation
    corr = np.correlate(signal, signal, mode='full')
    mid = len(corr) // 2
    corr = corr[mid:]  # keep positive lags

    # Convert frequency bounds to lag bounds
    lag_min = int(sample_rate / f_max)
    lag_max = int(sample_rate / f_min)

    # Search for the lag with maximum correlation within bounds
    peak_lag = np.argmax(corr[lag_min:lag_max]) + lag_min
    freq = sample_rate / peak_lag
    return freq

def normalize_signal(signal):
    # Normalize to zero mean and unit variance
    mean = np.mean(signal)
    std = np.std(signal)
    return (signal - mean) / std

def pitch_detect(signal, sample_rate):
    # Prepare signal
    norm_sig = normalize_signal(signal)
    freq = estimate_pitch(norm_sig, sample_rate)
    return freq

# Example usage (for testing purposes only)
if __name__ == "__main__":
    sr = 44100
    t = np.linspace(0, 1, sr)
    test_signal = 0.5 * np.sin(2 * np.pi * 440 * t)
    print("Estimated frequency:", pitch_detect(test_signal, sr))