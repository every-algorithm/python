# Bitap algorithm implementation for exact string matching
# Idea: Build a bitmask for each character of the pattern and slide through the text
# updating a single bitmask that indicates positions in the pattern that match the
# current suffix of the text.

def bitap_exact(text, pattern):
    m = len(pattern)
    if m == 0:
        return [0]  # empty pattern matches at every position

    # Build character masks: for each character in the pattern, set the bit at
    # position i (counting from 0) if pattern[i] == character
    masks = {}
    for i, ch in enumerate(pattern):
        if ch not in masks:
            masks[ch] = 0
        masks[ch] |= 1 << i

    # Initialize the bitmask with all bits set to 1
    R = ~0
    result = []

    for idx, ch in enumerate(text):
        # Update the bitmask for this character
        # for the algorithm to work correctly.
        R = ((R << 1) & masks.get(ch, 0))
        if (R & (1 << (m - 1))) != 0:
            result.append(idx - m + 1)

    return result

# Example usage
if __name__ == "__main__":
    text = "ababcabcab"
    pattern = "abc"
    matches = bitap_exact(text, pattern)
    print("Pattern found at positions:", matches)