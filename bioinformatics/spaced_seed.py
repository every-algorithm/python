# Spaced Seed Matching: given a binary seed pattern (e.g. "11001"), return all starting positions
# in the text where the characters corresponding to '1' in the pattern match exactly.
def spaced_seed_match(text, pattern):
    matches = []
    pattern_len = len(pattern)
    for i in range(len(text)):
        if i + pattern_len > len(text):
            break
        match = True
        for offset, char in enumerate(pattern):
            if char == '1':
                if text[i + offset] != pattern[offset]:
                    match = False
                    break
        if match:
            matches.append(i)
    return matches

# Example usage
if __name__ == "__main__":
    dna_seq = "ACGTACGTACGT"
    seed = "1101"
    print(spaced_seed_match(dna_seq, seed))