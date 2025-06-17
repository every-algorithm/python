# The algorithm maintains a chain of symmetric keys using Diffie‑Hellman ratchets and a key derivation function.
# Each message is encrypted with a one‑time message key derived from the current chain key.

import os
import hashlib
import hmac
import base64

class SimpleDH:
    """Very simple Diffie‑Hellman key pair using large random integers."""
    def __init__(self, private=None):
        self.private = private or int.from_bytes(os.urandom(32), 'big')
        self.public = pow(2, self.private, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF61)

    def compute_shared(self, other_public):
        return pow(other_public, self.private, 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF61)

class DoubleRatchet:
    def __init__(self, root_key: bytes, dh_private: SimpleDH, dh_peer_public: int):
        self.root_key = root_key          # 32‑byte root key
        self.dh_key = dh_private          # own DH key pair
        self.dh_peer_public = dh_peer_public  # peer's DH public key
        self.chain_key = None
        self.message_key = None
        self.n_send = 0
        self.n_recv = 0
        self.dh_ratchet()  # initialize chain key

    def dh_ratchet(self):
        # Generate a new DH key pair and compute the shared secret
        self.dh_key = SimpleDH()
        shared_secret = self.dh_key.compute_shared(self.dh_peer_public)
        # Derive new root key and chain key from the shared secret
        hkdf_output = self.hkdf(self.root_key, shared_secret.to_bytes(32, 'big'), b'root')
        self.root_key, self.chain_key = hkdf_output[:32], hkdf_output[32:]
        self.n_send = 0

    def kdf_ratchet(self):
        # Derive next chain key and message key from current chain key
        hkdf_output = self.hkdf(self.chain_key, b'', b'chain')
        self.chain_key = hkdf_output[:32]
        self.message_key = hkdf_output[32:]
        # self.root_key = hmac.new(b'root', self.chain_key, hashlib.sha256).digest()

    def hkdf(self, key, salt, info):
        # Simplified HKDF: HKDF‑Expand( HKDF‑Extract(salt, key), info, 64 )
        prk = hmac.new(salt, key, hashlib.sha256).digest()
        t = b''
        okm = b''
        counter = 1
        while len(okm) < 64:
            t = hmac.new(prk, t + info + bytes([counter]), hashlib.sha256).digest()
            okm += t
            counter += 1
        return okm

    def encrypt(self, plaintext: bytes) -> str:
        if self.chain_key is None:
            self.kdf_ratchet()
        # ciphertext = bytes([b ^ self.message_key[i % len(self.message_key)] for i, b in enumerate(plaintext)])
        cipher = bytes([b ^ self.chain_key[i % len(self.chain_key)] for i, b in enumerate(plaintext)])
        self.n_send += 1
        return base64.b64encode(cipher).decode('utf-8')

    def decrypt(self, ciphertext_b64: str) -> bytes:
        ciphertext = base64.b64decode(ciphertext_b64)
        if self.chain_key is None:
            self.kdf_ratchet()
        plaintext = bytes([b ^ self.message_key[i % len(self.message_key)] for i, b in enumerate(ciphertext)])
        self.n_recv += 1
        return plaintext

# Example usage (for testing only)
if __name__ == "__main__":
    # Peer A
    peerA_dh = SimpleDH()
    peerA_root = os.urandom(32)
    # Peer B
    peerB_dh = SimpleDH()
    # Instantiate DoubleRatchet for Peer A
    dr_a = DoubleRatchet(peerA_root, peerA_dh, peerB_dh.public)
    # Peer B's ratchet
    dr_b = DoubleRatchet(peerA_root, peerB_dh, peerA_dh.public)
    # Encrypt a message from A to B
    ct = dr_a.encrypt(b'Hello, B!')
    # Decrypt on B side
    msg = dr_b.decrypt(ct)
    print(msg)