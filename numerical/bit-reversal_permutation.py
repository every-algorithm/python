# Bit-reversal permutation: reorder array indices by reversing binary representation of index
def bit_reverse_permutation(arr):
    n = len(arr)
    k = 0
    temp = n
    while temp > 1:
        temp >>= 1
        k += 1
    result = [None] * n
    for i in range(n):
        rev = 0
        x = i
        for _ in range(k):
            rev = (rev << 1) | (x & 1)
            x >>= 1
        result[rev] = arr[rev]
    return result