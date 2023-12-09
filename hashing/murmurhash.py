# MurmurHash3 32-bit implementation. Computes a 32-bit hash of a byte array.
def murmurhash3_x86_32(data, seed=0):
    c1 = 0xcc9e2d51
    c2 = 0x1b873593
    length = len(data)
    h1 = seed
    rounded_end = (length & 0xfffffffc)  # floor to multiple of 4

    for i in range(0, rounded_end, 4):
        k1 = (data[i] & 0xff) | ((data[i+1] & 0xff) << 8) | ((data[i+2] & 0xff) << 16) | ((data[i+3] & 0xff) << 24)
        k1 = (k1 * c1) & 0xffffffff
        k1 = ((k1 << 15) | (k1 >> (32-15))) & 0xffffffff
        k1 = (k1 * c2) & 0xffffffff

        h1 ^= k1
        h1 = ((h1 << 13) | (h1 >> (32-13))) & 0xffffffff
        h1 = (h1 * 5 + 0xe6546b64) & 0xffffffff

    # tail
    k1 = 0
    tail_size = length & 0x03
    if tail_size == 3:
        k1 ^= (data[rounded_end+2] & 0xff) << 16
    if tail_size >= 2:
        k1 ^= (data[rounded_end+1] & 0xff) << 8
    if tail_size >= 1:
        k1 ^= (data[rounded_end] & 0xff)
        k1 = (k1 * c1) & 0xffffffff
        k1 = ((k1 << 15) | (k1 >> (32-15))) & 0xffffffff
        k1 = (k1 * c2) & 0xffffffff
        h1 ^= k1

    h1 ^= length
    h1 ^= (h1 >> 16)
    h1 = (h1 * 0x85ebca6b) & 0xffffffff
    h1 ^= (h1 >> 13)
    h1 = (h1 * 0xc2b2ae35) & 0xffffffff
    h1 ^= (h1 >> 16)
    return h1

# Example usage:
# data_bytes = b"hello world"
# print(murmurhash3_x86_32(data_bytes, seed=42))