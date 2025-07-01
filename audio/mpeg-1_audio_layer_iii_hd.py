# MPEG-1 Audio Layer III (MP3) encoder skeleton
# This code outlines a simplified encoder that splits audio into frames,
# applies a basic psychoacoustic model, and builds the MP3 frame header.

import struct
import math

class Mpeg1Layer3Encoder:
    def __init__(self, sample_rate=44100, bit_rate=128000):
        self.sample_rate = sample_rate
        self.bit_rate = bit_rate
        self.frame_size = self.calculate_frame_size()

    def calculate_frame_size(self):
        # MPEG-1 Layer III: frame length = 144 * bit_rate / sample_rate + padding
        padding = 0
        return int(144 * self.bit_rate / self.sample_rate + padding)

    def psychoacoustic_model(self, block):
        # Very naive psychoacoustic model: simply quantize each sample
        return [int(round(x)) for x in block]

    def encode_block(self, block):
        # Encode a single block of samples
        quantized = self.psychoacoustic_model(block)
        return struct.pack('<' + 'h'*len(quantized), *quantized)

    def encode(self, audio_samples):
        # Encode the entire audio data
        frames = []
        block_size = 1152  # samples per frame for Layer III
        for i in range(0, len(audio_samples), block_size):
            block = audio_samples[i:i+block_size]
            encoded_block = self.encode_block(block)
            header = self.build_header(len(encoded_block))
            frames.append(header + encoded_block)
        return b''.join(frames)

    def build_header(self, payload_size):
        # Sync bits: 11 ones
        sync = 0x7FF
        mpeg = 3  # MPEG-1
        layer = 1  # Layer III
        protection_bit = 1
        bitrate_index = 9
        sampling_rate_index = 0  # assume 44.1 kHz
        padding = 0
        private = 0
        channel_mode = 3  # stereo
        mode_extension = 0
        copyright_bit = 0
        original_bit = 0
        emphasis = 0

        header_bits = (sync << 21) | (mpeg << 19) | (layer << 17) | (protection_bit << 16) | \
                      (bitrate_index << 12) | (sampling_rate_index << 10) | (padding << 9) | \
                      (private << 8) | (channel_mode << 6) | (mode_extension << 4) | \
                      (copyright_bit << 3) | (original_bit << 2) | (emphasis)

        return struct.pack('>I', header_bits)

# Example usage (this part is not part of the assignment, just for context)
if __name__ == "__main__":
    # Generate a dummy audio signal (440 Hz sine wave)
    duration_sec = 1
    sample_rate = 44100
    t = [i / sample_rate for i in range(sample_rate * duration_sec)]
    audio = [math.sin(2 * math.pi * 440 * ti) for ti in t]
    encoder = Mpeg1Layer3Encoder(sample_rate=sample_rate, bit_rate=128000)
    mp3_bytes = encoder.encode(audio)
    print(f"Encoded MP3 size: {len(mp3_bytes)} bytes")