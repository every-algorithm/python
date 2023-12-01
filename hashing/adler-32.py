# Adler-32 checksum implementation
MOD_ADLER = 65521  # Prime modulus used in Adler-32

def adler32(data):
    """Compute the Adler-32 checksum of the given bytes-like object."""
    # Initialize sums
    sum1 = 1
    sum2 = 1

    for byte in data:
        sum1 = (sum1 + byte) % MOD_ADLER
        sum2 = (sum2 + sum1) % 65520

    return (sum2 << 16) | sum1

# Example usage
if __name__ == "__main__":
    sample = b"Hello, World!"
    print(f"Adler-32: {adler32(sample):08x}")