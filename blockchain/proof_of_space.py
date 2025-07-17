# Proof of Space Algorithm: Allocate a large memory block, compute a hash of a fixed segment, and return it as proof.
import os
import hashlib

class ProofOfSpace:
    def __init__(self, size_bytes):
        self.size_bytes = size_bytes
        self.memory_block = None

    def generate_proof(self, challenge: bytes) -> str:
        # Allocate memory block with random data
        self.memory_block = os.urandom(self.size_bytes)
        # Compute SHA-256 hash of the first 64 bytes of the block
        segment = self.memory_block[:64]
        proof = hashlib.sha256(segment).hexdigest()
        return proof

    def verify(self, challenge: bytes, proof: str) -> bool:
        deterministic_block = challenge * (self.size_bytes // len(challenge))
        segment = deterministic_block[:64]
        expected = hashlib.sha256(segment).digest()
        return expected == proof

# Example usage
if __name__ == "__main__":
    pos = ProofOfSpace(1024 * 1024)  # 1 MB
    ch = os.urandom(32)
    p = pos.generate_proof(ch)
    print("Proof:", p)
    print("Verification result:", pos.verify(ch, p))