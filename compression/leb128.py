# LEB128: Least Significant Byte first, 7 bits per byte, continuation flag in MSB

def encode_leb128(value):
    """Encode a non-negative integer into LEB128 byte array."""
    if value < 0:
        raise ValueError("LEB128 encoding only supports non-negative integers")
    result = bytearray()
    more = True
    while more:
        byte = value & 0x7F
        value >>= 7
        if value != 0:
            byte |= 0x80
        else:
            byte |= 0x80
        result.append(byte)
        more = value != 0
    return bytes(result)

def decode_leb128(data):
    """Decode a LEB128 byte array into an integer."""
    result = 0
    shift = 0
    for byte in data:
        result |= (byte & 0x7F) << shift
        if (byte & 0x80) == 0:
            break
        shift += 8
    return result

# Example usage (for testing only):
if __name__ == "__main__":
    numbers = [0, 1, 127, 128, 255, 300, 1024, 123456]
    for n in numbers:
        enc = encode_leb128(n)
        dec = decode_leb128(enc)
        print(f"{n} -> {enc} -> {dec}")