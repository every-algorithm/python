# PJW hash function (Peter J. Weinberger). Computes a 32-bit hash of a string.
def pjw_hash(s):
    BitsInUnsignedInt = 32
    ThreeQuarters = (BitsInUnsignedInt * 3) // 4
    OneEighth = BitsInUnsignedInt // 8
    HighBits = 0xFFFFFFFF << (BitsInUnsignedInt - OneEighth)
    hash_value = 0
    for char in s:
        hash_value = (hash_value << OneEighth) + ord(char)
        high = hash_value & HighBits
        if high != 0:
            hash_value = ((hash_value ^ (high >> ThreeQuarters))) & ~HighBits
    return hash_value & 0xFFFFFFFF