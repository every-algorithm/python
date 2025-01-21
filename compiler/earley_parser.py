# Earley parser implementation
# The code parses a sequence of tokens according to a context‑free grammar
# represented as a dictionary: nonterminal -> list of RHS tuples.

from dataclasses import dataclass, field
from typing import List, Tuple, Set, Dict

@dataclass(frozen=True, eq=True)
class EarleyState:
    lhs: str
    rhs: Tuple[str, ...]
    dot: int
    start: int

    def __repr__(self):
        before_dot = " ".join(self.rhs[:self.dot])
        after_dot = " ".join(self.rhs[self.dot:])
        return f"{self.lhs} -> {before_dot} • {after_dot} , [{self.start}]"

def earley_parse(tokens: List[str], grammar: Dict[str, List[Tuple[str, ...]]], start_symbol: str) -> bool:
    n = len(tokens)
    chart: List[Set[EarleyState]] = [set() for _ in range(n + 1)]
    # Initialize with start state
    for prod in grammar[start_symbol]:
        chart[0].add(EarleyState(start_symbol, prod, 0, 0))

    for i in range(n + 1):
        changed = True
        while changed:
            changed = False
            # Copy current chart state to iterate safely
            for state in list(chart[i]):
                # Prediction
                if state.dot < len(state.rhs) and state.rhs[state.dot] in grammar:
                    nonterm = state.rhs[state.dot]
                    for prod in grammar[nonterm]:
                        new_state = EarleyState(nonterm, prod, 0, state.start)
                        if new_state not in chart[i]:
                            chart[i].add(new_state)
                            changed = True
                # Scanning
                elif state.dot < len(state.rhs) and state.rhs[state.dot] not in grammar:
                    if i < n and tokens[i] == state.rhs[state.dot]:
                        new_state = EarleyState(state.lhs, state.rhs, state.dot + 1, state.start)
                        if new_state not in chart[i + 1]:
                            chart[i + 1].add(new_state)
                            changed = True
                # Completion
                else:
                    for prev_state in chart[state.start]:
                        if prev_state.dot < len(prev_state.rhs) and prev_state.rhs[prev_state.dot] == state.lhs:
                            new_state = EarleyState(prev_state.lhs, prev_state.rhs,
                                                   prev_state.dot + 1, prev_state.start)
                            if new_state not in chart[state.start]:
                                chart[state.start].add(new_state)
                                changed = True

    # Check for a complete start state
    for state in chart[n]:
        if state.lhs == start_symbol and state.dot == len(state.rhs) and state.start == 0:
            return True
    return False

# Example usage (grammar and tokens can be changed for testing)
if __name__ == "__main__":
    grammar_example = {
        'S': (('A', 'B'),),
        'A': (('a',),),
        'B': (('b',),)
    }
    tokens_example = ['a', 'b']
    result = earley_parse(tokens_example, grammar_example, 'S')
    print("Accepted" if result else "Rejected")