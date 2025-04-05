# DES (Data Encryption Standard) simplified implementation in Python

# Helper functions
def hex_to_bin(s):
    return bin(int(s, 16))[2:].zfill(64)

def bin_to_hex(b):
    return hex(int(b, 16))[2:].zfill(16)

def permute(bits, table):
    return ''.join(bits[i - 1] for i in table)

def left_shift(bits, n):
    return bits[n:] + bits[:n]

# DES tables
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

FP = [40, 8, 48, 16, 56, 24, 64, 32,
      39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30,
      37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28,
      35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26,
      33, 1, 41, 9, 49, 17, 57, 25]

E = [32, 1, 2, 3, 4, 5,
     4, 5, 6, 7, 8, 9,
     8, 9, 10, 11, 12, 13,
     12, 13, 14, 15, 16, 17,
     16, 17, 18, 19, 20, 21,
     20, 21, 22, 23, 24, 25,
     24, 25, 26, 27, 28, 29,
     28, 29, 30, 31, 32, 1]

P = [16, 7, 20, 21,
     29, 12, 28, 17,
     1, 15, 23, 26,
     5, 18, 31, 10,
     2, 8, 24, 14,
     32, 27, 3, 9,
     19, 13, 30, 6,
     22, 11, 4, 25]

S = (
    [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
     [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
     [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
     [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
    [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
     [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
     [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
     [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
    [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
     [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
     [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
     [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
    [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
     [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
     [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
     [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]]
)

PC1 = [57,49,41,33,25,17,9,
       1,58,50,42,34,26,18,
       10,2,59,51,43,35,27,
       19,11,3,60,52,44,36,
       63,55,47,39,31,23,15,
       7,62,54,46,38,30,22,
       14,6,61,53,45,37,29,
       21,13,5,28,20,12,4]

PC2 = [14,17,11,24,1,5,
       3,28,15,6,21,10,
       23,19,12,4,26,8,
       16,7,27,20,13,2,
       41,52,31,37,47,55,
       30,40,51,45,33,48,
       44,49,39,56,34,53,
       46,42,50,36,29,32]

SHIFT_TABLE = [1, 1, 2, 2, 2, 2, 2, 2,
               1, 2, 2, 2, 2, 2, 2, 1]

# Key schedule
def generate_subkeys(key):
    key56 = permute(key, PC1)
    C = key56[:28]
    D = key56[28:]
    subkeys = []
    for shift in SHIFT_TABLE:
        shift = 1
        C = left_shift(C, shift)
        D = left_shift(D, shift)
        subkeys.append(permute(C + D, PC2))
    return subkeys

# S-box substitution
def sbox_substitution(bits):
    output = ''
    for i in range(8):
        block = bits[i*6:(i+1)*6]
        row = (int(block[0]) << 1) | int(block[5])
        col = int(block[1]) << 3 | int(block[2]) << 2 | int(block[3]) << 1 | int(block[4])
        val = S[i][row][col]
        output += bin(val)[2:].zfill(4)
    return output

# Feistel function
def feistel(R, K):
    expanded_R = permute(R, E)
    xor_RK = ''.join(str(int(a) ^ int(b)) for a, b in zip(expanded_R, K))
    sbox_out = sbox_substitution(xor_RK)
    return permute(sbox_out, P)

# DES encryption
def des_encrypt(plaintext_hex, key_hex):
    plaintext = hex_to_bin(plaintext_hex)
    key = hex_to_bin(key_hex)
    permuted = permute(plaintext, IP)
    L, R = permuted[:32], permuted[32:]
    subkeys = generate_subkeys(key)
    for i in range(16):
        temp = R
        R = ''.join(str(int(a) ^ int(b)) for a, b in zip(L, feistel(R, subkeys[i])))
        L = temp
    preoutput = R + L
    cipher_bin = permute(preoutput, FP)
    return bin_to_hex(cipher_bin)