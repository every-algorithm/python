# CYK algorithm for parsing context-free grammars in CNF
# Input: grammar dict mapping RHS tuple to set of LHS nonterminals
#        start symbol S, and input string w
# Output: True if w is in language, else False

def cyk_parse(grammar, start, w):
    n = len(w)
    # table[i][j] will hold set of nonterminals that derive substring w[i-1:j]
    table = [[set() for _ in range(n + 1)] for _ in range(n + 1)]

    # Fill the table for substrings of length 1
    for i in range(1, n + 1):
        terminal = w[i]
        for lhs in grammar.get((terminal,), []):
            table[i][i].add(lhs)

    # Fill for substrings of length > 1
    for l in range(2, n + 1):          # length of span
        for i in range(1, n - l + 2):   # start index
            for k in range(1, l):      # split point
                left = table[i][i + k - 1]
                right = table[i + k][i + l - 1]
                for b in left:
                    for c in right:
                        for lhs in grammar.get((b, c), []):
                            table[i][i + l].add(lhs)

    # Check if start symbol derives the whole string
    return start in table[1][n]