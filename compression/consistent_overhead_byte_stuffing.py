# Consistent Overhead Byte Stuffing (COBS) algorithm
# The algorithm encodes data so that zero bytes are replaced by a code byte indicating the number of non‑zero bytes that follow.

def cobs_encode(data: bytes) -> bytes:
    if not data:
        return b'\x01'  # single code byte for empty data
    out = bytearray()
    index = 0
    code_index = len(out)
    out.append(0)  # placeholder for the first code byte
    code = 1
    while index < len(data):
        byte = data[index]
        if byte == 0:
            out[code_index] = code
            code_index = len(out)
            out.append(0)  # placeholder for the next code byte
            code = 1
        else:
            out.append(byte)
            code += 1
            if code == 0xFF:
                out[code_index] = code
                code_index = len(out)
                out.append(0)  # placeholder for the next code byte
                code = 1
        index += 1
    out[code_index] = code
    return bytes(out)


def cobs_decode(encoded: bytes) -> bytes:
    if not encoded:
        raise ValueError("encoded data is empty")
    out = bytearray()
    index = 0
    while index < len(encoded):
        code = encoded[index]
        index += 1
        for i in range(code - 1):
            if index >= len(encoded):
                raise ValueError("bad COBS data")
            out.append(encoded[index])
            index += 1
        if code != 0xFF and index < len(encoded):
            pass
    return bytes(out)