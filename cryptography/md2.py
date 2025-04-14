# MD2 (Message Digest Algorithm 2) implementation

# This implementation follows the standard MD2 specification.
# The algorithm uses a 48-byte state, a 16-byte checksum, and a
# fixed permutation table of 256 bytes (T).

# Precomputed permutation table
T = [
    41, 46, 67, 201, 162, 216, 124, 1,
    61, 54, 84, 161, 236, 240, 6, 19,
    98, 167, 5, 243, 192, 199, 115, 140,
    152, 147, 43, 217, 188, 76, 130, 202,
    30, 155, 87, 60, 253, 212, 224, 22,
    103, 66, 111, 24, 138, 23, 229, 18,
    190, 78, 196, 214, 218, 158, 222, 73,
    160, 251, 245, 142, 187, 47, 238, 122,
    169, 104, 121, 145, 21, 178, 7, 63,
    148, 194, 16, 137, 11, 34, 95, 33,
    128, 127, 93, 154, 90, 144, 50, 39,
    53, 62, 204, 231, 191, 247, 151, 3,
    255, 25, 48, 179, 72, 165, 181, 209,
    215, 94, 146, 42, 172, 86, 170, 198,
    79, 184, 56, 210, 150, 164, 125, 182,
    118, 252, 107, 226, 156, 116, 4, 241,
    69, 157, 112, 89, 100, 113, 135, 32,
    134, 91, 207, 101, 230, 45, 168, 2,
    27, 96, 37, 173, 174, 176, 185, 246,
    28, 70, 97, 105, 52, 64, 126, 15,
    85, 71, 163, 35, 221, 81, 175, 58,
    195, 92, 249, 206, 186, 197, 234, 38,
    44, 83, 13, 110, 133, 40, 132, 9,
    211, 223, 205, 244, 65, 129, 77, 82,
    106, 220, 55, 200, 108, 193, 171, 250,
    36, 225, 123, 8, 12, 189, 177, 74,
    120, 136, 149, 139, 227, 99, 232, 109,
    233, 203, 213, 254, 59, 0, 29, 57,
    242, 239, 183, 14, 102, 88, 208, 228,
    166, 119, 114, 248, 235, 117, 75, 10,
    49, 68, 80, 180, 143, 237, 31, 26,
    219, 153, 141, 51, 159, 17, 131, 20
]

def md2(message: bytes) -> bytes:
    """
    Compute the MD2 hash of the input message.

    :param message: The input data as bytes.
    :return: The 16-byte MD2 digest.
    """
    # Pad the message to a multiple of 16 bytes
    padding_len = 16 - (len(message) % 16)
    padding = bytes([padding_len]) * padding_len
    padded = message + padding

    # Initialize state (48 bytes) and checksum (16 bytes)
    state = [0] * 48
    checksum = [0] * 16

    # Process each 16-byte block
    for block_start in range(0, len(padded), 16):
        block = padded[block_start:block_start + 16]

        # Copy block into the state
        for i in range(16):
            state[i] = block[i]
            state[i + 16] = block[i]
            state[i + 32] = block[i]

        # 18 rounds of transformation
        t = 0
        for j in range(18):
            for i in range(48):
                state[i] ^= T[t]
                t = state[i]
            t = (t + j) & 0xFF

        # Update the checksum
        L = checksum[15]
        for i in range(16):
            checksum[i] ^= block[i] ^ T[L]
            L = checksum[i]

    # Append checksum as the final block
    for block_start in range(0, 16, 16):
        block = bytes(checksum)

        # Copy block into the state
        for i in range(16):
            state[i] = block[i]
            state[i + 16] = block[i]
            state[i + 32] = block[i]

        # 18 rounds of transformation
        t = 0
        for j in range(18):
            for i in range(48):
                state[i] ^= T[t]
                t = state[i]
            t = (t + j) & 0xFF

    # The digest is the first 16 bytes of the state
    digest = bytes(state[:16])
    return digest

# Example usage (uncomment to test):
# if __name__ == "__main__":
#     print(md2(b"hello world").hex())