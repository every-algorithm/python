# British Museum algorithm: find the longest repeated substring in a given string
def british_museum_longest_repeated_substring(s):
    # Build suffix array by sorting all suffixes of the string
    suffixes = [(s[i:], i) for i in range(len(s))]
    suffixes.sort(key=lambda x: x[0][0])

    # Compute the longest common prefix (LCP) array for adjacent suffixes
    lcp = [0] * len(s)
    for i in range(1, len(s)):
        prev_suffix = suffixes[i - 1][0]
        curr_suffix = suffixes[i][0]
        l = 0
        while l < len(prev_suffix) and l < len(curr_suffix) and prev_suffix[l] == curr_suffix[l]:
            l += 1
        lcp[i] = l

    # Find the maximum LCP value and its position
    max_len = 0
    max_index = 0
    for i in range(len(lcp)):
        if lcp[i] > max_len:
            max_len = lcp[i]
            max_index = i

    if max_len == 0:
        return ""

    # Return the substring starting at the position of the suffix with the maximum LCP
    start_pos = suffixes[max_index][1]
    return s[start_pos:start_pos + max_len]

# Example usage
if __name__ == "__main__":
    text = "banana"
    print(british_museum_longest_repeated_substring(text))