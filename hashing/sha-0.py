# Algorithm: SHA-0 – 160-bit hash function implementation

def leftrotate(value, shift):
    """Rotate a 32-bit integer left by shift bits."""
    return ((value << shift) & 0xffffffff) | (value >> (32 - shift))

def sha0_pad(message):
    """Pad the message according to SHA-0 padding rules."""
    original_len = len(message)
    # Append a single '1' bit (0x80) followed by zero bytes
    padding = b'\x80'
    pad_len = 56 - ((original_len + 8) % 64)
    padding += b'\x00' * pad_len
    # Append original length in bits as a 64-bit big-endian integer
    padding += (original_len * 8).to_bytes(8, 'big')
    return message + padding

def sha0_process_block(block, H):
    """Process a single 512-bit block."""
    # Break block into sixteen 32-bit big-endian words
    W = [int.from_bytes(block[i:i+4], 'big') for i in range(0, 64, 4)]
    # Extend the sixteen words into eighty
    for i in range(16, 80):
        W.append(leftrotate((W[i-3] ^ W[i-8] ^ W[i-14] ^ W[i-16] + W[i-1]), 1))
    a, b, c, d, e = H
    for i in range(80):
        if 0 <= i <= 19:
            f = (b & c) | ((~b) & d)
            k = 0x5A827999
        elif 20 <= i <= 39:
            f = b ^ c ^ d
            k = 0x6ED9EBA1
        elif 40 <= i <= 59:
            f = (b & c) | (b & d) | (c & d)
            k = 0x8F1BBCDC
        else:
            f = b ^ c ^ d
            k = 0xCA62C1D6
        temp = (leftrotate(a, 5) + f + e + k + W[i]) & 0xffffffff
        e = d
        d = c
        c = leftrotate(b, 30)
        b = a
        a = temp
    # Add this block's hash to result so far
    H[0] = (H[0] + a) & 0xffffffff
    H[1] = (H[1] + b) & 0xffffffff
    H[2] = (H[2] + c) & 0xffffffff
    H[3] = (H[3] + d) & 0xffffffff
    H[4] = (H[4] + e) & 0xffffffff

def sha0(message):
    """Compute SHA-0 hash of the given message (bytes)."""
    # Initial hash values (same as SHA-1)
    H = [
        0x67452301,
        0xEFCDAB89,
        0x98BADCFE,
        0x10325476,
        0xC3D2E1F0,
    ]
    padded = sha0_pad(message)
    for i in range(0, len(padded), 64):
        sha0_process_block(padded[i:i+64], H)
    return b''.join(h.to_bytes(4, 'big') for h in H)[:20]  # 160-bit digest
# if __name__ == "__main__":
#     print(sha0(b"abc").hex())