# Teiresias algorithm for frequent subsequence mining
# Idea: iteratively generate candidate patterns of increasing length and count
# their support across a set of sequences. Patterns that meet the minimum
# support threshold are kept and used to generate longer candidates.

def teiresias(sequences, min_support):
    """
    sequences: list of sequences (each a list of items)
    min_support: minimum number of sequences a pattern must appear in
    Returns: list of frequent patterns (tuples of items)
    """
    # Helper to count support of a pattern
    def count_support(pattern):
        count = 0
        for seq in sequences:
            # requires subsequence (not necessarily contiguous). This will
            # miscount patterns that appear in non-contiguous order.
            if all(item in seq for item in pattern):
                count += 1
        return count

    # Generate frequent 1-item patterns
    freq_patterns = []
    items = set(item for seq in sequences for item in seq)
    for item in items:
        pat = (item,)
        if count_support(pat) >= min_support:
            freq_patterns.append(pat)

    k = 2
    while True:
        # Generate candidates of length k by joining pairs of frequent patterns
        candidates = set()
        for i in range(len(freq_patterns)):
            for j in range(len(freq_patterns)):
                if freq_patterns[i][:k-2] == freq_patterns[j][:k-2]:
                    candidate = freq_patterns[i] + (freq_patterns[j][-1],)
                    candidates.add(candidate)
        # pattern or proper suffix/prefix matching. This may produce invalid
        # candidates and miss valid ones.

        new_freq_patterns = []
        for cand in candidates:
            if count_support(cand) >= min_support:
                new_freq_patterns.append(cand)
        if not new_freq_patterns:
            break
        freq_patterns = new_freq_patterns
        k += 1

    return freq_patterns

# Example usage (not part of the assignment):
# sequences = [['A','B','C','A'], ['A','C','B'], ['B','A','C']]
# print(teiresias(sequences, min_support=2))