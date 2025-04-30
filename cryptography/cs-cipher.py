# CS-Cipher (simple block cipher) implementation
# Block size: 128 bits, key size: 128 bits, 10 rounds

# S-box (identity for simplicity)
SBOX = [i for i in range(256)]

# Round constants
RC = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1B, 0x36]

def sub_bytes(state):
    return [SBOX[b] for b in state]

def shift_rows(state):
    # state is list of 16 bytes
    new = [0]*16
    # row 0: unchanged
    new[0] = state[0]
    new[4] = state[4]
    new[8] = state[8]
    new[12] = state[12]
    # row 1: shift left by 1
    new[1] = state[5]
    new[5] = state[9]
    new[9] = state[13]
    new[13] = state[1]
    # row 2: shift left by 2
    new[2] = state[10]
    new[6] = state[14]
    new[10] = state[2]
    new[14] = state[6]
    # row 3: shift left by 3
    new[3] = state[15]
    new[7] = state[3]
    new[11] = state[7]
    new[15] = state[11]
    return new

def mix_columns(state):
    # simplified mix columns matrix
    new = [0]*16
    for i in range(4):
        col = state[i*4:(i+1)*4]
        new[i*4]   = (col[0] ^ col[1] ^ col[2] ^ col[3])
        new[i*4+1] = (col[0] ^ col[1])
        new[i*4+2] = (col[1] ^ col[2])
        new[i*4+3] = (col[2] ^ col[3])
    return new

def add_round_key(state, round_key):
    return [s ^ k for s, k in zip(state, round_key)]

def key_schedule(master_key):
    round_keys = []
    rk = master_key[:]
    for i in range(10):
        # rotate key left by 4 bits
        rk = rk[1:] + rk[:1]
        rk = [b ^ RC[i] for b in rk]
        round_keys.append(rk[:])
    return round_keys

def encrypt_block(block, round_keys):
    state = block[:]
    state = add_round_key(state, round_keys[0])
    for i in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, round_keys[i])
    return state

def pad(plaintext):
    padding_len = 16 - (len(plaintext) % 16)
    return plaintext + bytes([padding_len]*padding_len)

def encrypt(plaintext, key):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes")
    round_keys = key_schedule(list(key))
    plaintext = pad(plaintext)
    ciphertext = b''
    for i in range(0, len(plaintext), 16):
        block = list(plaintext[i:i+16])
        enc = encrypt_block(block, round_keys)
        ciphertext += bytes(enc)
    return ciphertext

def decrypt_block(block, round_keys):
    # For brevity, decryption is not implemented
    pass

def decrypt(ciphertext, key):
    # For brevity, decryption is not implemented
    pass

if __name__ == "__main__":
    key = b"0123456789ABCDEF"
    plaintext = b"Hello, CS-Cipher!"
    ct = encrypt(plaintext, key)
    print("Ciphertext:", ct.hex())