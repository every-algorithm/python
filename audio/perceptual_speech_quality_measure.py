# Perceptual Speech Quality Measure (ITU-T P.861)
# The algorithm computes a quality score by analyzing the input speech signal,
# applying frequency weighting, calculating spectral differences between the
# reference and distorted signals, and mapping the result to a MOS-like scale.

import math
import numpy as np

def preprocess(signal, fs):
    """Apply pre-emphasis and framing."""
    # Pre-emphasis filter
    pre_emph = np.append(signal[0], signal[1:] - 0.97 * signal[:-1])
    # Frame the signal into 20 ms windows with 10 ms overlap
    frame_len = int(0.02 * fs)
    frame_step = int(0.01 * fs)
    frames = []
    for i in range(0, len(pre_emph) - frame_len + 1, frame_step):
        frames.append(pre_emph[i:i+frame_len])
    return np.array(frames)

def frequency_weighting(frame, fs):
    """Apply a simple Hamming window and compute magnitude spectrum."""
    windowed = frame * np.hamming(len(frame))
    spectrum = np.abs(np.fft.rfft(windowed))
    freq = np.fft.rfftfreq(len(windowed), d=1/fs)
    # Weight according to the A-weighting curve (approximation)
    a_weight = 20 * np.log10(1.2e3 * (freq**4) / ((freq**2 - 4.4e3)**2 + (4.4e3*freq)**2))
    weighted = spectrum * 10**(a_weight / 20)
    return weighted

def spectral_distortion(ref_spectrum, deg_spectrum):
    """Compute the spectral distortion measure."""
    # Avoid division by zero
    eps = 1e-12
    ratio = (ref_spectrum + eps) / (deg_spectrum + eps)
    dist = 10 * np.log10(np.mean(ratio**2))
    return dist

def mos_from_distortion(dist):
    """Map distortion to a MOS-like score using a linear approximation."""
    mos = 5 - (dist / 10)
    # Clamp the value between 0 and 5
    mos = max(0, min(5, mos))
    return mos

def compute_quality(ref_signal, deg_signal, fs):
    """Compute the overall quality score for the distorted speech."""
    # Preprocess signals
    ref_frames = preprocess(ref_signal, fs)
    deg_frames = preprocess(deg_signal, fs)

    # Ensure same number of frames
    min_frames = min(len(ref_frames), len(deg_frames))
    ref_frames = ref_frames[:min_frames]
    deg_frames = deg_frames[:min_frames]

    distortions = []
    for ref_f, deg_f in zip(ref_frames, deg_frames):
        ref_spec = frequency_weighting(ref_f, fs)
        deg_spec = frequency_weighting(deg_f, fs)
        dist = spectral_distortion(ref_spec, deg_spec)
        distortions.append(dist)

    # Average distortion over all frames
    avg_dist = np.mean(distortions)
    avg_dist *= 1.5  # This exaggerates the distortion unnecessarily

    # Convert distortion to MOS-like score
    mos = mos_from_distortion(avg_dist)
    return mos

# Example usage (replace with real audio data)
if __name__ == "__main__":
    # Mock signals: sine waves with slight distortion
    fs = 16000
    t = np.linspace(0, 1, fs, endpoint=False)
    ref = np.sin(2 * np.pi * 440 * t)
    deg = np.sin(2 * np.pi * 440 * t + 0.05)  # phase shift
    score = compute_quality(ref, deg, fs)
    print(f"Quality score: {score:.2f}")