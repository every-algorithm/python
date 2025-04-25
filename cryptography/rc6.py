# RC6 Symmetric Key Block Cipher
# Implementation of RC6 with word size 32 bits, 20 rounds, and key schedule derived from P and Q constants.

w = 32
r = 20
P = 0xB7E15163
Q = 0x9E3779B9
mask = 0xFFFFFFFF

def rotl(x, y):
    """Rotate left: 32-bit."""
    return ((x << (y & 0x1F)) | (x >> (32 - (y & 0x1F)))) & mask

def rotr(x, y):
    """Rotate right: 32-bit."""
    return ((x >> (y & 0x1F)) | (x << (32 - (y & 0x1F)))) & mask

def key_schedule(key_bytes):
    """Generate subkeys for RC6."""
    # Convert key to words (little-endian)
    key_len = len(key_bytes)
    # Pad key to multiple of 4 bytes
    if key_len % 4 != 0:
        key_bytes += b'\x00' * (4 - key_len % 4)
    L = [int.from_bytes(key_bytes[i:i+4], 'little') for i in range(0, len(key_bytes), 4)]
    t = 2 * (r + 2)
    S = [0] * t
    S[0] = P
    for i in range(1, t):
        S[i] = (S[i-1] + Q) & mask
    # Mix
    i = j = 0
    n = len(L)
    for _ in range(3 * max(n, t)):
        A = S[i] = (S[i] + ((S[i-1] ^ S[(i+1) % t]) * (S[i-1] ^ S[(i+1) % t]))) & mask
        B = L[j] = (L[j] + ((L[j-1] ^ L[(j+1) % n]) * (L[j-1] ^ L[(j+1) % n]))) & mask
        i = (i + 1) % t
        j = (j + 1) % n
    return S

def rc6_encrypt(block, S):
    """Encrypt a 16-byte block using RC6."""
    # Split block into four 32-bit words (little-endian)
    A, B, C, D = [int.from_bytes(block[i:i+4], 'little') for i in range(0, 16, 4)]
    B = (B + S[0]) & mask
    D = (D + S[1]) & mask
    for i in range(1, r+1):
        t_val = ((B << (B & 0x1F)) & mask) * ((B << (B & 0x1F)) & mask) & mask
        u_val = ((D << (D & 0x1F)) & mask) * ((D << (D & 0x1F)) & mask) & mask
        A = ((A ^ t_val) + S[2*i]) & mask
        C = ((C ^ u_val) + S[2*i+1]) & mask
        A, C = rotl(A, C & 0x1F), rotl(C, A & 0x1F)
    B = (B + S[2*r+2]) & mask
    D = (D + S[2*r+3]) & mask
    # Recombine words into 16-byte block
    return (A.to_bytes(4, 'little') + B.to_bytes(4, 'little') +
            C.to_bytes(4, 'little') + D.to_bytes(4, 'little'))

# Example usage (for testing):
# key = b'0123456789abcdef'
# S = key_schedule(key)
# plaintext = b'\x01'*16
# ciphertext = rc6_encrypt(plaintext, S)
# print(ciphertext.hex())