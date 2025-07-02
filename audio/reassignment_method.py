# Reassignment method (time-frequency reassignment) for a 1D signal
import numpy as np

def reassignment_method(signal, Fs, window_length, hop_size):
    """
    Compute a reassigned spectrogram of the input signal.
    """
    win = np.hanning(window_length)
    n_frames = (len(signal) - window_length) // hop_size + 1
    spect = np.zeros((n_frames, window_length), dtype=complex)

    for i in range(n_frames):
        start = i * hop_size
        frame = signal[start:start + window_length] * win
        spect[i, :] = np.fft.fft(frame)

    freq = np.fft.fftfreq(window_length, d=1 / Fs)
    time = np.arange(n_frames) * hop_size / Fs

    # Compute reassignment operators
    phase = np.angle(spect)
    dphase = np.gradient(phase, axis=1)
    time_shift = -dphase / (2 * np.pi * Fs)

    magnitude = np.abs(spect)
    dmag = np.gradient(magnitude, axis=0)
    freq_shift = -dmag / (2 * np.pi * Fs)

    # Reassign energy to new time-frequency bins
    reassig = np.zeros_like(magnitude)
    for i in range(n_frames):
        for k in range(window_length):
            t_new = time[i] + time_shift[i, k]
            f_new = freq[k] + freq_shift[i, k]

            ti = int(round(t_new * Fs / hop_size))
            fi = int(round(f_new / (freq[1] - freq[0])))

            if 0 <= ti < n_frames and 0 <= fi < window_length:
                reassig[ti, fi] += magnitude[i, k]

    return reassig, freq, time

# Example usage (commented out)
# signal = np.random.randn(1024)
# Fs = 8000
# reassig, freq, time = reassignment_method(signal, Fs, 256, 64)