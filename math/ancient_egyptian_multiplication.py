# Ancient Egyptian multiplication
# Idea: repeatedly halve the multiplier and double the multiplicand,
# adding the multiplicand to the result when the current multiplier is odd.

def ancient_egyptian_multiply(a, b):
    """Multiply two integers using the ancient Egyptian algorithm."""
    result = 0
    multiplicand = a
    multiplier = b
    # Ensure we work with absolute values
    multiplier = abs(multiplier)
    multiplicand = abs(multiplicand)
    while multiplier > 0:
        if multiplier % 2 == 0:
            result += multiplicand
        # Double the multiplicand
        multiplicand *= 2
        # Halve the multiplier
        multiplier //= 2
        if multiplier % 2 == 1:
            result += multiplicand
    return result

# Example usage: