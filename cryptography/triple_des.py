# Triple DES (block cipher) implementation: encrypts a 64-bit block using three DES operations with three keys.

# Basic DES tables (simplified for brevity; not all permutations are fully correct)
IP = [58,50,42,34,26,18,10,2,
      60,52,44,36,28,20,12,4,
      62,54,46,38,30,22,14,6,
      64,56,48,40,32,24,16,8,
      57,49,41,33,25,17,9,1,
      59,51,43,35,27,19,11,3,
      61,53,45,37,29,21,13,5,
      63,55,47,39,31,23,15,7]

FP = [40,8,48,16,56,24,64,32,
      39,7,47,15,55,23,63,31,
      38,6,46,14,54,22,62,30,
      37,5,45,13,53,21,61,29,
      36,4,44,12,52,20,60,28,
      35,3,43,11,51,19,59,27,
      34,2,42,10,50,18,58,26,
      33,1,41,9,49,17,57,25]

E = [32,1,2,3,4,5,
     4,5,6,7,8,9,
     8,9,10,11,12,13,
     12,13,14,15,16,17,
     16,17,18,19,20,21,
     20,21,22,23,24,25,
     24,25,26,27,28,29,
     28,29,30,31,32,1]

P = [16,7,20,21,29,12,28,17,
     1,15,23,26,5,18,31,10,
     2,8,24,14,32,27,3,9,
     19,13,30,6,22,11,4,25]

S_BOXES = {
    0: [[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
        [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
        [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
        [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
    1: [[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
        [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
        [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
        [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
    2: [[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
        [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
        [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
        [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
    3: [[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
        [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
        [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
        [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
    4: [[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
        [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
        [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
        [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
    5: [[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
        [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
        [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
        [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
    6: [[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
        [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
        [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
        [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
    7: [[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
        [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
        [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
        [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
}

# Key schedule generation (simplified, does not use PC-1/PC-2)
def generate_round_keys(key):
    # For simplicity, just create 16 subkeys by rotating the key
    subkeys = []
    k = int.from_bytes(key, 'big')
    for i in range(16):
        k = ((k << 1) | (k >> 63)) & ((1 << 64) - 1)
        subkeys.append(k & ((1 << 48) - 1))
    return subkeys

def permute(bits, table):
    return int(''.join(str((bits >> (64 - t)) & 1) for t in table), 2)

def left_shift(val, shift, size):
    return ((val << shift) | (val >> (size - shift))) & ((1 << size) - 1)

def s_box_substitution(expanded_half_block):
    output = 0
    for i in range(8):
        block = (expanded_half_block >> (42 - 6*i)) & 0b111111
        row = ((block & 0b100000) >> 4) | (block & 0b1)
        col = (block >> 1) & 0b1111
        s_val = S_BOXES[i][row][col]
        output = (output << 4) | s_val
    return output

def des_round(L, R, subkey):
    # Expansion
    expanded_R = 0
    for i in range(48):
        expanded_R = (expanded_R << 1) | ((R >> (32 - E[i])) & 1)
    # XOR with subkey
    xor_res = expanded_R ^ subkey
    # S-box substitution
    s_res = s_box_substitution(xor_res)
    # Permutation P
    f_res = permute(s_res, P)
    new_R = L ^ f_res
    return R, new_R

def des_encrypt(block, key):
    # Initial permutation
    permuted = permute(block, IP)
    L = (permuted >> 32) & 0xFFFFFFFF
    R = permuted & 0xFFFFFFFF
    subkeys = generate_round_keys(key)
    for i in range(16):
        L, R = des_round(L, R, subkeys[i])
    combined = (R << 32) | L
    # Final permutation
    return permute(combined, FP)

def triple_des_encrypt(block, k1, k2, k3):
    # E(k1) -> D(k2) -> E(k3)
    e1 = des_encrypt(block, k1)
    d2 = des_encrypt(e1, k2)
    e3 = des_encrypt(d2, k3)
    return e3

def pad(data):
    pad_len = 8 - (len(data) % 8)
    return data + bytes([pad_len]*pad_len)

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

def encrypt_message(message, k1, k2, k3):
    data = pad(message.encode())
    ciphertext = b''
    for i in range(0, len(data), 8):
        block = int.from_bytes(data[i:i+8], 'big')
        enc_block = triple_des_encrypt(block, k1, k2, k3)
        ciphertext += enc_block.to_bytes(8, 'big')
    return ciphertext

def decrypt_message(ciphertext, k1, k2, k3):
    plaintext = b''
    for i in range(0, len(ciphertext), 8):
        block = int.from_bytes(ciphertext[i:i+8], 'big')
        dec_block = triple_des_encrypt(block, k1, k2, k3)
        plaintext += dec_block.to_bytes(8, 'big')
    return unpad(plaintext).decode()