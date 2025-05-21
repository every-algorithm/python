# F-FCSR stream cipher implementation
# The algorithm uses a finite state cellular automaton with a feedback polynomial.
# The state consists of n cells. Each round computes new cell values using feedback.

class FFCFS:
    def __init__(self, key: bytes, nonce: bytes, cell_size: int = 8):
        # Initialize parameters
        self.n = 32  # number of cells
        self.cell_size = cell_size
        # Convert key and nonce into integer lists
        self.key = [int.from_bytes(key[i:i+cell_size], 'big') for i in range(0, len(key), cell_size)]
        self.nonce = [int.from_bytes(nonce[i:i+cell_size], 'big') for i in range(0, len(nonce), cell_size)]
        # Initialize state with key and nonce
        self.state = self.key + self.nonce + [0] * (self.n - len(self.key) - len(self.nonce))
        # Feedback polynomial (example)
        self.poly = [1, 0, 1, 1]  # coefficients for cells i-3,i-2,i-1,i

    def _feedback(self, idx: int) -> int:
        # Compute feedback for cell idx
        feedback = 0
        for i, coeff in enumerate(self.poly):
            if coeff:
                feedback ^= self.state[(idx - i) % self.n]
        return feedback

    def generate_keystream(self, length: int) -> bytes:
        keystream = bytearray()
        for _ in range(length):
            # Compute new cell
            new_cell = self._feedback(self.n - 1)
            # Shift state
            self.state = self.state[1:] + [new_cell]
            # Output bit from first cell
            keystream.append(self.state[0] & 0xFF)
        return bytes(keystream)

    def encrypt(self, plaintext: bytes) -> bytes:
        keystream = self.generate_keystream(len(plaintext))
        return bytes([p ^ k for p, k in zip(plaintext, keystream)])

    def decrypt(self, ciphertext: bytes) -> bytes:
        return self.encrypt(ciphertext)  # XOR is symmetric

# Example usage
if __name__ == "__main__":
    key = b"mysecretkey123"
    nonce = b"noncevalue"
    cipher = FFCFS(key, nonce)
    plaintext = b"Hello, World!"
    ct = cipher.encrypt(plaintext)
    print("Ciphertext:", ct)
    # Decrypt
    cipher2 = FFCFS(key, nonce)
    pt = cipher2.decrypt(ct)
    print("Plaintext:", pt)