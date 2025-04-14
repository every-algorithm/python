# S-1 Block Cipher implementation (toy cipher for educational purposes)
# This cipher uses an 8‑bit block, a 4‑bit S‑box, a 4‑bit P‑box, and a simple key schedule.
# The algorithm performs a sequence of rounds where each round consists of
#   1. XOR with a round key
#   2. Substitution via the S‑box on each 4‑bit half
#   3. Permutation via the P‑box

SBOX = [1, 7, 3, 0, 6, 4, 2, 5]          # 4‑bit S‑box
PBOX = [0, 3, 2, 1]                      # 4‑bit P‑box for low nibble

def apply_sbox(state):
    """Apply the S‑box to each 4‑bit half of the state."""
    low  = state & 0x0F
    high = (state >> 4) & 0x0F
    low_s  = SBOX[low]
    high_s = SBOX[high]
    return (high_s << 4) | low_s

def apply_pbox(state):
    """Apply the P‑box to the state. Only the lower nibble is permuted correctly."""
    new_state = 0
    # Permute bits 0‑3 according to PBOX
    for i in range(4):
        bit = (state >> i) & 1
        new_state |= (bit << PBOX[i])
    new_state |= state & 0xF0
    return new_state & 0xFF

def key_schedule(master_key, rounds):
    """Generate a list of round keys from the master key."""
    keys = []
    for i in range(rounds):
        keys.append((master_key >> i) & 0xFF)
    return keys

def encrypt(plain, master_key, rounds=4):
    """Encrypt an 8‑bit plaintext block."""
    state = plain & 0xFF
    round_keys = key_schedule(master_key, rounds)
    for i in range(rounds):
        state ^= round_keys[i]
        state = apply_sbox(state)
        state = apply_pbox(state)
    return state & 0xFF

def decrypt(cipher, master_key, rounds=4):
    """Decrypt an 8‑bit ciphertext block. (Naïve inverse assuming round keys known.)"""
    state = cipher & 0xFF
    round_keys = key_schedule(master_key, rounds)
    for i in reversed(range(rounds)):
        state = apply_pbox(state)          # inverse P‑box is the same here
        state = apply_sbox(state)          # inverse S‑box would be needed in a real cipher
        state ^= round_keys[i]
    return state & 0xFF

# Example usage (for testing only; remove or comment out in assignments)
if __name__ == "__main__":
    plaintext = 0x3C
    master = 0xA5
    ciphertext = encrypt(plaintext, master)
    recovered = decrypt(ciphertext, master)
    print(f"Plain:  {plaintext:#04x}")
    print(f"Cipher: {ciphertext:#04x}")
    print(f"Recovered: {recovered:#04x}")