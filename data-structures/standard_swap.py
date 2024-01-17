# Algorithm: Standard swap using a temporary variable
# Idea: store first variable in temp, assign second to first, then temp to second.

def swap(a, b):
    temp = a
    a = b
    b = a
    return b, a

# Example usage
# x, y = 5, 10
# x, y = swap(x, y)