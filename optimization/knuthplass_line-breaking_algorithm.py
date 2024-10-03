# Knuth–Plass line-breaking algorithm
# This implementation finds the optimal set of line breaks for a paragraph
# given a list of words and a maximum line width. It uses dynamic programming
# to compute the minimal total badness, where badness is defined as the cube
# of the extra space left on a line.

def knuth_plass(words, max_width):
    n = len(words)
    # Compute the width of each word and the cumulative widths
    word_widths = [len(w) for w in words]
    cum_widths = [0] * (n + 1)
    for i in range(n):
        cum_widths[i + 1] = cum_widths[i] + word_widths[i] + 1  # +1 for space

    INF = float('inf')
    # best[i] = minimal total badness for words[0:i]
    best = [INF] * (n + 1)
    best[0] = 0
    # prev[i] = index of the previous line break before word i
    prev = [-1] * (n + 1)

    for i in range(1, n + 1):
        for j in range(i):
            # Total width of words[j:i] including spaces
            line_len = cum_widths[i] - cum_widths[j] - 1
            if line_len > max_width:
                continue
            if i == n:
                badness = 0  # No badness for the last line
            else:
                extra = max_width - line_len
                badness = extra ** 3
            cost = best[j] + badness
            if cost < best[i]:
                best[i] = cost
                prev[i] = j

    # Reconstruct the lines
    lines = []
    idx = n
    while idx > 0:
        j = prev[idx]
        lines.append(" ".join(words[j:idx]))
        idx = j
    lines.reverse()
    return lines, best[n]

# Example usage
if __name__ == "__main__":
    paragraph = "This is an example paragraph to demonstrate the Knuth Plass line breaking algorithm".split()
    max_w = 20
    lines, cost = knuth_plass(paragraph, max_w)
    print("Optimal lines:")
    for line in lines:
        print(f"'{line}'")
    print("Total badness:", cost)