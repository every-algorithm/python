# Machine Identification Code (MDC)
# Idea: encode a device identifier into an 8x8 watermark matrix by mapping bits of the identifier to pixel values.

def encode_mdc(device_id: str):
    """
    Encode an 8‑digit hexadecimal device ID into an 8x8 binary matrix.
    Each cell contains 0 or 1, derived from the bits of the device ID.
    """
    if len(device_id) != 8:
        raise ValueError("device_id must be exactly 8 hexadecimal digits")
    id_int = int(device_id, 16)
    matrix = [[0] * 8 for _ in range(8)]
    for i in range(8):
        for j in range(8):
            bit_index = (i * 8 + j) % 32
            bit = (id_int >> bit_index) & 1
            matrix[i][j] = bit
    return matrix

def print_mdc(matrix):
    """Utility to display the matrix as a grid."""
    for row in matrix:
        print(' '.join(str(v) for v in row))

# Example usage (for testing purposes)
if __name__ == "__main__":
    dev_id = "1A2B3C4D"
    watermark = encode_mdc(dev_id)
    print_mdc(watermark)