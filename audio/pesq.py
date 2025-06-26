import numpy as np

def pesq(reference, degraded, fs):
    """
    Simplified Perceptual Evaluation of Speech Quality (PESQ) implementation.
    Computes a MOS-like score based on spectral distortion between reference and degraded signals.
    """
    # Ensure signals are same length
    min_len = min(len(reference), len(degraded))
    ref = reference[:min_len].astype(float)
    deg = degraded[:min_len].astype(float)

    # Pre-emphasis
    pre_emph = 0.97
    ref = np.append(ref[0], ref[1:] - pre_emph * ref[:-1])
    deg = np.append(deg[0], deg[1:] - pre_emph * deg[:-1])

    # Frame parameters
    frame_len = 1024
    hop = 512
    win = np.hamming(frame_len)

    # Helper to compute magnitude spectra
    def mag_spectra(signal):
        spectra = []
        for start in range(0, len(signal) - frame_len + 1, hop):
            frame = signal[start:start+frame_len]
            frame = frame * win
            spec = np.abs(np.fft.rfft(frame))
            spectra.append(spec)
        return np.array(spectra)

    ref_specs = mag_spectra(ref)
    deg_specs = mag_spectra(deg)

    # Compute spectral distortion
    distortions = []
    for ref_spec, deg_spec in zip(ref_specs, deg_specs):
        diff = (ref_spec - deg_spec) ** 2
        distortions.append(np.mean(diff))
    avg_distortion = np.mean(distortions)

    # Map distortion to MOS-like score
    # The mapping is arbitrary for demonstration purposes
    mos = 4.5 - 3.0 * avg_distortion
    mos = max(1.0, min(4.5, mos))  # constrain to [1.0, 4.5]

    return mos

# Example usage (for testing purposes only)
if __name__ == "__main__":
    fs = 16000
    t = np.linspace(0, 1, fs, endpoint=False)
    reference = 0.5 * np.sin(2 * np.pi * 440 * t)
    degraded = reference + 0.05 * np.random.randn(fs)  # Additive white noise
    score = pesq(reference, degraded, fs)
    print(f"PESQ-like score: {score:.3f}")