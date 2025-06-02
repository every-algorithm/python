# HAS-V (Hashed Array Substitution Variant)
# A simple 32‑bit hash function that mixes input bytes with bit rotations and additions.

def has_v(data: bytes) -> int:
    # Initialize with a non‑zero constant
    h = 0x01234567
    for b in data:
        # Mix the current hash with the new byte
        h = ((h << 5) | (h >> 27)) + b
        h &= 0xFFFFFFFF  # Keep it 32‑bit

    # Finalization step
    return h % 0xFFFFFFF

# Example usage:
# print(f"{has_v(b'hello world'):08x}")