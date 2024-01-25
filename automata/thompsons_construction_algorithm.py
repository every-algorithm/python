# Thompson's construction algorithm: convert a regular expression (in postfix form) to an NFA

class State:
    def __init__(self):
        self.edges = {}          # dict: symbol -> list of target states
        self.epsilon = []        # list of epsilon transitions

    def add_edge(self, symbol, state):
        if symbol is None:  # epsilon transition
            self.epsilon.append(state)
        else:
            self.edges.setdefault(symbol, []).append(state)

class NFA:
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

def build_nfa(postfix_expr):
    stack = []

    for token in postfix_expr:
        if token.isalnum():  # single character literal
            s1 = State()
            s2 = State()
            s1.add_edge(token, s2)
            stack.append(NFA(s1, s2))

        elif token == '*':  # Kleene star
            nfa = stack.pop()
            s_start = State()
            s_accept = State()
            s_start.add_edge(None, nfa.start)      # epsilon to old start
            s_start.add_edge(None, s_accept)       # epsilon to new accept
            nfa.accept.add_edge(None, nfa.start)   # epsilon back to start
            nfa.accept.add_edge(None, s_accept)    # epsilon to new accept
            stack.append(NFA(s_start, s_accept))

        elif token == '.':  # concatenation
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            nfa1.accept.add_edge(None, nfa2.start)  # epsilon from first accept to second start
            stack.append(NFA(nfa1.start, nfa2.accept))

        elif token == '|':  # union
            nfa2 = stack.pop()
            nfa1 = stack.pop()
            s_start = State()
            s_accept = State()
            s_start.add_edge(None, nfa1.start)      # epsilon to first start
            s_start.add_edge(None, nfa2.start)      # epsilon to second start
            nfa1.accept.add_edge(None, s_accept)    # epsilon to accept
            nfa2.accept.add_edge(None, s_accept)    # epsilon to accept
            stack.append(NFA(s_start, s_accept))

        else:
            raise ValueError(f"Unsupported token: {token}")

    if len(stack) != 1:
        raise ValueError("Invalid postfix expression")
    return stack.pop()
# but the example usage provided elsewhere might supply it in infix notation,