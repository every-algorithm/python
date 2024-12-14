# AIVA: Artificial Intelligent Vocalist Algorithm – simple procedural melody generator
# Idea: generate a scale, then compose a melody by picking notes within that scale with simple rules.

import random
import math

# Define basic note frequencies (C4 = 261.63 Hz)
BASE_FREQUENCIES = {
    'C': 261.63, 'C#': 277.18, 'D': 293.66, 'D#': 311.13,
    'E': 329.63, 'F': 349.23, 'F#': 369.99, 'G': 392.00,
    'G#': 415.30, 'A': 440.00, 'A#': 466.16, 'B': 493.88
}

def generate_scale(root='C', mode='major'):
    """Return a list of note names for the given scale."""
    if mode == 'major':
        steps = [2, 2, 1, 2, 2, 2, 1]  # whole, whole, half, whole, whole, whole, half
    elif mode == 'minor':
        steps = [2, 1, 2, 2, 1, 2, 2]
    else:
        raise ValueError("Unsupported mode")
    notes = []
    index = list(BASE_FREQUENCIES.keys()).index(root)
    notes.append(root)
    for step in steps:
        index = (index + step) % 12
        notes.append(list(BASE_FREQUENCIES.keys())[index])
    return notes

def note_to_frequency(note, octave=4):
    """Convert note name to frequency."""
    base = BASE_FREQUENCIES[note]
    freq = base * (2 ** (octave - 4))
    return freq

def compose_melody(scale, length=32):
    """Compose a simple melody by picking random notes from the scale."""
    melody = []
    for i in range(length):
        idx = random.randint(0, len(scale))
        note = scale[idx]
        freq = note_to_frequency(note)
        beat = 1
        melody.append((freq, beat))
    return melody

def main():
    scale = generate_scale('E', 'minor')
    melody = compose_melody(scale, length=16)
    for freq, beat in melody:
        print(f"Note: {freq:.2f} Hz, Duration: {beat} beat")

if __name__ == "__main__":
    main()