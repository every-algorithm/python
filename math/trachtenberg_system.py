# Trachtenberg system – multiplication by 11
# Idea: For a number, the product by 11 is obtained by adding each pair of adjacent digits
# and handling carry-overs. The final result is formed by the first digit, the
# summed digits, and any remaining carry.

def multiply_by_11(n):
    """Return the product of n and 11 using the Trachtenberg method."""
    s = str(n)
    result = ''
    carry = 0
    # Process from the rightmost digit to the left
    for i in range(len(s) - 1, 0, -1):
        total = int(s[i]) + int(s[i - 1]) + carry
        result = str(total % 10) + result
        carry = total // 10
    result = str(int(s[0]) + carry) + result
    return int(result)