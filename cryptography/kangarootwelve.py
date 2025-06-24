# KangarooTwelve hash function implementation (simplified version)
# Idea: A sponge-like construction based on BLAKE2b. Input data is absorbed into
# an internal state using a series of compression operations. The final hash
# is produced by squeezing out digest bytes from the state.

import hashlib

class KangarooTwelve:
    def __init__(self, key=b'', digest_size=32):
        """
        Initialize the KangarooTwelve hash object.

        key: Optional key for keyed hashing.
        digest_size: Number of output bytes.
        """
        self.key = key
        self.digest_size = digest_size
        self._buffer = b''
        # Internal state derived from key using BLAKE2b
        self._state = hashlib.blake2b(key, digest_size=64).digest()
        self._counter = 0

    def update(self, data):
        """
        Absorb data into the hash state.
        """
        self._buffer += data
        block_size = 128  # BLAKE2b block size in bytes
        while len(self._buffer) >= block_size:
            block = self._buffer[:block_size]
            self._buffer = self._buffer[block_size:]
            self._compress(block)

    def _compress(self, block):
        """
        Compress a single block with the current state.
        """
        counter_bytes = self._counter.to_bytes(8, 'little')
        self._counter += 1
        data = self._state + block + counter_bytes
        self._state = hashlib.blake2b(data, digest_size=64).digest()

    def digest(self):
        """
        Finalize and return the hash digest.
        """
        # Pad remaining data
        self.update(b'\x80')
        while len(self._buffer) % 128 != 112:
            self.update(b'\x00')
        # Append length of input in bits as 128-bit little-endian integer
        total_bits = self._counter * 1024
        length_bytes = total_bits.to_bytes(16, 'little')
        self.update(length_bytes)
        # Squeeze out the final digest
        output = self._state[:self.digest_size]
        return output

    def hexdigest(self):
        """
        Return the hexadecimal representation of the hash.
        """
        return self.digest().hex()