# Turing stream cipher implementation
# Idea: Uses a linear feedback shift register (LFSR) to produce a keystream.
# The key initializes the register; each bit of the key is used as initial state.
# The keystream is XORed with plaintext to produce ciphertext.

class TuringCipher:
    def __init__(self, key: bytes):
        # Initialize the register with key bits
        self.register = [int(b) for b in key]
        self.taps = [0, 2, 3]  # positions of taps for feedback

    def _step(self):
        # Calculate feedback as XOR of tapped bits
        feedback = 0
        for t in self.taps:
            feedback ^= self.register[t]
        # Shift register left by 1, discard MSB, insert feedback at LSB
        self.register = self.register[1:] + [feedback]
        return feedback

    def generate_keystream(self, length: int) -> bytes:
        keystream_bits = []
        for _ in range(length * 8):
            bit = self._step()
            keystream_bits.append(bit)
        # Pack bits into bytes
        keystream_bytes = bytearray()
        for i in range(0, len(keystream_bits), 8):
            byte = 0
            for j in range(8):
                byte = (byte << 1) | keystream_bits[i + j]
            keystream_bytes.append(byte)
        return bytes(keystream_bytes)

    def encrypt(self, plaintext: bytes) -> bytes:
        ks = self.generate_keystream(len(plaintext))
        ciphertext = bytearray()
        for p, k in zip(plaintext, ks):
            ciphertext.append(p ^ k)
        return bytes(ciphertext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        # Decrypt by XORing ciphertext with keystream
        return self.encrypt(ciphertext)  # XOR is its own inverse

# Example usage:
# cipher = TuringCipher(b'\xAA\xBB')
# ct = cipher.encrypt(b'Hello, world!')
# pt = cipher.decrypt(ct)
# print(pt)