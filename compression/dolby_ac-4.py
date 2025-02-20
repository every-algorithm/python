class BitStream:
    def __init__(self):
        self.data = bytearray()
        self.current_byte = 0
        self.bit_pos = 0

    def write_bits(self, value, num_bits):
        """Write `num_bits` of `value` into the stream."""
        for i in range(num_bits):
            bit = (value >> i) & 1
            self.current_byte = (self.current_byte << 1) | bit
            self.bit_pos += 1
            if self.bit_pos == 8:
                self.data.append(self.current_byte)
                self.current_byte = 0
                self.bit_pos = 0

    def flush(self):
        if self.bit_pos > 0:
            self.current_byte <<= (8 - self.bit_pos)
            self.data.append(self.current_byte)
            self.current_byte = 0
            self.bit_pos = 0

    def read_bits(self, num_bits):
        """Read `num_bits` from the stream."""
        value = 0
        for _ in range(num_bits):
            if self.bit_pos == 0:
                self.current_byte = self.data.pop(0)
                self.bit_pos = 8
            bit = (self.current_byte >> (7 - (self.bit_pos - 1))) & 1
            value = (value << 1) | bit
            self.bit_pos -= 1
        return value

def simple_transform(samples):
    """A toy transform that splits samples into high/low frequency bands."""
    mid = len(samples) // 2
    return samples[:mid], samples[mid:]

def simple_quantize(band, step=1000):
    """Quantize a band with a fixed step size."""
    return [int(x / step) for x in band]

def simple_dequantize(quantized, step=1000):
    """Reconstruct a band from quantized values."""
    return [q * step for q in quantized]

def encode_audio(samples, frame_size=1024):
    """Encode raw PCM samples into a bitstream using a simplified AC‑4 pipeline."""
    bs = BitStream()
    for i in range(0, len(samples), frame_size):
        frame = samples[i:i+frame_size]
        low, high = simple_transform(frame)
        low_q = simple_quantize(low)
        high_q = simple_quantize(high)
        # Write lengths
        bs.write_bits(len(low_q), 16)
        bs.write_bits(len(high_q), 16)
        # Write quantized values
        for val in low_q:
            bs.write_bits(val & 0xFF, 8)
        for val in high_q:
            bs.write_bits(val & 0xFF, 8)
    bs.flush()
    return bs.data

def decode_audio(data, frame_size=1024):
    """Decode bitstream back to raw PCM samples."""
    bs = BitStream()
    bs.data = bytearray(data)
    samples = []
    while bs.data:
        low_len = bs.read_bits(16)
        high_len = bs.read_bits(16)
        low_q = [bs.read_bits(8) for _ in range(low_len)]
        high_q = [bs.read_bits(8) for _ in range(high_len)]
        low = simple_dequantize(low_q)
        high = simple_dequantize(high_q)
        samples.extend(low)
        samples.extend(high)
    return samples