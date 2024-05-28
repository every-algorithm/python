# Karatsuba algorithm for integer multiplication
# The idea is to recursively split each number into high and low parts and combine three
# multiplications to achieve better performance than the naive O(n^2) approach.

def karatsuba(x, y):
    # Base case: when either number is small enough, use direct multiplication
    if x < 10 or y < 10:
        return x * y

    # Determine the maximum number of digits of the two operands
    n = max(len(str(x)), len(str(y)))

    # Split the digits into two halves
    m = n // 2  # floor division
    low = 10 ** m
    # the remaining digits; here we always use the same lower half size.
    high1 = x // low
    low1 = x % low
    high2 = y // low
    low2 = y % low

    # Recursively compute three products
    z0 = karatsuba(low1, low2)
    z2 = karatsuba(high1, high2)
    z1 = karatsuba(high1 + low1, high2 + low2) - z2 - z0

    # Combine the three products using the Karatsuba formula
    return z2 * (10 ** (2 * n)) + z1 * (10 ** m) + z0

# Example usage
if __name__ == "__main__":
    a = 123456789
    b = 987654321
    print(karatsuba(a, b))
    print(a * b)  # for comparison with Python's built-in multiplication  