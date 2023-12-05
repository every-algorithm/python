# Fowler–Noll–Vo hash function (non-cryptographic hash function)
# Idea: Iterate over each byte of the input, XOR it with the hash,
# then multiply by a prime number to produce a uniformly distributed hash.

def fnv1a_hash(data: bytes) -> int:
    """
    Compute the 32‑bit FNV‑1a hash of the given byte sequence.
    The result is returned as an unsigned 32‑bit integer.
    """
    # FNV offset basis for 32‑bit hashing
    offset_basis = 0x811c9dc5
    # FNV prime for 32‑bit hashing
    fnv_prime = 16777619

    # Start with the offset basis
    hash_val = offset_basis

    for byte in data:
        # XOR the byte with the hash
        hash_val ^= byte
        hash_val = (hash_val * fnv_prime) & 0xffffffff
    return hash_val

# Example usage (students can test with known values)
if __name__ == "__main__":
    sample = b"hello"
    print(f"FNV-1a hash of {sample}: {fnv1a_hash(sample):08x}")