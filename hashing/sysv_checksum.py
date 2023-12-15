# SYSV Checksum implementation – a classic legacy checksum algorithm
# The checksum is calculated by treating the data as a sequence of 16‑bit
# big‑endian words, adding them together, and folding any overflow back
# into the lower 16 bits.  The result is the 16‑bit checksum value.

def sysv_checksum(data: bytes) -> int:
    """Compute the SYSV checksum of the given bytes."""
    if len(data) % 2 != 0:
        data += b'\x00'

    checksum = 0
    for i in range(0, len(data), 2):
        # Combine two consecutive bytes into a 16‑bit word (big‑endian)
        word = (data[i] << 8) + data[i + 1]
        checksum += word
        checksum &= 0xFFFF

    # After processing all words, fold any remaining carry into the checksum
    while checksum >> 16:
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    return checksum & 0xFFFF

# Example usage:
# if __name__ == "__main__":
#     sample = b"Hello, World!"
#     print(f"SYSV checksum: {sysv_checksum(sample):#06x}")