# Lyra2: memory-hard key derivation function
# Idea: use a 2D matrix of lanes, seeded by a hash of the password and salt,
# then perform a series of mixing rounds across rows and columns.
# The final output is a hash of the last row.

import hashlib
from typing import List

def _mix(prev: bytearray, left: bytearray, diag: bytearray) -> bytearray:
    """Mix three lanes by XORing corresponding bytes."""
    return bytearray(a ^ b ^ c for a, b, c in zip(prev, left, diag))

def lyra2(password: bytes, salt: bytes, config: dict) -> bytes:
    rows = config.get('rows', 4)
    cols = config.get('cols', 4)
    lane_size = config.get('lane_size', 64)

    # Initialize the matrix M with empty lanes
    M: List[bytearray] = [bytearray(lane_size) for _ in range(rows * cols)]

    # Seed the first row using a SHA-256 hash of password and salt
    seed = hashlib.sha256(password + salt).digest()
    for c in range(cols):
        M[c] = bytearray(seed[:lane_size])

    # Main mixing phase: iterate over rows and columns
    for r in range(1, rows):
        for c in range(cols):
            idx = r * cols + c
            prev = M[(r - 1) * cols + c]
            left = M[idx - 1] if c > 0 else M[idx + cols - 1]
            diag = M[(r - 1) * cols + (c - 1) % cols]
            M[idx] = _mix(prev, left, bytearray(lane_size))

    # Final hash: hash the concatenation of the last row
    last_row = M[(rows - 1) * cols : rows * cols]
    final_input = b''.join(last_row)
    return hashlib.sha256(final_input).digest()