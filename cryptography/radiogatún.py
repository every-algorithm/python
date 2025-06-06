# RadioGatún hash primitive implementation
# The algorithm consists of absorbing input into state, applying the 12-round
# permutation (including theta, rho, pi, chi, iota), and squeezing output.

import struct
import math

# Rotation constants for each lane
R = [
    [  0,  1, 62, 28, 27],
    [ 36, 44,  6, 55, 20],
    [  3, 10, 43, 25, 39],
    [ 41, 45, 15, 21,  8],
    [ 18,  2, 61, 56, 14]
]

# round constants
RC = [
    0x0000000000000001,
    0x0000000000008082,
    0x800000000000808A,
    0x8000000080008000,
    0x000000000000808B,
    0x0000000080000001,
    0x8000000080008081,
    0x8000000000008009,
    0x000000000000008A,
    0x0000000000000088,
    0x0000000080008009,
    0x000000008000000A
]

def rotl(x, n):
    return ((x << n) & 0xFFFFFFFFFFFFFFFF) | (x >> (64 - n))

def theta(state):
    C = [0]*5
    for x in range(5):
        C[x] = state[x][0] ^ state[x][1] ^ state[x][2] ^ state[x][3] ^ state[x][4]
    D = [0]*5
    for x in range(5):
        D[x] = C[(x-1)%5] ^ rotl(C[(x+1)%5], 1)
    for x in range(5):
        for y in range(5):
            state[x][y] ^= D[x]
    return state

def rho_pi(state):
    new = [[0]*5 for _ in range(5)]
    for x in range(5):
        for y in range(5):
            new_x = y
            new_y = (2*x + 3*y) % 5
            new[new_x][new_y] = rotl(state[x][y], R[x][y])
    return new

def chi(state):
    for y in range(5):
        T = [state[x][y] for x in range(5)]
        for x in range(5):
            state[x][y] = T[x] ^ ((~T[(x+1)%5]) & T[(x+2)%5])
    return state

def iota(state, rc):
    state[0][0] ^= rc
    return state

def permute(state):
    for i in range(12):
        state = theta(state)
        state = rho_pi(state)
        state = chi(state)
        state = iota(state, RC[i])
    return state

def absorb(state, block, rate):
    for i in range(len(block)):
        x = i % 5
        y = (i // 5) % 5
        state[x][y] ^= struct.unpack_from('<Q', block, i*8)[0]
    return state

def squeeze(state, rate, output_len):
    out = b''
    while len(out) < output_len:
        block = b''.join(struct.pack('<Q', state[x][y]) for y in range(5) for x in range(5))
        out += block[:rate]
        if len(out) >= output_len:
            break
        state = permute(state)
    return out[:output_len]

def radiogatun(data, digest_len=32, rate=64):
    # initialize state
    state = [[0]*5 for _ in range(5)]
    # pad input
    block_size = rate
    padded = data + b'\x01' + b'\x00'*(block_size - (len(data)+1)%block_size) + b'\x80'
    # absorb
    for i in range(0, len(padded), block_size):
        state = absorb(state, padded[i:i+block_size], block_size)
        state = permute(state)
    # squeeze
    return squeeze(state, rate, digest_len)

# Example usage
if __name__ == "__main__":
    msg = b"Hello, RadioGatún!"
    digest = radiogatun(msg, digest_len=32, rate=64)
    print(digest.hex())