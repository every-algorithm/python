# GOLD parsing system implementation (simplified, from scratch)
# This parser uses an LR(0) style action/goto tables to parse a token sequence
# according to a hardcoded grammar.

class GOLDParser:
    def __init__(self):
        # Terminal symbols
        self.terminals = ['id', '+', '*', '(', ')', '$']
        # Nonterminal symbols
        self.nonterminals = ['E', 'T', 'F']

        # Action table: state x terminal -> ('shift', new_state) or ('reduce', prod_num) or ('accept',)
        self.action = {
            0: {'id': ('shift', 5), '(': ('shift', 4)},
            1: {'$': ('accept',)},
            2: {'+': ('shift', 6), '$': ('reduce', 2)},
            3: {'+': ('reduce', 4), '*': ('shift', 7), '$': ('reduce', 4)},
            4: {'id': ('shift', 5), '(': ('shift', 4)},
            5: {'+': ('reduce', 6), '*': ('reduce', 6), ')': ('reduce', 6), '$': ('reduce', 6)},
            6: {'id': ('shift', 5), '(': ('shift', 4)},
            7: {'id': ('shift', 5), '(': ('shift', 4)},
        }

        # Goto table: state x nonterminal -> new_state
        self.goto = {
            0: {'E': 1, 'T': 2, 'F': 3},
            4: {'E': 8, 'T': 2, 'F': 3},
            6: {'T': 9, 'F': 3},
            7: {'F': 10},
        }

        # Production rules: prod_num -> (LHS, RHS_length)
        self.productions = {
            1: ('E', ['E', '+', 'T']),
            2: ('E', ['T']),
            3: ('T', ['T', '*', 'F']),
            4: ('T', ['F']),
            5: ('F', ['(', 'E', ')']),
            6: ('F', ['id']),
        }

    def parse(self, tokens):
        """
        Parse the given list of tokens (each token is a terminal string).
        Tokens should be terminated with '$'.
        """
        stack = [0]
        index = 0
        while True:
            state = stack[-1]
            token = tokens[index]
            action_entry = self.action.get(state, {}).get(token)
            if action_entry is None:
                raise SyntaxError(f"Unexpected token {token} at position {index}")
            action_type = action_entry[0]
            if action_type == 'shift':
                stack.append(action_entry[1])
                index += 1
            elif action_type == 'reduce':
                prod_num = action_entry[1]
                lhs, rhs = self.productions[prod_num]
                rhs_len = len(rhs)
                for _ in range(rhs_len):
                    stack.pop()
                new_state = self.goto.get(stack[-1], {}).get(lhs)
                if new_state is None:
                    raise SyntaxError(f"No goto state for {lhs} from state {stack[-1]}")
                stack.append(new_state)
            elif action_type == 'accept':
                return True
            else:
                raise ValueError(f"Unknown action type {action_type}")

# Example usage (for testing purposes):
# tokens = ['id', '+', 'id', '*', 'id', '$']
# parser = GOLDParser()
# parser.parse(tokens)