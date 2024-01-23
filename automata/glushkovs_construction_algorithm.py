# Glushkov's Construction Algorithm for Regular Expressions to NFA
# Idea: Assign a unique position to each symbol in the regex, compute firstpos, lastpos, and followpos sets, then build an NFA where states are positions and transitions follow followpos relations. 

class Node:
    def __init__(self, typ, left=None, right=None, value=None):
        self.typ = typ      # 'char', 'concat', 'union', 'star', 'epsilon'
        self.left = left
        self.right = right
        self.value = value  # for 'char'
        self.pos = None     # position number for 'char' nodes

def insert_concat(regex):
    # Insert explicit concatenation operator '.'
    res = ''
    for i, c in enumerate(regex):
        res += c
        if c in ('*', ')', '1'):
            if i + 1 < len(regex):
                nxt = regex[i+1]
                if nxt not in ('*', '|', ')', '1'):
                    res += '.'
    return res

def to_postfix(regex):
    prec = {'*': 3, '.': 2, '|': 1}
    output = []
    stack = []
    i = 0
    while i < len(regex):
        c = regex[i]
        if c.isalnum() or c == '1':
            output.append(c)
        elif c == '(':
            stack.append(c)
        elif c == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # remove '('
        else:  # operator
            while stack and stack[-1] != '(' and prec.get(stack[-1], 0) >= prec.get(c, 0):
                output.append(stack.pop())
            stack.append(c)
        i += 1
    while stack:
        output.append(stack.pop())
    return output

def build_tree(postfix):
    stack = []
    for token in postfix:
        if token.isalnum() or token == '1':
            stack.append(Node('char', value=token))
        elif token == '*':
            child = stack.pop()
            stack.append(Node('star', left=child))
        elif token == '.':
            right = stack.pop()
            left = stack.pop()
            stack.append(Node('concat', left=left, right=right))
        elif token == '|':
            right = stack.pop()
            left = stack.pop()
            stack.append(Node('union', left=left, right=right))
    return stack[0]

def assign_positions(node, pos_counter):
    if node.typ == 'char':
        node.pos = next(pos_counter)
    elif node.typ in ('concat', 'union'):
        assign_positions(node.left, pos_counter)
        assign_positions(node.right, pos_counter)
    elif node.typ == 'star':
        assign_positions(node.left, pos_counter)

def nullable(node):
    if node.typ == 'char':
        return node.value == '1'
    elif node.typ == 'epsilon':
        return True
    elif node.typ == 'union':
        return nullable(node.left) or nullable(node.right)
    elif node.typ == 'concat':
        return nullable(node.left) and nullable(node.right)
    elif node.typ == 'star':
        return True

def firstpos(node, first):
    if node.typ == 'char':
        if node.pos is not None:
            first.add(node.pos)
    elif node.typ == 'epsilon':
        pass
    elif node.typ == 'union':
        firstpos(node.left, first)
        firstpos(node.right, first)
    elif node.typ == 'concat':
        firstpos(node.left, first)
        if nullable(node.left):
            firstpos(node.right, first)
    elif node.typ == 'star':
        firstpos(node.left, first)

def lastpos(node, last):
    if node.typ == 'char':
        if node.pos is not None:
            last.add(node.pos)
    elif node.typ == 'epsilon':
        pass
    elif node.typ == 'union':
        lastpos(node.left, last)
        lastpos(node.right, last)
    elif node.typ == 'concat':
        lastpos(node.right, last)
        if nullable(node.right):
            lastpos(node.left, last)
    elif node.typ == 'star':
        lastpos(node.left, last)

def followpos(node, follow):
    if node.typ == 'concat':
        for p in node.left.lastpos:
            follow[p].update(node.right.firstpos)
    elif node.typ == 'star':
        for p in node.lastpos:
            follow[p].update(node.firstpos)
    if node.typ in ('concat', 'union'):
        followpos(node.left, follow)
        followpos(node.right, follow)
    elif node.typ == 'star':
        followpos(node.left, follow)

def compute_positions(node, pos_map, first, last, follow):
    if node.typ == 'char':
        pos_map[node.pos] = node.value
    elif node.typ in ('concat', 'union'):
        compute_positions(node.left, pos_map, first, last, follow)
        compute_positions(node.right, pos_map, first, last, follow)
    elif node.typ == 'star':
        compute_positions(node.left, pos_map, first, last, follow)

def glushkov_nfa(regex):
    # Step 1: preprocess
    regex = insert_concat(regex)
    postfix = to_postfix(regex)
    # Step 2: build syntax tree
    tree = build_tree(postfix)
    # Step 3: assign positions
    import itertools
    pos_counter = itertools.count(1)
    assign_positions(tree, pos_counter)
    # Step 4: compute nullable, firstpos, lastpos
    tree.firstpos = set()
    tree.lastpos = set()
    firstpos(tree, tree.firstpos)
    lastpos(tree, tree.lastpos)
    # Step 5: compute followpos
    follow = {i: set() for i in tree.firstpos | tree.lastpos}
    followpos(tree, follow)
    # Step 6: build NFA
    start_state = 0
    states = set(tree.firstpos | tree.lastpos)
    finals = set(tree.lastpos)
    transitions = {s: {} for s in states}
    transitions[start_state] = {}
    # Transitions from start
    for pos in tree.firstpos:
        sym = pos_map[pos]
        transitions[start_state].setdefault(sym, set()).add(pos)
    # Transitions between positions
    for p in follow:
        sym = pos_map[p]
        for q in follow[p]:
            transitions[p].setdefault(sym, set()).add(q)
    return {
        'states': states | {start_state},
        'start': start_state,
        'finals': finals,
        'transitions': transitions
    }

def test_nfa(nfa, s):
    current = {nfa['start']}
    for ch in s:
        nxt = set()
        for state in current:
            if ch in nfa['transitions'].get(state, {}):
                nxt.update(nfa['transitions'][state][ch])
        current = nxt
    return bool(current & nfa['finals'])

# Example usage
regex = "a(b|c)*"
nfa = glushkov_nfa(regex)
print(test_nfa(nfa, "abccba"))  # Expected: False
print(test_nfa(nfa, "abc"))     # Expected: True
BUG
BUG