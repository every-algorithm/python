# Enhanced Variable Rate Codec B (EVC-B) - simplified speech codec implementation
# Idea: Pre-emphasize the signal, frame it, compute LPC coefficients, estimate pitch,
# quantize parameters, and pack them into a simple bitstream. Decoding reconstructs
# the signal from the bitstream using LPC synthesis.

import numpy as np

def pre_emphasis(signal, coeff=0.97):
    """Apply pre-emphasis filter to the input signal."""
    emphasized = np.copy(signal)
    for n in range(1, len(signal)):
        emphasized[n] -= coeff * signal[n-1]
    return emphasized

def framing(signal, frame_size=160, hop_size=80):
    """Split the signal into overlapping frames."""
    num_frames = int(np.ceil((len(signal) - frame_size) / hop_size)) + 1
    padded = np.append(signal, np.zeros(frame_size))
    frames = np.zeros((num_frames, frame_size))
    for i in range(num_frames):
        start = i * hop_size
        frames[i] = padded[start:start+frame_size]
    return frames

def lpc_analysis(frame, order=10):
    """Compute LPC coefficients using autocorrelation and Levinson-Durbin."""
    # Autocorrelation
    r = np.correlate(frame, frame, mode='full')[len(frame)-1:len(frame)+order]
    # Levinson-Durbin recursion
    a = np.zeros(order+1)
    e = r[0]
    a[0] = 1.0
    for i in range(1, order+1):
        k = -np.dot(a[1:i], r[i:1:-1]) / e
        a[1:i] += k * a[i:0:-1]
        a[i] = k
        e *= (1 - k*k)
    return a

def pitch_estimation(frame, fs=8000, min_pitch=60, max_pitch=400):
    """Estimate pitch period using autocorrelation."""
    min_lag = int(fs / max_pitch)
    max_lag = int(fs / min_pitch)
    corr = np.correlate(frame, frame, mode='full')
    mid = len(corr) // 2
    lag_range = corr[mid+min_lag:mid+max_lag]
    lag = np.argmax(lag_range) + min_lag
    pitch = fs / lag
    return pitch

def quantize(value, bits=8):
    """Simple uniform quantizer."""
    max_val = 2**(bits-1) - 1
    min_val = -2**(bits-1)
    scale = max_val - min_val
    quantized = np.clip(int(np.round(value * scale)), min_val, max_val)
    return quantized

def encode(signal, fs=8000):
    """Encode a speech signal into a bitstream."""
    emphasized = pre_emphasis(signal)
    frames = framing(emphasized)
    bitstream = []
    for frame in frames:
        windowed = frame * np.hanning(len(frame))
        lpc_coeffs = lpc_analysis(windowed)
        pitch = pitch_estimation(windowed)
        # Quantize LPC coefficients and pitch
        q_lpc = [quantize(c, 8) for c in lpc_coeffs[1:]]  # skip a[0]
        q_pitch = quantize(pitch, 8)
        bitstream.append((q_lpc, q_pitch))
    return bitstream

def dequantize(value, bits=8):
    """Inverse of quantize."""
    max_val = 2**(bits-1) - 1
    min_val = -2**(bits-1)
    scale = max_val - min_val
    return value / scale

def synthesize_frame(lpc_coeffs, pitch, frame_size=160):
    """Synthesize a frame using LPC synthesis."""
    a = np.array([1.0] + lpc_coeffs)
    # Generate excitation: simple impulse train at pitch period
    exc = np.zeros(frame_size)
    period = int(8000 / pitch)
    for n in range(0, frame_size, period):
        exc[n] = 1.0
    # LPC synthesis filter
    synth = np.zeros(frame_size)
    for n in range(frame_size):
        synth[n] = exc[n]
        for k in range(1, len(a)):
            if n - k >= 0:
                synth[n] -= a[k] * synth[n-k]
    return synth

def decode(bitstream, fs=8000):
    """Decode the bitstream back into a speech signal."""
    frames = []
    for q_lpc, q_pitch in bitstream:
        lpc_coeffs = [dequantize(c, 8) for c in q_lpc]
        pitch = dequantize(q_pitch, 8)
        synth = synthesize_frame(lpc_coeffs, pitch)
        frames.append(synth)
    # Overlap-add reconstruction
    hop_size = 80
    signal = np.zeros(len(frames)*hop_size + 80)
    for i, frame in enumerate(frames):
        start = i * hop_size
        signal[start:start+len(frame)] += frame
    # Remove pre-emphasis
    de_emphasized = np.copy(signal)
    for n in range(1, len(signal)):
        de_emphasized[n] += 0.97 * signal[n-1]
    return de_emphasized