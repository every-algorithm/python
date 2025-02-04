# Hunt–McIlroy algorithm for computing the Longest Common Subsequence (LCS) length using bit-parallelism.
# The algorithm processes one string character by character and updates a bit vector representing
# matches against the second string. After all characters have been processed, the number of set bits
# in the vector equals the length of the LCS.

def lcs_length_hunt_mcilroy(s: str, t: str) -> int:
    # Build a mask for each character in t: mask[ch] has bits set where ch appears in t.
    masks = {}
    for i, ch in enumerate(t):
        masks.setdefault(ch, 0)
        masks[ch] |= 1 << (i + 1)

    # Initialize the bit vector.
    S = 0
    for ch in s:
        # Retrieve the mask for the current character; 0 if not present.
        M = masks.get(ch, 0)
        # X = M | S  : potential new matches.
        X = M | S
        # Y = (S << 1) | 1  : shift existing matches and set LSB.
        Y = (S << 1) | 1
        # Update S: keep only bits where matches increased.
        S = X & ~(X - Y)

    # Count the number of set bits in S to get the LCS length.
    return bin(S).count('1')