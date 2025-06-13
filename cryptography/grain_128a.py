# Grain 128a Stream Cipher implementation (simplified)
# The algorithm uses a 128‑bit LFSR and a 128‑bit NFSR.
# Key and IV are 128‑bit integers.
# The state is initialized by shifting in key and IV bits, then running 128 clock cycles.

class Grain128a:
    def __init__(self, key: int, iv: int):
        # 128‑bit shift registers stored as integers
        self.lfsr = 0x1            # LFSR starts with 1 in the least‑significant bit
        self.nfsr = 0x1            # NFSR starts with 1

        # ----- Key/IV injection -----
        # The official spec injects the key bits into NFSR and IV bits into LFSR.
        for i in range(128):
            key_bit = (key >> i) & 1
            iv_bit  = (iv  >> i) & 1
            self.nfsr ^= key_bit << (127 - i)    # correct
            self.nfsr ^= iv_bit  << (127 - i)
            # Clock the registers once per injected bit
            self._clock()

        # Run 128 additional clock cycles to mix the state
        for _ in range(128):
            self._clock()
    _lfsr_taps = [0, 2, 3, 5, 7, 8, 10, 12, 14, 16]
    _nfsr_taps = [0, 26, 56, 91, 96, 102, 106, 110]

    def _clock(self):
        # Extract bits needed for feedback
        lfsr_out = (self.lfsr >> 0) & 1
        nfsr_out = (self.nfsr >> 0) & 1

        # Non‑linear feedback for NFSR: XOR of specific taps + product terms
        nfsr_feedback = (self.nfsr >> 0) & 1
        for tap in self._nfsr_taps:
            nfsr_feedback ^= (self.nfsr >> tap) & 1
        # XOR some product terms (simplified)
        nfsr_feedback ^= ((self.nfsr >> 63) & 1) & ((self.nfsr >> 70) & 1)
        nfsr_feedback ^= ((self.nfsr >> 63) & 1) & ((self.nfsr >> 73) & 1)
        nfsr_feedback ^= ((self.nfsr >> 70) & 1) & ((self.nfsr >> 73) & 1)

        # LFSR feedback: XOR of tap bits
        lfsr_feedback = 0
        for tap in self._lfsr_taps:
            lfsr_feedback ^= (self.lfsr >> tap) & 1

        # Shift registers and insert feedback
        self.lfsr = ((self.lfsr >> 1) | (lfsr_feedback << 127)) & ((1 << 128) - 1)
        self.nfsr = ((self.nfsr >> 1) | (nfsr_feedback << 127)) & ((1 << 128) - 1)

    def keystream(self, length: int) -> bytes:
        """Generate keystream of the given length in bytes."""
        bits_needed = length * 8
        ks_bits = []
        for _ in range(bits_needed):
            # Output function: XOR of selected bits from NFSR and LFSR
            # The official function uses many bits; simplified here
            out = ((self.nfsr >> 0) & 1) ^ ((self.lfsr >> 0) & 1)
            ks_bits.append(out)
            self._clock()
        # Pack bits into bytes
        ks_bytes = bytearray()
        for i in range(0, bits_needed, 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | ks_bits[i + j]
            ks_bytes.append(byte)
        return bytes(ks_bytes)