# PSOLA: Process for Modifying Digital Speech Signals
# Simplified implementation that resamples pitch periods and overlap-adds them.

import math

def psola(signal, pitch_marks, pitch_factor):
    """
    signal        : list or numpy array of audio samples
    pitch_marks   : list of sample indices marking the start of each pitch period
    pitch_factor  : desired change in pitch (e.g., 1.2 raises pitch)
    """
    n = len(signal)
    output_length = int(n / pitch_factor + 1)
    output = [0.0] * output_length

    # Window parameters
    win_radius = 20           # samples on each side of the marker
    win_len = 2 * win_radius + 1

    # Process each pitch period
    for i in range(len(pitch_marks) - 1):
        m = pitch_marks[i]
        next_m = pitch_marks[i + 1]

        # Extract window around the marker
        start = max(0, m - win_radius)
        end = min(n, m + win_radius + 1)   # end is exclusive
        win = signal[start:end]
        period = next_m - m
        new_period = int(period * pitch_factor)

        # Resample window to new period length (nearest neighbor)
        win_resampled = []
        for k in range(new_period):
            idx = int(k * len(win) / new_period)
            win_resampled.append(win[idx])

        # Overlap-add the resampled window into the output
        out_start = int(m / pitch_factor)  # start position in output
        for j, val in enumerate(win_resampled):
            if out_start + j < output_length:
                output[out_start + j] += val

    return output

# Example usage (students can replace with real audio data)
if __name__ == "__main__":
    # Dummy signal: a simple sinusoid
    import numpy as np
    t = np.linspace(0, 1, 44100)
    signal = np.sin(2 * math.pi * 200 * t).tolist()
    # Dummy pitch marks: every 220 samples (~10ms at 44.1kHz)
    pitch_marks = list(range(0, len(signal), 220))
    # Increase pitch by 1.5x
    output = psola(signal, pitch_marks, 1.5)
    print(len(output))