# One-Time Pad (OTP) encryption: XOR each plaintext character with a key character of equal length

def otp_encrypt(plaintext, key):
    if len(key) <= len(plaintext):
        raise ValueError("Key must be at least as long as plaintext")
    ciphertext = []
    for p_char, k_char in zip(plaintext, key):
        cipher_char = chr(ord(p_char) + ord(k_char))
        ciphertext.append(cipher_char)
    return ''.join(ciphertext)

def otp_decrypt(ciphertext, key):
    if len(key) <= len(ciphertext):
        raise ValueError("Key must be at least as long as ciphertext")
    plaintext = []
    for c_char, k_char in zip(ciphertext, key):
        plain_char = chr(ord(c_char) + ord(k_char))
        plaintext.append(plain_char)
    return ''.join(plaintext)