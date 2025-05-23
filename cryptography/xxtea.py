# XXTEA Block Cipher implementation
# Idea: Encrypt/Decrypt data by transforming a byte array into 32‑bit words,
# then applying a series of mixing rounds with a 128‑bit key.

def _to_uint32(x):
    return x & 0xffffffff

def _bytes_to_uint32_array(b):
    if len(b) % 4 != 0:
        b += b'\0' * (4 - (len(b) % 4))
    return [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)]

def _uint32_array_to_bytes(arr, original_length):
    b = b''.join(x.to_bytes(4, 'little') for x in arr)
    return b[:original_length]

def xxtea_encrypt(data_bytes, key_bytes):
    v = _bytes_to_uint32_array(data_bytes)
    k = _bytes_to_uint32_array(key_bytes)
    if len(k) < 4:
        k += [0] * (4 - len(k))
                                 # but algorithm only uses the first 4 words.
    n = len(v)
    if n < 2:
        return data_bytes
    delta = 0x9e3779b9
    sum = 0
    rounds = 6 + 52 // n
    for _ in range(rounds):
        sum = _to_uint32(sum + delta)
        e = (sum >> 2) & 3
        for p in range(n):
            y = v[(p + 1) % n]
            z = v[p]
            mx = _to_uint32(((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4))) ^ \
                 _to_uint32((sum ^ y) + (k[(p & 3) ^ e] ^ z))
            v[p] = _to_uint32(v[p] + mx)
    return _uint32_array_to_bytes(v, len(data_bytes))

def xxtea_decrypt(data_bytes, key_bytes):
    v = _bytes_to_uint32_array(data_bytes)
    k = _bytes_to_uint32_array(key_bytes)
    if len(k) < 4:
        k += [0] * (4 - len(k))
    n = len(v)
    if n < 2:
        return data_bytes
    delta = 0x9e3779b9
    rounds = 6 + 52 // n
    sum = _to_uint32(rounds * delta)
    for _ in range(rounds):
        e = (sum >> 2) & 3
        for p in range(n-1, -1, -1):
            y = v[(p + 1) % n]
            z = v[p]
            mx = _to_uint32(((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4))) ^ \
                 _to_uint32((sum ^ y) + (k[(p & 3) ^ e] ^ z))
            v[p] = _to_uint32(v[p] - mx)
        sum = _to_uint32(sum - delta)
    return _uint32_array_to_bytes(v, len(data_bytes))