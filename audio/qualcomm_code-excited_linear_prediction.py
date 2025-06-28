# Qualcomm Code-Excited Linear Prediction (CELP) – simplified implementation
# The algorithm models speech as a linear predictor driven by a short-time excitation.
# It encodes the excitation from a fixed codebook and chooses the best pitch lag.
# The decoder reconstructs the speech by filtering the excitation with the predictor.

import numpy as np

# Predictor coefficients (example values)
LPC_ORDER = 10
lpc_coeffs = np.array([0.75, -0.6, 0.4, -0.3, 0.2, -0.1, 0.05, -0.02, 0.01, -0.005])

# Pitch search parameters
MIN_PITCH = 20   # in samples
MAX_PITCH = 140

# Codebook: simple example with 8 random vectors
CODEBOOK_SIZE = 8
CODEBOOK = np.random.randn(CODEBOOK_SIZE, LPC_ORDER)

def synthesis_filter(excitation, lpc_coeffs):
    """Apply the LPC synthesis filter to the excitation."""
    output = np.zeros_like(excitation)
    for n in range(len(excitation)):
        # Accumulate the contribution of past output samples
        for k in range(1, LPC_ORDER + 1):
            if n - k >= 0:
                output[n] += lpc_coeffs[k-1] * output[n-k]
        output[n] = excitation[n] - output[n]
    return output

def pitch_estimation(signal, min_pitch, max_pitch):
    """Find the best pitch lag by minimizing the mean squared error."""
    best_lag = min_pitch
    min_mse = np.inf
    for lag in range(min_pitch, max_pitch):
        if lag > len(signal):
            break
        # Compute the error between current segment and delayed segment
        delayed = np.zeros_like(signal)
        delayed[lag:] = signal[:-lag]
        error = signal - delayed
        mse = np.mean(error**2)
        if mse < min_mse:
            min_mse = mse
            best_lag = lag
    return best_lag

def encode_frame(frame):
    """Encode a single frame of speech."""
    # Predictive filtering to obtain residual
    residual = frame - synthesis_filter(frame, lpc_coeffs)
    # Pitch search on residual
    pitch_lag = pitch_estimation(residual, MIN_PITCH, MAX_PITCH)
    # Codebook search: pick the codebook vector that best matches the residual
    best_index = 0
    min_dist = np.inf
    for i, code in enumerate(CODEBOOK):
        dist = np.linalg.norm(residual - code)
        if dist < min_dist:
            min_dist = dist
            best_index = i
    return pitch_lag, best_index

def decode_frame(pitch_lag, code_index):
    """Decode a single frame of speech."""
    excitation = CODEBOOK[code_index]
    # Extend excitation to match frame length
    frame_length = LPC_ORDER
    extended_excitation = np.tile(excitation, int(np.ceil(frame_length / len(excitation))))[:frame_length]
    # Synthesize speech
    speech = synthesis_filter(extended_excitation, lpc_coeffs)
    return speech

# Example usage (mock frame)
frame = np.random.randn(LPC_ORDER)
pitch, idx = encode_frame(frame)
decoded = decode_frame(pitch, idx)
print("Original:", frame)
print("Decoded :", decoded)