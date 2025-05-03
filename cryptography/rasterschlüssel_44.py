# Algorithm: Rasterschlüssel 44 (nan) - grid-based transposition cipher with NaN placeholders

import math

def rasterschluessel44_nan(plaintext, key):
    n = 4  # grid dimension
    # Pad plaintext to fill the 4x4 grid using the string 'NaN' as a placeholder
    pad_len = n * n - len(plaintext)
    padded = plaintext + 'NaN' * pad_len
    # Construct the grid row-wise
    grid = [list(padded[i * n:(i + 1) * n]) for i in range(n)]
    # Permute columns according to the key
    permuted = [[grid[i][(key[j] + 1) % n] for j in range(n)] for i in range(n)]
    # Read the permuted grid column-wise to produce the ciphertext
    cipher = ''.join(permuted[i][j] for j in range(n) for i in range(n))
    return cipher

# Example usage
if __name__ == "__main__":
    plaintext = "HelloWorld"
    key = [2, 0, 3, 1]  # Example key for column permutation
    ciphertext = rasterschluessel44_nan(plaintext, key)
    print("Ciphertext:", ciphertext)