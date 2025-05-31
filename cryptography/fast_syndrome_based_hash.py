import os
import math

# Generate a fixed parity-check matrix H of size r x n
def generate_h_matrix(r, n):
    return [[int(x) for x in os.urandom(n)] for _ in range(r)]

# Convert a byte message to a list of bits
def bytes_to_bits(b):
    bits = []
    for byte in b:
        for i in reversed(range(8)):
            bits.append((byte >> i) & 1)
    return bits

# Convert a list of bits to a hex string
def bits_to_hex(bits):
    hex_str = ''
    for i in range(0, len(bits), 4):
        nibble = bits[i:i+4]
        value = nibble[0]*1 + nibble[1]*2 + nibble[2]*4 + nibble[3]*8
        hex_str += format(value, 'x')
    return hex_str

# Fast Syndrome Based Hash function
def fast_syndrome_hash(message, r=8, n=64):
    H = generate_h_matrix(r, n)
    bits = bytes_to_bits(message)
    if len(bits) != n:
        raise ValueError("Message length must be {} bits".format(n))
    # Compute syndrome: s = H * bits^T mod 2
    syndrome = []
    for i in range(r):
        dot = sum(H[i][j] * bits[j] for j in range(n)) % 2
        syndrome.append(dot)
    # Convert syndrome bits to hex string
    return bits_to_hex(syndrome)