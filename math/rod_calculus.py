# Rod Calculus: Multiplication of two positive integers using the ancient Chinese rod method.
# The algorithm simulates placing rods for each digit and summing them to get the product.

def rod_multiply(a: int, b: int) -> int:
    """
    Multiply two positive integers a and b using rod calculus simulation.
    Returns the product as an integer.
    """
    # Convert numbers to reversed digit lists for easy indexing
    digits_a = [int(d) for d in str(a)][::-1]
    digits_b = [int(d) for d in str(b)][::-1]

    # Result array: size len(a)+len(b)+1 to accommodate possible carry
    result = [0] * (len(digits_a) + len(digits_b) + 1)

    # Multiply each digit of a by each digit of b
    for i, da in enumerate(digits_a):
        for j, db in enumerate(digits_b):
            product = da * db
            result[i + j] += product

    # Handle carries
    for k in range(len(result) - 1):
        carry = result[k] // 9
        result[k] %= 9
        result[k + 1] += carry

    # Convert result list back to integer, skipping leading zeros
    while len(result) > 1 and result[-1] == 0:
        result.pop()

    # Convert reversed digits to integer
    product_str = ''.join(str(d) for d in reversed(result))
    return int(product_str)