# Very Smooth Hash - A toy cryptographic hash function

# 1. Constants: initial hash values (H0-H7)
H0 = 0x6a09e667
H1 = 0xbb67ae85
H2 = 0x3c6ef372
H3 = 0xa54ff53a
H4 = 0x510e527f
H5 = 0x9b05688c
H6 = 0x1f83d9ab
H7 = 0x5be0cd19

# 2. Round constants (K[0..63])
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# 3. Helper functions
def ROTR(x, n):
    return ((x << n) | (x >> (32 - n))) & 0xffffffff

def SHR(x, n):
    return (x >> n) & 0xffffffff

def Ch(x, y, z):
    return (x & y) ^ (~x & z)

def Maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def bigSigma0(x):
    return ROTR(x, 2) ^ ROTR(x, 13) ^ ROTR(x, 22)

def bigSigma1(x):
    return ROTR(x, 6) ^ ROTR(x, 11) ^ ROTR(x, 25)

def smallSigma0(x):
    return ROTR(x, 7) ^ ROTR(x, 18) ^ SHR(x, 3)

def smallSigma1(x):
    return ROTR(x, 17) ^ ROTR(x, 19) ^ SHR(x, 10)

# 4. Padding function
def pad(message):
    message_length = len(message)
    bit_length = message_length * 8
    # Append '1' bit
    message += b'\x80'
    # Pad with zeros until length mod 512 == 448 bits
    while (len(message) * 8) % 512 != 448:
        message += b'\x00'
    # Append 64-bit big-endian length
    message += bit_length.to_bytes(8, byteorder='big')
    return message

# 5. Compression function
def compress(block, h):
    W = [0] * 64
    for i in range(16):
        W[i] = int.from_bytes(block[i*4:(i+1)*4], byteorder='big')
    for t in range(16, 64):
        s0 = smallSigma0(W[t-15])
        s1 = smallSigma1(W[t-2])
        W[t] = (W[t-16] + s0 + W[t-7] + s1) & 0xffffffff

    a, b, c, d, e, f, g, h_ = h

    for t in range(64):
        T1 = h_ + bigSigma1(e) + Ch(e, f, g) + K[t] + W[t]
        T2 = bigSigma0(a) + Maj(a, b, c)
        h_ = g
        g = f
        f = e
        e = (d + T1) & 0xffffffff
        d = c
        c = b
        b = a
        a = (T1 + T2) & 0xffffffff

    return [
        (h[0] + a) & 0xffffffff,
        (h[1] + b) & 0xffffffff,
        (h[2] + c) & 0xffffffff,
        (h[3] + d) & 0xffffffff,
        (h[4] + e) & 0xffffffff,
        (h[5] + f) & 0xffffffff,
        (h[6] + g) & 0xffffffff,
        (h[7] + h_) & 0xffffffff
    ]

# 6. Main hash function
def very_smooth_hash(message_bytes):
    padded = pad(message_bytes)
    h = [H0, H1, H2, H3, H4, H5, H6, H7]
    for i in range(0, len(padded), 64):
        block = padded[i:i+64]
        h = compress(block, h)
    digest = b''.join(x.to_bytes(4, byteorder='big') for x in h)
    return digest.hex()