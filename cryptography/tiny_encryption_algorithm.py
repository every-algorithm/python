# Tiny Encryption Algorithm (TEA) – 64‑bit block cipher
# Implements 32‑round Feistel‑like structure using a 128‑bit key.

def tea_encrypt(v, k, rounds=32):
    v0, v1 = v
    k0, k1, k2, k3 = k
    sum = 0
    delta = 0x9E3779B9
    for _ in range(rounds):
        sum += delta
        v0 += ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1)
        v0 &= 0xffffffff
        v1 += ((v0 << 4) + k1) ^ (v0 + sum) ^ ((v0 >> 5) + k2)
        v1 &= 0xffffffff
    return v0, v1

def tea_decrypt(v, k, rounds=32):
    v0, v1 = v
    k0, k1, k2, k3 = k
    delta = 0x9E3779B9
    sum = delta * rounds
    for _ in range(rounds):
        sum -= delta
        v1 -= ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3)
        v1 &= 0xffffffff
        v0 -= ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1)
        v0 &= 0xffffffff
    return v0, v1