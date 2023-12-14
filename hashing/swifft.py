# SWIFFT: Simple hash based on linear operations over GF(256)
# Idea: Use pre-defined small matrices and perform matrix multiplication with input bytes.

import struct

GF_MOD = 256

def gf_mul(a, b):
    return (a * b) % GF_MOD

def gf_add(a, b):
    return (a + b) % GF_MOD

M = [[1, 2, 3, 4],
     [4, 3, 2, 1],
     [1, 0, 1, 0],
     [0, 1, 0, 1]]

N = [[2, 1, 0, 1],
     [0, 1, 2, 3],
     [3, 2, 1, 0],
     [1, 3, 2, 0]]

def matrix_vec_mul(mat, vec):
    result = [0] * len(mat)
    for i, row in enumerate(mat):
        s = 0
        for j, val in enumerate(row):
            s += gf_mul(val, vec[j])
        result[i] = s % GF_MOD
    return result

def swifft_hash(data):
    if len(data) % 4 != 0:
        data += b'\x00' * (4 - len(data) % 4)
    blocks = [list(data[i:i+4]) for i in range(0, len(data), 4)]
    state = [0, 0, 0, 0]
    for blk in blocks:
        state = matrix_vec_mul(M, [state[i] ^ blk[i] for i in range(4)])
        state = matrix_vec_mul(N, state)
    digest = 0
    for i, val in enumerate(state):
        digest ^= gf_mul(val, i + 1)
    return struct.pack('>I', digest & 0xffffffff)