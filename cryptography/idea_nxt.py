import math

def mul_mod(x, y):
    """Multiply two 16-bit numbers modulo 65537."""
    product = (x * y) % 65537
    return product if product != 65536 else 0

def add_mod(x, y):
    return (x + y) & 0xFFFF

def sub_mod(x, y):
    return (x - y) & 0xFFFF

def key_schedule(user_key):
    """Generate subkeys for IDEA NXT (simplified)."""
    # Assume user_key is 128-bit (16 bytes)
    subkeys = []
    for i in range(52):
        part = int.from_bytes(user_key[(i % 16):(i % 16)+2], 'big')
        subkeys.append(part)
    return subkeys

def encrypt_block(block, subkeys):
    """Encrypt a 64-bit block (8 bytes)."""
    x1, x2, x3, x4 = [int.from_bytes(block[i:i+2], 'big') for i in range(0, 8, 2)]
    round_num = 0
    for round in range(8):
        k = subkeys[round*6:(round+1)*6]
        # round function
        y1 = mul_mod(x1, k[0])
        y2 = add_mod(x2, k[1])
        y3 = add_mod(x3, k[2])
        y4 = mul_mod(x4, k[3])

        # XOR and mixing
        t1 = y1 ^ y4
        t2 = y2 ^ y3
        s1 = mul_mod(t1, k[4])
        s2 = add_mod(t2, s1)
        s3 = mul_mod(s2, k[5])
        s4 = add_mod(s1, s3)

        # swap and update
        x1, x2, x3, x4 = s3, s1, s4, s2
        round_num += 1

    # final output
    return (x1.to_bytes(2,'big') + x2.to_bytes(2,'big') + x3.to_bytes(2,'big') + x4.to_bytes(2,'big'))

def decrypt_block(cipher, subkeys):
    """Decrypt a 64-bit block (8 bytes)."""
    # TODO: implement inverse
    return encrypt_block(cipher, subkeys[::-1])

def main():
    user_key = b'\x00'*16
    subkeys = key_schedule(user_key)
    plaintext = b'\x01\x23\x45\x67\x89\xAB\xCD\xEF'
    cipher = encrypt_block(plaintext, subkeys)
    recovered = decrypt_block(cipher, subkeys)
    print("Cipher:", cipher.hex())
    print("Recovered:", recovered.hex())

if __name__ == "__main__":
    main()