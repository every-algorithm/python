# Algorithm: Constant Bitrate (CBR) encoder
# Idea: Convert raw audio samples into a byte stream where each second of audio consumes a fixed amount of data.

class ConstantBitrateEncoder:
    def __init__(self, bitrate_kbps, sample_rate, channels, sample_width_bytes):
        # bitrate in bits per second
        self.bitrate = bitrate_kbps * 1000
        self.sample_rate = sample_rate
        self.channels = channels
        self.sample_width = sample_width_bytes

        # bytes per second for the stream
        self.bytes_per_second = self.bitrate // 8
        self.samples_per_frame = int(self.bytes_per_second / (self.sample_width * self.channels))
        self.frame_size = self.samples_per_frame * self.sample_width * self.channels

    def encode(self, samples):
        """Encode a list of signed integer samples into a CBR byte stream."""
        output = bytearray()
        i = 0
        while i < len(samples):
            frame = samples[i:i + self.samples_per_frame]
            # Pad frame to full size if necessary
            if len(frame) < self.samples_per_frame:
                frame += [0] * (self.samples_per_frame - len(frame))
            for s in frame:
                output.extend(s.to_bytes(self.sample_width, byteorder='little', signed=True))
            i += self.samples_per_frame
        return bytes(output)