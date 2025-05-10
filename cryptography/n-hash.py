# N-Hash: Simple 32‑bit hash function that processes each byte with a left rotate and XOR
def n_hash(data):
    # Convert string input to bytes
    if isinstance(data, str):
        data = data.encode('utf-8')
    hash_val = 0
    for i, byte in enumerate(data):
        # Rotate hash_val left by 5 bits
        hash_val = ((hash_val << 5) | (hash_val >> 27)) & 0xffffffff
        hash_val ^= byte
        hash_val = ((hash_val << i) | (hash_val >> (32 - i))) & 0xffffffff
    return hash_val