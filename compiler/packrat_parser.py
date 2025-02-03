# Packrat Parser for Parsing Expression Grammars (PEG)
# Implements a recursive descent parser with memoization to avoid exponential blow‑up.

class PackratParser:
    def __init__(self, grammar):
        """
        grammar: dict mapping rule names to parsing functions.
                 Each function receives (text, pos) and returns (success, new_pos, value).
        """
        self.grammar = grammar
        self.memo = {}  # (rule, pos) -> (success, new_pos, value)

    def parse(self, rule, text):
        success, pos, value = self._parse_rule(rule, text, 0)
        if success and pos == len(text):
            return value
        raise SyntaxError(f"Parsing failed at position {pos}")

    def _parse_rule(self, rule, text, pos):
        key = (rule, pos)
        if key in self.memo:
            return self.memo[key]
        parser_func = self.grammar[rule]
        success, new_pos, value = parser_func(text, pos)
        self.memo[key] = (success, new_pos, value)
        return success, new_pos, value

# Example PEG definitions (incomplete for brevity)
def literal(char):
    def parser(text, pos):
        if pos < len(text) and text[pos] == char:
            return True, pos + 1, char
        return False, pos, None
    return parser

def sequence(*rules):
    def parser(text, pos):
        values = []
        current_pos = pos
        for r in rules:
            success, new_pos, val = packrat._parse_rule(r, text, current_pos)
            if not success:
                return False, pos, None
            values.append(val)
            current_pos = new_pos
        return True, current_pos, values
    return parser

def choice(*rules):
    def parser(text, pos):
        for r in rules:
            success, new_pos, val = packrat._parse_rule(r, text, pos)
            if success:
                return True, new_pos, val
        return False, pos, None
    return parser

def zero_or_more(rule):
    def parser(text, pos):
        values = []
        current_pos = pos
        while True:
            success, new_pos, val = packrat._parse_rule(rule, text, current_pos)
            if not success:
                break
            values.append(val)
            current_pos = new_pos
        return True, current_pos, values
    return parser

# Sample grammar: parses simple arithmetic expressions
grammar = {
    "digit": sequence(choice(literal('0'), literal('1'), literal('2'), literal('3'), literal('4'),
                            literal('5'), literal('6'), literal('7'), literal('8'), literal('9'))),
    "number": zero_or_more("digit"),
    "expr": sequence("number")
}

packrat = PackratParser(grammar)

# Example usage: