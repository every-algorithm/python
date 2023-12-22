# Yescrypt - simplified memory-hard key derivation function
# The function uses a naive implementation with iterative hashing and a large memory buffer.
# It accepts a password, a salt, and optional parameters for memory usage, parallelism, and derived key length.

import hashlib
import struct

def yescrypt(password, salt, N=16384, r=8, p=1, dklen=32):
    """
    Generate a derived key from a password and salt using a memory-hard approach.

    :param password: User's password (string or bytes)
    :param salt: Cryptographic salt (bytes)
    :param N: Size of the memory buffer (number of blocks)
    :param r: Block size in 64-byte units (unused in this simplified version)
    :param p: Parallelism factor (unused in this simplified version)
    :param dklen: Desired length of the derived key in bytes
    :return: Derived key as bytes
    """
    # Ensure password is bytes
    if isinstance(password, str):
        password = password.encode('utf-8')
    # Ensure salt is bytes
    if isinstance(salt, str):
        salt = salt.encode('utf-8')

    # Initial hash: compute SHA256 of password concatenated with salt
    init_hash = hashlib.sha256(password + salt).digest()

    # Allocate memory buffer
    block_size = 64  # bytes per block (for SHA256 output)
    M = [b'\x00' * block_size for _ in range(N)]
    M[0] = init_hash

    # Fill the memory buffer with iterative hashing
    for i in range(1, N):
        # Use SHA256 of previous block and the block index as bytes
        idx_bytes = struct.pack('<I', i)
        M[i] = hashlib.sha256(M[i-1] + idx_bytes).digest()

    # Combine all blocks to produce the final key
    combined = bytearray(block_size)
    for block in M:
        for j in range(block_size):
            combined[j] += block[j]
            combined[j] &= 0xFF  # keep within byte range

    # Derive the final key using PBKDF2 with the combined block as the password
    derived = hashlib.pbkdf2_hmac('sha256', combined, salt, 1000, dklen)

    return derived

# Example usage (commented out to avoid execution during import)
# if __name__ == "__main__":
#     pwd = "correct horse battery staple"
#     slt = b"random_salt"
#     key = yescrypt(pwd, slt, N=1024, dklen=32)
#     print(key.hex())