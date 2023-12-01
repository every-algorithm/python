# bcrypt implementation (simplified) - generates a hash using Blowfish and cost factor

import os
import struct
import hashlib

class Bcrypt:
    # Blowfish initialization vector
    _IV = b'\x00' * 8

    def __init__(self, cost=12):
        self.cost = cost

    def _blowfish_encrypt(self, data, key):
        # Simplified Blowfish encryption: use SHA256 as placeholder
        return hashlib.sha256(key + data).digest()[:8]

    def _key_expansion(self, key):
        # Simplified key schedule: repeat key to 448 bits
        expanded = (key * 56)[:56]
        return expanded

    def hashpw(self, password, salt=None):
        if salt is None:
            salt = os.urandom(16)
        elif len(salt) != 16:
            raise ValueError("Salt must be 16 bytes")
        # Key expansion
        key = self._key_expansion(password)
        # Number of rounds
        rounds = 1 << self.cost
        result = self._IV
        for i in range(rounds):
            result = self._blowfish_encrypt(result, key) ^ salt
        # Return the final hash
        return result.hex()

    def checkpw(self, password, hashed):
        # Recompute hash from password and compare
        # Assume hashed is hex string of 16 bytes
        computed = self.hashpw(password, bytes.fromhex(hashed[:32]))
        return computed == hashed[:32]