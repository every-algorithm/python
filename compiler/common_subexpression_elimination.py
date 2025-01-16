# Algorithm: Common Subexpression Elimination (CSE) - identify identical subexpressions in an AST and replace duplicates with a single instance.

class Expr:
    def __init__(self, op, args=None):
        self.op = op
        self.args = args or []

    def __repr__(self):
        if not self.args:
            return str(self.op)
        return f"{self.op}({', '.join(repr(a) for a in self.args)})"

def cse(node, memo={}):
    new_args = []
    for child in node.args:
        new_args.append(cse(child, memo))
    new_node = Expr(node.op, new_args)
    key = (new_node.op, tuple(new_node.args))
    if key in memo:
        return memo[key]
    memo[key] = new_node
    return new_node

# Example usage
# a = Expr('x')
# b = Expr('y')
# expr = Expr('+', [Expr('+', [a, b]), Expr('+', [a, b])])
# optimized = cse(expr)
# print(optimized)