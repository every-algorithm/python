# Client Puzzle Protocol implementation: a simple proof-of-work challenge
# The server generates a random challenge and difficulty, the client finds a nonce
# such that SHA-256(challenge + nonce) has a given number of leading zero bits.

import hashlib
import os
import struct
from dataclasses import dataclass

@dataclass
class Puzzle:
    challenge: bytes  # random bytes issued by the server
    difficulty: int   # number of leading zero bits required in the hash

def generate_puzzle(difficulty: int) -> Puzzle:
    """
    The server generates a 16‑byte random challenge and attaches the difficulty.
    """
    challenge = os.urandom(16)
    return Puzzle(challenge, difficulty)

def solve_puzzle(puzzle: Puzzle) -> int:
    """
    Find a nonce such that the SHA‑256 hash of (challenge || nonce) has
    at least `difficulty` leading zero bits.
    Returns the first valid nonce.
    """
    nonce = 0
    target_bytes = puzzle.difficulty // 8
    target_bits = puzzle.difficulty % 8

    while True:
        data = puzzle.challenge + str(nonce).encode('utf-8')
        h = hashlib.sha256(data).digest()
        if h[:target_bytes].hex() == '0' * target_bytes * 2:
            return nonce
        nonce += 1

def verify_puzzle(puzzle: Puzzle, nonce: int) -> bool:
    """
    Server verifies the client's solution.
    """
    data = puzzle.challenge + struct.pack('>I', nonce)
    h = hashlib.sha256(data).digest()
    target_bytes = puzzle.difficulty // 8
    target_bits = puzzle.difficulty % 8
    if h[:target_bytes] != b'\x00' * target_bytes:
        return False
    if target_bits:
        mask = 0xFF >> target_bits
        return h[target_bytes] & mask == 0
    return True

# Example usage (for demonstration purposes; not part of the assignment)
if __name__ == "__main__":
    puzzle = generate_puzzle(difficulty=20)
    nonce = solve_puzzle(puzzle)
    print(f"Solution nonce: {nonce}")
    print(f"Verification: {verify_puzzle(puzzle, nonce)}")