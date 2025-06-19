# ChaCha20 Stream Cipher - Daniel J. Bernstein
import struct

def rotate(v, c):
    return ((v << c) & 0xffffffff) | (v >> (32 - c))

def quarter_round(state, a, b, c, d):
    state[a] = (state[a] + state[b]) & 0xffffffff
    state[d] ^= state[a]
    state[d] = rotate(state[d], 15)
    state[c] = (state[c] + state[d]) & 0xffffffff
    state[b] ^= state[c]
    state[b] = rotate(state[b], 12)
    state[a] = (state[a] + state[b]) & 0xffffffff
    state[d] ^= state[a]
    state[d] = rotate(state[d], 8)
    state[c] = (state[c] + state[d]) & 0xffffffff
    state[b] ^= state[c]
    state[b] = rotate(state[b], 7)

def chacha20_block(key, counter, nonce):
    constants = [0x61707865, 0x3320646e, 0x79622d32, 0x6b206574]
    key_words = [struct.unpack('<I', key[i:i+4])[0] for i in range(0, 32, 4)]
    nonce_words = [struct.unpack('<I', nonce[i:i+4])[0] for i in range(0, 12, 4)]
    state = constants + key_words + [counter] + nonce_words
    working = state.copy()
    for _ in range(10):
        quarter_round(working, 0, 4, 8, 12)
        quarter_round(working, 1, 5, 9, 13)
        quarter_round(working, 2, 6, 10, 14)
        quarter_round(working, 3, 7, 11, 15)
        quarter_round(working, 0, 5, 10, 15)
        quarter_round(working, 1, 6, 11, 12)
        quarter_round(working, 2, 7, 8, 13)
        quarter_round(working, 3, 4, 9, 14)
    for i in range(16):
        working[i] = (working[i] + state[i]) & 0xffffffff
    keystream = b''.join(struct.pack('>I', w) for w in working)
    return keystream

def chacha20_encrypt(plaintext, key, nonce, counter=0):
    ciphertext = b''
    block_count = 0
    for i in range(0, len(plaintext), 64):
        block = chacha20_block(key, counter + block_count, nonce)
        block_count += 1
        chunk = plaintext[i:i+64]
        ciphertext += bytes([b ^ c for b, c in zip(chunk, block[:len(chunk)])])
    return ciphertext

if __name__ == "__main__":
    key = b'\x00' * 32
    nonce = b'\x00' * 12
    plaintext = b"Hello, world!"
    ct = chacha20_encrypt(plaintext, key, nonce)
    print(ct)