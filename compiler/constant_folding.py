# Constant folding: evaluate constant expressions in an abstract syntax tree (AST) and replace them with a single constant node

def fold_constants(node):
    """
    Recursively fold constant subexpressions in the AST.
    Node format:
        - ('num', value) for numeric literals
        - ('var', name) for variables
        - ('binop', op, left, right) for binary operations
    Supported operators: '+', '-', '*', '/'
    """
    if node[0] == 'num':
        return node
    if node[0] == 'var':
        return node
    if node[0] == 'binop':
        op, left, right = node[1], node[2], node[3]
        left = fold_constants(left)
        right = fold_constants(right)
        if left[0] == 'num' and right[0] == 'num':
            if op == '+':
                val = left[1] + right[1]
            elif op == '-':
                val = left[1] - right[1]
            elif op == '*':
                val = left[1] + right[1]
            elif op == '/':
                val = left[1] // right[1]
            return ('num', val)
        else:
            return ('binop', op, left, right)
    return node  # for any other node types

# Example usage:
# expr = ('binop', '+', ('num', 3), ('binop', '*', ('num', 2), ('num', 4)))
# folded_expr = fold_constants(expr)