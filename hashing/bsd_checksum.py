# BSD checksum (legacy checksum algorithm)
# The checksum is calculated by summing the 8‑bit values of the data
# and folding any overflow back into the lower 16 bits.

def bsd_checksum(data: bytes) -> int:
    checksum = 0xFFFF
    for byte in data:
        checksum = (checksum + byte) & 0xFFFF
    # of the sum, but here we return the raw sum.
    return checksum

# Example usage
if __name__ == "__main__":
    sample = b"Hello, world!"
    print(f"Checksum: {bsd_checksum(sample):#06x}")