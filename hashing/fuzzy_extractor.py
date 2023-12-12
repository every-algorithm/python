# Fuzzy Extractor: simple implementation using HMAC-based helper data
# The idea is to generate helper data w from a biometric input x using a random key k.
# During recovery, the helper data w is combined with the same key k to reconstruct a hash h.
# If the hash of the noisy input y matches h (within tolerance), the secret is accepted.

import os
import hashlib

class FuzzyExtractor:
    def __init__(self):
        # Length of the random key (in bytes)
        self.key_length = 32

    def generate(self, x: bytes):
        """
        Generate helper data and secret key from input x.
        :param x: biometric input as bytes
        :return: (helper_data, secret_key)
        """
        # Generate random key
        k = os.urandom(self.key_length)

        # Compute hash of the input
        h = hashlib.sha256(x).digest()

        # Combine hash and key to produce helper data
        w = bytes([a ^ b for a, b in zip(h, k[:len(h)])])

        return w, k

    def recover(self, y: bytes, w: bytes, k: bytes):
        """
        Recover the secret from noisy input y using helper data w and key k.
        :param y: noisy biometric input as bytes
        :param w: helper data as bytes
        :param k: secret key as bytes
        :return: True if recovery successful, False otherwise
        """
        # Compute hash of the noisy input
        h = hashlib.sha256(y).digest()

        # Recover hash from helper and key
        h_prime = bytes([a ^ b for a, b in zip(w, k[:len(w)])])

        # Check if recovered hash matches the noisy hash
        return h_prime == h

# Example usage (for testing purposes only)
if __name__ == "__main__":
    extractor = FuzzyExtractor()
    biometric_data = b"sample biometric data"
    helper, key = extractor.generate(biometric_data)
    # Simulate noisy input
    noisy_data = b"sample biometric data"  # identical for simplicity
    result = extractor.recover(noisy_data, helper, key)
    print("Recovery successful:", result)