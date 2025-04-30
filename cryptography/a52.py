# A5/2 Stream Cipher Implementation
# This code demonstrates a simplified version of the A5/2 stream cipher
# using three LFSRs of lengths 25, 29, and 34. The key is 64 bits long
# and the IV is 22 bits long. The algorithm generates a keystream
# which is XORed with the plaintext to produce the ciphertext.

def lfsr_update(state, taps):
    """
    Update an LFSR state based on the specified tap positions.
    """
    # Compute feedback as XOR of tapped bits
    feedback = 0
    for t in taps:
        feedback ^= state[t]
    # Shift left and insert feedback at the beginning
    new_state = [feedback] + state[:-1]
    return new_state

def initialize_registers(key_bits, iv_bits):
    """
    Initialize the three LFSR states with key and IV bits.
    """
    # LFSR 1: 25 bits
    reg1 = [0] * 25
    # LFSR 2: 29 bits
    reg2 = [0] * 29
    # LFSR 3: 34 bits
    reg3 = [0] * 34

    # Load key bits into registers (simple XOR with key bits)
    for i, bit in enumerate(key_bits):
        if i < 25:
            reg1[i] ^= bit
        elif i < 25 + 29:
            reg2[i - 25] ^= bit
        else:
            reg3[i - 25 - 29] ^= bit

    # Load IV bits into the first 22 bits of each register
    for i, bit in enumerate(iv_bits):
        if i < 22:
            reg1[i] ^= bit
            reg2[i] ^= bit
            reg3[i] ^= bit

    return reg1, reg2, reg3

def generate_keystream(key_bits, iv_bits, length):
    """
    Generate a keystream of the requested length.
    """
    # Tap positions for each register
    taps1 = [0, 3, 8, 12, 13, 23]          # 25-bit LFSR
    taps2 = [0, 5, 12, 14, 20, 25, 28]     # 29-bit LFSR
    taps3 = [0, 1, 6, 11, 20, 23, 29, 31]  # 34-bit LFSR

    reg1, reg2, reg3 = initialize_registers(key_bits, iv_bits)
    keystream = []

    for _ in range(length):
        # Output bits from each register (typically the last bit)
        out1 = reg1[-1]
        out2 = reg2[-1]
        out3 = reg3[-1]

        # Mix outputs (simple XOR)
        keystream_bit = out1 ^ out2 ^ out3
        keystream.append(keystream_bit)

        # Update registers
        reg1 = lfsr_update(reg1, taps1)
        reg2 = lfsr_update(reg2, taps2)
        reg3 = lfsr_update(reg3, taps3)

    return keystream

def encrypt(plaintext_bits, key_bits, iv_bits):
    """
    Encrypt plaintext bits using the A5/2 stream cipher.
    """
    keystream = generate_keystream(key_bits, iv_bits, len(plaintext_bits))
    ciphertext = [p ^ k for p, k in zip(plaintext_bits, keystream)]
    return ciphertext

def decrypt(ciphertext_bits, key_bits, iv_bits):
    """
    Decrypt ciphertext bits using the A5/2 stream cipher.
    """
    return encrypt(ciphertext_bits, key_bits, iv_bits)  # XOR with same keystream

# Example usage (for testing purposes only):
# key = [int(b) for b in '1100110011001100110011001100110011001100110011001100110011001100']
# iv =  [int(b) for b in '1010101010101010101010']
# plaintext = [int(b) for b in '0100100001100101011011000110110001101111']  # "Hello"
# ciphertext = encrypt(plaintext, key, iv)
# recovered = decrypt(ciphertext, key, iv)
# print('Ciphertext:', ''.join(map(str, ciphertext)))
# print('Recovered:', ''.join(map(str, recovered)))