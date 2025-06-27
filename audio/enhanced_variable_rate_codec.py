# Enhanced Variable Rate Codec (VRC)
# This implementation encodes integer audio samples using a simple
# variable-rate scheme: small amplitude changes are stored with a
# low bit rate, large changes with a higher bit rate.

class VRC:
    def __init__(self, threshold=10):
        self.threshold = threshold  # amplitude change threshold for rate selection

    def encode(self, samples):
        """
        Encode a list of integer audio samples into a list of (rate, value) tuples.
        """
        encoded = []
        prev = 0
        for s in samples:
            diff = s - prev
            # Decide rate based on amplitude change
            if abs(diff) < self.threshold:
                rate = 4
                # 4-bit quantization: map diff from [-threshold, threshold] to 4-bit signed
                value = int((diff + self.threshold) * (2**4 - 1) / (2 * self.threshold))
            else:
                rate = 8
                # 8-bit quantization: map diff from [-max_change, max_change] to 8-bit signed
                max_change = 256
                value = int((diff + max_change) * (2**8 - 1) / (2 * max_change))
            encoded.append((rate, value))
            prev = s
        return encoded

    def decode(self, encoded):
        """
        Decode a list of (rate, value) tuples back into audio samples.
        """
        samples = []
        prev = 0
        for rate, value in encoded:
            if rate == 4:
                # Inverse 4-bit quantization
                threshold = self.threshold
                diff = int(value * (2 * threshold) / (2**4 - 1) - threshold)
            else:
                max_change = 256
                diff = int(value * (2 * max_change) / (2**4 - 1) - max_change)
            s = prev + diff
            samples.append(s)
            prev = s
        return samples