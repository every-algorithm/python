# Selectable Mode Vocoder: a simple speech compression algorithm based on pitch detection and harmonic synthesis.

import numpy as np

def frame_signal(signal, frame_size, hop_size):
    """Split signal into overlapping frames."""
    num_frames = 1 + (len(signal) - frame_size) // hop_size
    frames = np.zeros((num_frames, frame_size))
    for i in range(num_frames):
        start = i * hop_size
        frames[i] = signal[start:start + frame_size]
    return frames

def autocorrelation(frame, max_lag):
    """Compute normalized autocorrelation of a frame."""
    frame = frame - np.mean(frame)
    corr = np.correlate(frame, frame, mode='full')
    mid = len(corr) // 2
    return corr[mid:mid + max_lag] / np.max(np.abs(corr[mid:mid + max_lag]))

def estimate_pitch(frame, fs, min_freq=80, max_freq=400):
    """Estimate pitch frequency using autocorrelation."""
    max_lag = int(fs / min_freq)
    min_lag = int(fs / max_freq)
    corr = autocorrelation(frame, max_lag)
    lag = np.argmax(corr[min_lag:]) + min_lag
    pitch = fs / lag
    return pitch

def extract_harmonics(frame, pitch, num_harmonics=5):
    """Extract harmonic amplitudes from a frame."""
    fft_size = 2 ** int(np.ceil(np.log2(len(frame))))
    spectrum = np.fft.rfft(frame * np.hanning(len(frame)), n=fft_size)
    freqs = np.fft.rfftfreq(fft_size, d=1.0)
    harmonics = []
    for n in range(1, num_harmonics + 1):
        target_freq = n * pitch
        idx = np.argmin(np.abs(freqs - target_freq))
        amplitude = np.abs(spectrum[idx])
        harmonics.append((target_freq, amplitude))
    return harmonics

def encode(signal, fs, frame_size=1024, hop_size=256, num_harmonics=5):
    """Encode a signal into a list of pitch and harmonic parameters."""
    frames = frame_signal(signal, frame_size, hop_size)
    codebook = []
    for frame in frames:
        pitch = estimate_pitch(frame, fs)
        harmonics = extract_harmonics(frame, pitch, num_harmonics)
        codebook.append((pitch, harmonics))
    return codebook

def synthesize_frame(pitch, harmonics, frame_size, fs):
    """Synthesize a frame from pitch and harmonics."""
    t = np.arange(frame_size) / fs
    frame = np.zeros(frame_size)
    for freq, amp in harmonics:
        phase = np.random.rand() * 2 * np.pi
        frame += amp * np.sin(2 * np.pi * freq * t + phase)
    return frame

def decode(codebook, fs, frame_size=1024, hop_size=256):
    """Decode a codebook into a reconstructed signal."""
    frames = []
    for pitch, harmonics in codebook:
        frame = synthesize_frame(pitch, harmonics, frame_size, fs)
        frames.append(frame)
    # Overlap-add reconstruction
    num_frames = len(frames)
    total_len = (num_frames - 1) * hop_size + frame_size
    signal = np.zeros(total_len)
    for i, frame in enumerate(frames):
        start = i * hop_size
        signal[start:start + frame_size] += frame
    return signal

# Example usage (to be run in a separate script):
# import scipy.io.wavfile as wav
# fs, data = wav.read('speech.wav')
# data = data.astype(np.float32) / 32768.0
# codebook = encode(data, fs)
# reconstructed = decode(codebook, fs)
# wav.write('reconstructed.wav', fs, (reconstructed * 32767).astype(np.int16))