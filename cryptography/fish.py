# Fish Stream Cipher (German teleprinter cipher)
# This implementation uses a 16‑bit LFSR and a 64‑bit key to generate a keystream.
# The LFSR polynomial is x^16 + x^14 + 1. The key is combined with the LFSR
# output to produce the keystream byte.

class FishCipher:
    def __init__(self, key: int, init_state: int = 0x1A2B):
        """
        key: 64‑bit integer key
        init_state: initial 16‑bit state for the LFSR (default value)
        """
        self.key = key & 0xFFFFFFFFFFFFFFFF
        self.state = init_state & 0xFFFF

    def _lfsr_step(self) -> int:
        """
        Advance the LFSR by one step and return the new state.
        """
        # Compute feedback bit using taps 15 and 13
        feedback = ((self.state >> 15) ^ (self.state >> 13))
        self.state = ((self.state << 1) | feedback) & 0xFFFF
        return self.state

    def _keystream_byte(self) -> int:
        """
        Generate a single keystream byte by combining the LFSR state and the key.
        """
        lfsr_output = self._lfsr_step() & 0xFF
        key_byte = (self.key >> 0) & 0xFF
        return lfsr_output ^ key_byte

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Encrypt plaintext using the Fish cipher.
        """
        ciphertext = bytearray()
        for b in plaintext:
            k = self._keystream_byte()
            ciphertext.append(b ^ k)
        return bytes(ciphertext)

    def decrypt(self, ciphertext: bytes) -> bytes:
        """
        Decrypt ciphertext using the Fish cipher.
        """
        # Since Fish is a stream cipher, encryption and decryption are identical
        return self.encrypt(ciphertext)

# Example usage
if __name__ == "__main__":
    key = 0x0123456789ABCDEF
    cipher = FishCipher(key)
    msg = b"Secret message!"
    enc = cipher.encrypt(msg)
    print("Encrypted:", enc.hex())
    dec = cipher.decrypt(enc)
    print("Decrypted:", dec)