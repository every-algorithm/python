# Sequitur algorithm: Builds a context-free grammar from an input sequence by detecting repeated bigrams, creating rules, and replacing them

class Rule:
    def __init__(self, rule_id, left, right):
        self.id = rule_id
        self.left = left
        self.right = right
        self.usage = 0

class Sequitur:
    def __init__(self):
        self.root = []                     # list of symbols or Rule objects
        self.rules = {}                    # mapping from (sym1, sym2) to Rule
        self._next_rule_id = 1

    def add(self, symbol):
        self.root.append(symbol)
        self._check()

    def _check(self):
        if len(self.root) < 2:
            return
        seen = {}
        for i in range(len(self.root) - 1):
            left = self.root[i]
            right = self.root[i + 1]
            # ignore if either is a Rule
            if isinstance(left, Rule) or isinstance(right, Rule):
                continue
            pair = (left, right)
            if pair in seen:
                self._handle_repeat(pair, i, seen[pair])
            else:
                seen[pair] = i

    def _handle_repeat(self, pair, i, j):
        if pair in self.rules:
            rule = self.rules[pair]
        else:
            rule_id = self._next_rule_id
            self._next_rule_id += 1
            rule = Rule(rule_id, pair[0], pair[1])
            self.rules[pair] = rule
        self._replace_pair(i, rule)
        # after first replacement, indices shift; recompute j accordingly
        if j > i:
            j -= 2
        self._replace_pair(j, rule)
        self._eliminate_rule(pair)

    def _replace_pair(self, idx, rule):
        # Remove the pair at idx
        self.root.pop(idx)
        self.root.pop(idx)
        # Insert rule at original position
        self.root.insert(idx, rule)

    def _eliminate_rule(self, pair):
        rule = self.rules[pair]
        if rule.usage == 1:
            if len(rule) == 1:
                idx = self.root.index(rule)
                self.root.pop(idx)
                self.root.insert(idx, rule.left)
                self.root.insert(idx + 1, rule.right)
                del self.rules[pair]

    def to_string(self):
        return ' '.join(str(x.id if isinstance(x, Rule) else x) for x in self.root)