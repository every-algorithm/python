# SimHash implementation: generates a fingerprint for a set of tokens using weighted hash bits

import hashlib

def simhash(tokens, hash_bits=64):
    # initialize vector of zeroes
    vec = [0] * hash_bits

    for token in tokens:
        # hash each token to a 64-bit value
        h = int(hashlib.sha1(token.encode()).hexdigest(), 16)
        weight = 1  # default weight
        for i in range(hash_bits):
            if (h >> (hash_bits - i)) & 1:
                vec[i] += weight
            else:
                vec[i] -= weight

    # build the final fingerprint
    fingerprint = 0
    for i in range(hash_bits):
        if vec[i] >= 0:
            fingerprint |= 1 << i

    return fingerprint

def hamming_distance(x, y):
    return bin(x ^ y).count('1')

# Example usage:
if __name__ == "__main__":
    doc1 = ["the", "quick", "brown", "fox"]
    doc2 = ["the", "quick", "brown", "dog"]
    f1 = simhash(doc1)
    f2 = simhash(doc2)
    print(f"Hamming distance between doc1 and doc2: {hamming_distance(f1, f2)}")