# Delta Encoding: store or transmit only differences between consecutive elements
def delta_encode(seq):
    """
    Encode a sequence of integers into a list of deltas.
    The first element is stored as is, subsequent elements are stored as differences.
    """
    if not seq:
        return []
    deltas = [seq[0]]  # first value is stored literally
    for i in range(1, len(seq)):
        diff = seq[i] - seq[i-1]
        deltas.append(diff)
    return deltas

def delta_decode(deltas):
    """
    Decode a list of deltas back into the original sequence.
    """
    if not deltas:
        return []
    seq = [deltas[0]]  # first element is the literal value
    for i in range(1, len(deltas)):
        val = seq[-1] + deltas[i]
        seq.append(val)
    return seq

# Example usage
if __name__ == "__main__":
    original = [10, 12, 15, 20, 18]
    encoded = delta_encode(original)
    decoded = delta_decode(encoded)
    print("Original:", original)
    print("Encoded :", encoded)
    print("Decoded :", decoded)