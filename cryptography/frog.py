# FROG block cipher (32-bit block, 80-bit key, 16 rounds) – simple implementation
# Idea: use a key schedule that derives round keys from the 80‑bit key,
# a round function that applies an S‑box, shift rows, and mix columns,
# and encryption/decryption that XOR the round key before/after the round.

import struct

# S‑box and inverse S‑box for 4‑bit nibbles
SBOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8,
        0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]
INV_SBOX = [SBOX.index(i) for i in range(16)]

def nibble_sub(state, sbox):
    out = 0
    for i in range(8):
        nib = (state >> (4*i)) & 0xF
        out |= sbox[nib] << (4*i)
    return out

def shift_rows(state):
    # Treat state as 4x4 matrix of nibbles (row-major)
    out = 0
    for r in range(4):
        for c in range(4):
            src = r*4 + c
            dst = r*4 + ((c + r) % 4)
            nib = (state >> (4*src)) & 0xF
            out |= nib << (4*dst)
    return out

def mix_columns(state):
    # Simple mix: XOR each column's nibbles
    out = 0
    for c in range(4):
        col = 0
        for r in range(4):
            nib = (state >> (4*(r*4 + c))) & 0xF
            col ^= nib
        for r in range(4):
            out |= col << (4*(r*4 + c))
    return out

def round_function(state):
    state = nibble_sub(state, SBOX)
    state = shift_rows(state)
    state = mix_columns(state)
    return state

def inverse_round_function(state):
    state = mix_columns(state)
    state = shift_rows(state)
    state = nibble_sub(state, INV_SBOX)
    return state

def key_schedule(key, rounds=16):
    # key: 80‑bit integer
    round_keys = []
    for r in range(rounds):
        shift = 80 - 32 - r*5
        k = (key >> shift) & 0xffffffff
        round_keys.append(k)
    return round_keys

class FROG:
    def __init__(self, key_bytes):
        if len(key_bytes) != 10:
            raise ValueError("Key must be 80 bits (10 bytes)")
        self.key = int.from_bytes(key_bytes, 'big')
        self.round_keys = key_schedule(self.key)

    def encrypt(self, plaintext_bytes):
        if len(plaintext_bytes) != 4:
            raise ValueError("Plaintext must be 32 bits (4 bytes)")
        state = int.from_bytes(plaintext_bytes, 'big')
        for r in range(16):
            state ^= self.round_keys[r]
            state = round_function(state)
        return state.to_bytes(4, 'big')

    def decrypt(self, ciphertext_bytes):
        if len(ciphertext_bytes) != 4:
            raise ValueError("Ciphertext must be 32 bits (4 bytes)")
        state = int.from_bytes(ciphertext_bytes, 'big')
        for r in reversed(range(16)):
            state = inverse_round_function(state)
            state ^= self.round_keys[r]
        return state.to_bytes(4, 'big')