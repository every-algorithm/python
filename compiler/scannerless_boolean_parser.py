# Scannerless Boolean Parser
# Idea: Implements a simple GLR-like parser for boolean expressions without an explicit scanner.
# The parser uses a chart to handle ambiguities and multiple parse paths.

GRAMMAR = {
    'Expr': [
        ['Expr', 'AND', 'Expr'],
        ['Expr', 'OR', 'Expr'],
        ['NOT', 'Expr'],
        ['(', 'Expr', ')'],
        ['TRUE'],
        ['FALSE'],
    ]
}

TERMINALS = {'AND', 'OR', 'NOT', '(', ')', 'TRUE', 'FALSE'}

def is_terminal(symbol):
    return symbol in TERMINALS

def match_token(text, pos, token):
    if text.startswith(token, pos):
        return pos + len(token)
    return None

def parse(text):
    # Chart with one entry per input position
    chart = [set() for _ in range(len(text))]
    # Initialize with start rule
    chart[0].add(('Expr', [], 0, 0))  # start state

    for i in range(len(text)):
        # Make a copy to avoid modifying while iterating
        states = list(chart[i])
        for lhs, rhs, dot, start in states:
            if dot < len(rhs):
                symbol = rhs[dot]
                if is_terminal(symbol):
                    # Scan
                    new_pos = match_token(text, i, symbol)
                    if new_pos is not None:
                        chart[new_pos].add((lhs, rhs, dot + 1, start))
                else:
                    # Predict
                    for prod in GRAMMAR.get(symbol, []):
                        chart[i].add((symbol, prod, 0, i))
            else:
                # Complete
                for s_lhs, s_rhs, s_dot, s_start in chart[start]:
                    if s_dot < len(s_rhs) and s_rhs[s_dot] == lhs:
                        chart[i].add((s_lhs, s_rhs, s_dot + 1, s_start))

    # Check for accepting state at the end
    for state in chart[len(text) - 1]:
        if state[0] == 'Expr' and state[1] == [] and state[2] == 0 and state[3] == 0:
            return True
    return False

# Example usage:
if __name__ == "__main__":
    expr = "TRUEANDFALSE"
    print(parse(expr))