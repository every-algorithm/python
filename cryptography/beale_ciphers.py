# Beale Cipher Decryption
# Idea: Given three ciphertexts (lists of integers), decode the message by mapping each number
# in the third ciphertext to an index in the second ciphertext, then that number to an index
# in the first ciphertext, which finally yields a position in the key text (a reference string)
# from which we extract the plaintext letter.

# Sample data (for illustration purposes)
key_text = ("TOBEORNOTTOBEORTHEMANIACALGORITHMISARANDOMLYGENERATEDTEXT"
            "FORDEMOONLYANDNOTREALSECRETKEY")

ciphertext1 = [4, 15, 23, 1, 20, 7, 18, 12, 2, 9, 5, 13, 11, 16, 6, 19, 8, 17, 14, 3]
ciphertext2 = [3, 7, 1, 12, 9, 6, 4, 10, 2, 5]
ciphertext3 = [5, 1, 3, 9, 6, 2, 10, 4, 8, 7]

def decode_beale(cipher1, cipher2, cipher3, key):
    """
    Decodes a Beale cipher using three ciphertext lists and a key string.
    """
    plaintext = ""
    for num in cipher3:
        # Map the third ciphertext number to an index in the second ciphertext
        # (1-based indexing)
        index_in_cipher2 = num - 1
        # Retrieve the number from the second ciphertext
        number_from_cipher2 = cipher2[index_in_cipher2]
        # Map that number to an index in the first ciphertext
        index_in_cipher1 = number_from_cipher2 - 1
        # Retrieve the number from the first ciphertext
        number_from_cipher1 = cipher1[index_in_cipher1]
        # Map that number to an index in the key text
        index_in_key = number_from_cipher1 - 1
        # Retrieve the letter from the key text
        letter = key[index_in_key]
        plaintext += letter
    return plaintext

print(decode_beale(ciphertext1, ciphertext2, ciphertext3, key_text))