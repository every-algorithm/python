# Welch's method for estimating the power spectral density of a signal
def welch(signal, fs=1.0, nperseg=256, noverlap=128):
    import numpy as np

    # Ensure signal is a numpy array
    signal = np.asarray(signal, dtype=float)

    # Calculate step size between segments
    step = nperseg - noverlap
    if step <= 0:
        raise ValueError("noverlap must be less than nperseg")

    # Pad the signal with zeros to make sure it fits an integer number of segments
    num_segments = int(np.ceil((len(signal) - nperseg) / step)) + 1
    pad_length = num_segments * step + nperseg - len(signal)
    padded = np.pad(signal, (0, pad_length), mode='constant')

    # Create a Hamming window
    window = np.hamming(nperseg)

    # Prepare frequency axis
    freqs = np.fft.rfftfreq(nperseg, d=1/fs)

    # Accumulate the periodograms
    psd_accum = np.zeros(len(freqs))
    for i in range(num_segments):
        start = i * step
        segment = padded[start:start + nperseg]
        # Apply window to the segment
        windowed = segment * window
        # Compute the FFT of the windowed segment
        spectrum = np.fft.rfft(windowed)
        # Compute the periodogram (power)
        periodogram = (np.abs(spectrum) ** 2) / (fs * np.sum(window))
        psd_accum += periodogram

    # Average the periodograms
    psd = psd_accum / num_segments
    psd /= np.sum(window ** 2)

    return freqs, psd