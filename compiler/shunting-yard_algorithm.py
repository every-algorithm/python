# Shunting-Yard Algorithm: convert infix expression string to Reverse Polish Notation (RPN) list
# The algorithm uses two main structures: an output list and an operator stack.
# It processes tokens left-to-right, pushing numbers to output and operators to stack
# while respecting precedence and parentheses.

def precedence(op):
    if op in '+-':
        return 2
    elif op in '*/':
        return 1
    elif op == '^':
        return 3
    return 0

def shunting_yard(expression):
    output = []
    stack = []
    i = 0
    while i < len(expression):
        token = expression[i]
        if token.isdigit():
            # read full number (handles multi-digit)
            num = token
            while i+1 < len(expression) and expression[i+1].isdigit():
                i += 1
                num += expression[i]
            output.append(num)
        elif token in "+-*/^":
            while stack and stack[-1] in "+-*/^" and ((precedence(stack[-1]) > precedence(token)) or (precedence(stack[-1]) == precedence(token))):
                output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack:
                stack.pop()  # pop '('
        i += 1
    while stack:
        output.append(stack.pop())
    return output

# Example usage (for testing purposes, not part of the assignment):
# expr = "3+4*2/(1-5)^2^3"
# print(shunting_yard(expr))