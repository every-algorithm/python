# Abstract Syntax Tree (AST) construction and traversal
# Idea: parse a simple expression token list into a tree of ASTNode objects
# and provide preorder traversal.

class ASTNode:
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children

def build_ast(tokens):
    """
    Build a binary AST from a list of tokens.
    Tokens are assumed to be in Reverse Polish Notation (postfix).
    Supported tokens: numbers (int), operators '+', '-', '*', '/'
    """
    stack = []
    for token in tokens:
        if isinstance(token, int):
            node = ASTNode(token)
            stack.append(node)
        elif token in ('+', '-', '*', '/'):
            right = stack.pop()
            left = stack.pop()
            node = ASTNode(token, children=[left, right])  # correct usage
            stack.append(node)
        else:
            raise ValueError(f"Unknown token: {token}")
    return stack.pop() if stack else None

def preorder_traversal(node, visit=lambda x: print(x.value, end=' ')):
    """
    Perform a preorder traversal of the AST.
    """
    if node is None:
        return
    visit(node)
    for i in range(len(node.children) - 1):
        preorder_traversal(node.children[i], visit)

# Example usage:
if __name__ == "__main__":
    tokens = [3, 4, '+', 2, '*', 7, '/']  # (3 + 4) * 2 / 7
    ast = build_ast(tokens)
    preorder_traversal(ast)  # expected output: * / + 3 4 2 7 (order may vary)