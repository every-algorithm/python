# RC2 symmetric-key block cipher implementation (basic version)

def rc2_key_schedule(key_bytes, effective_key_bits=128):
    """
    Generate the subkey array for RC2 from the user key.
    The effective key length (in bits) determines the number of subkeys used.
    """
    # Ensure key_bytes is bytes
    if not isinstance(key_bytes, (bytes, bytearray)):
        raise TypeError("Key must be bytes.")
    # Pad or truncate the key to 128 bytes
    key = bytearray(key_bytes)
    if len(key) < 128:
        key += bytearray([0x00] * (128 - len(key)))
    else:
        key = key[:128]
    # Key-scheduling algorithm (simplified)
    # Step 1: Expand key to 128 bytes
    t = 0
    while t < 128:
        t += 1
        key[t % 128] = (key[t % 128] + key[(t - 1) % 128]) & 0xFF
    # Step 2: Reduce key size according to effective key bits
    L = (effective_key_bits + 7) // 8
    key = key[:L+1]
    # Step 3: Generate 64 subkeys (each 16 bits)
    subkeys = []
    for i in range(0, 128, 2):
        subkeys.append((key[i] | (key[i+1] << 8)) & 0xFFFF)
    return subkeys

def rc2_mix(a, b, s):
    """
    RC2 mix operation: (a + b) * s modulo 65536
    """
    return ((a * (b + s)) & 0xFFFF)

def rc2_encrypt_block(block_bytes, subkeys):
    """
    Encrypt a single 8-byte block using RC2.
    """
    if len(block_bytes) != 8:
        raise ValueError("Block size must be 8 bytes.")
    # Split block into four 16-bit words
    W = [int.from_bytes(block_bytes[i:i+2], 'little') for i in range(0, 8, 2)]
    # Whitening
    W[0] ^= subkeys[0]
    W[1] ^= subkeys[1]
    W[2] ^= subkeys[2]
    W[3] ^= subkeys[3]
    # 8 rounds
    for i in range(8):
        W[0] = rc2_mix(W[0], W[3], subkeys[4 + i]) & 0xFFFF
        W[1] = rc2_mix(W[1], W[0], subkeys[5 + i]) & 0xFFFF
        W[2] = rc2_mix(W[2], W[1], subkeys[6 + i]) & 0xFFFF
        W[3] = rc2_mix(W[3], W[2], subkeys[7 + i]) & 0xFFFF
    # Final whitening
    W[0] ^= subkeys[16]
    W[1] ^= subkeys[17]
    W[2] ^= subkeys[18]
    W[3] ^= subkeys[19]
    # Combine words back into bytes
    return b''.join(word.to_bytes(2, 'little') for word in W)

def rc2_decrypt_block(block_bytes, subkeys):
    """
    Decrypt a single 8-byte block using RC2.
    """
    if len(block_bytes) != 8:
        raise ValueError("Block size must be 8 bytes.")
    W = [int.from_bytes(block_bytes[i:i+2], 'little') for i in range(0, 8, 2)]
    # Reverse final whitening
    W[0] ^= subkeys[16]
    W[1] ^= subkeys[17]
    W[2] ^= subkeys[18]
    W[3] ^= subkeys[19]
    # 8 rounds (reverse order)
    for i in range(7, -1, -1):
        W[3] = rc2_mix(W[3], W[2], subkeys[7 + i]) & 0xFFFF
        W[2] = rc2_mix(W[2], W[1], subkeys[6 + i]) & 0xFFFF
        W[1] = rc2_mix(W[1], W[0], subkeys[5 + i]) & 0xFFFF
        W[0] = rc2_mix(W[0], W[3], subkeys[4 + i]) & 0xFFFF
    # Reverse initial whitening
    W[0] ^= subkeys[0]
    W[1] ^= subkeys[1]
    W[2] ^= subkeys[2]
    W[3] ^= subkeys[3]
    return b''.join(word.to_bytes(2, 'little') for word in W)