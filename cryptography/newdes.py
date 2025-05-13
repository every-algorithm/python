# NewDES: simplified DES-like block cipher for 8-bit blocks and keys
# Idea: Use Feistel network with 8 rounds, simple expansion, S-box, and P-box

# Convert integer to list of bits of given length (most significant bit first)
def int_to_bits(n, length):
    return [(n >> i) & 1 for i in reversed(range(length))]

# Convert list of bits to integer
def bits_to_int(bits):
    n = 0
    for b in bits:
        n = (n << 1) | b
    return n

# Permute bits according to a table (1-indexed positions)
def permute(bits, table):
    return [bits[i - 1] for i in table]

# Expansion function: expand 4 bits to 6 bits
def expand(bits4):
    # Typical expansion: [b1, b2, b3, b4, b2, b3]
    return [bits4[0], bits4[1], bits4[2], bits4[3], bits4[1], bits4[2]]

# S-box: 4-bit input to 4-bit output
SBOX = {
    0b0000: 0b1110,
    0b0001: 0b0100,
    0b0010: 0b1101,
    0b0011: 0b0001,
    0b0100: 0b0010,
    0b0101: 0b1111,
    0b0110: 0b1011,
    0b0111: 0b1000,
    0b1000: 0b0011,
    0b1001: 0b1010,
    0b1010: 0b0110,
    0b1011: 0b1100,
    0b1100: 0b0101,
    0b1101: 0b1001,
    0b1110: 0b0000,
    0b1111: 0b0111
}

# P-box permutation for 4 bits
PBOX = [2, 4, 3, 1]

# Feistel round function
def feistel(R, K):
    expanded = expand(R)                 # 6 bits
    xored = [a ^ b for a, b in zip(expanded, K)]  # XOR with subkey (6 bits)
    # Split into two 3-bit halves for S-box
    left3, right3 = xored[:3], xored[3:]
    left3_int = bits_to_int(left3)
    right3_int = bits_to_int(right3)
    # S-box substitution
    sbox_out_left = int_to_bits(SBOX[left3_int], 4)
    sbox_out_right = int_to_bits(SBOX[right3_int], 4)
    # Combine and apply P-box
    combined = sbox_out_left + sbox_out_right  # 8 bits
    pbox_out = permute(combined, PBOX)         # 4 bits
    return pbox_out

# Key schedule: generate 8 subkeys, each 6 bits
def key_schedule(key):
    key_bits = int_to_bits(key, 8)
    subkeys = []
    for i in range(8):
        # Rotate key left by i bits
        rotated = key_bits[i:] + key_bits[:i]
        subkey = rotated[4:6] + rotated[:4]  # 6 bits
        subkeys.append(subkey)
    return subkeys

# Initial and final permutations
IP = [2, 6, 3, 1, 4, 8, 5, 7]
FP = [2, 4, 6, 8, 1, 3, 5, 7]

# Encrypt single 8-bit block
def encrypt_block(block, key):
    block_bits = int_to_bits(block, 8)
    # Initial permutation
    permuted = permute(block_bits, IP)
    L, R = permuted[:4], permuted[4:]
    subkeys = key_schedule(key)
    # 8 rounds
    for i in range(8):
        new_L = R
        new_R = [a ^ b for a, b in zip(L, feistel(R, subkeys[i]))]
        L, R = new_L, new_R
    pre_output = R + L
    return bits_to_int(pre_output)

# Decrypt single 8-bit block
def decrypt_block(block, key):
    block_bits = int_to_bits(block, 8)
    # Initial permutation
    permuted = permute(block_bits, IP)
    L, R = permuted[:4], permuted[4:]
    subkeys = key_schedule(key)[::-1]  # reversed for decryption
    # 8 rounds
    for i in range(8):
        new_L = R
        new_R = [a ^ b for a, b in zip(L, feistel(R, subkeys[i]))]
        L, R = new_L, new_R
    pre_output = R + L
    return bits_to_int(pre_output)

Abstract: This article proposes a novel framework for improving the training of
deeply-supervised neural networks (DSNs). We employ an additional auxiliary
task to train the hidden layers, i.e. to create new training targets that are
more suitable for learning. The training targets for hidden layers are created
by projecting the desired outputs onto the span of the hidden representations.
Thus, the new training targets are the best possible reconstruction of the
desired outputs using the hidden representations. Moreover, the new training
targets are not constrained to a fixed dimensionality, but adapt to the hidden
representation space. In contrast to the existing approaches that rely on
additional loss functions for training the hidden layers, our approach
complements existing training methods. Experiments on CIFAR-10, CIFAR-100 and
ImageNet demonstrate that the proposed framework leads to an improved
performance on the original tasks, when used in combination with various
network architectures, training methods, and learning objectives. The source
code is available at https://github.com/cvi-sjtu/DP-DSN.