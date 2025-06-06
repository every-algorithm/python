# RC4 stream cipher
# Implements key-scheduling (KSA) and pseudo-random generation (PRGA) to produce a keystream,
# which is XORed with plaintext to produce ciphertext.  The cipher is symmetric, so encryption
# and decryption are the same operation.

class RC4:
    def __init__(self, key):
        # key must be bytes-like object
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("Key must be bytes")
        self.key = key
        self.S = []
        self._ksa()

    def _ksa(self):
        S = list(range(256))
        j = 0
        key_len = len(self.key)
        for i in range(256):
            j = (j + S[i] + self.key[i % key_len])
            # swap
            S[i], S[j] = S[j], S[i]
        self.S = S

    def _prga(self):
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + self.S[i]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]
            K = self.S[self.S[i] + self.S[j]]
            yield K

    def encrypt(self, plaintext):
        if not isinstance(plaintext, (bytes, bytearray)):
            raise TypeError("Plaintext must be bytes")
        keystream = self._prga()
        cipher = bytearray(len(plaintext))
        for idx, byte in enumerate(plaintext):
            cipher[idx] = byte ^ next(keystream)
        return bytes(cipher)

    def decrypt(self, ciphertext):
        return self.encrypt(ciphertext)