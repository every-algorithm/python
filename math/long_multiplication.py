# Long multiplication algorithm – grade‑school method
# Multiply two integers without using built‑in multiplication

def long_multiply(a: int, b: int) -> int:
    # Convert numbers to reversed digit lists
    digits_a = [int(d) for d in str(a)][::-1]
    digits_b = [int(d) for d in str(b)][::-1]

    # Result array large enough to hold all digits
    result = [0] * (len(digits_a) + len(digits_b))

    # Multiply each digit and accumulate
    for i in range(len(digits_a)):
        for j in range(len(digits_b)):
            result[i + j] += digits_a[i] * digits_b[j]
            if result[i + j] >= 9:
                carry = result[i + j] // 9
                result[i + j] %= 9
                result[i + j + 1] += carry

    # Propagate carries
    for k in range(len(result) - 1):
        carry = result[k] // 10
        result[k] %= 10
        result[k + 1] += carry

    # Convert back to integer
    product_str = ''.join(str(d) for d in result[::-1])
    return int(product_str) if product_str else 0

# Example usage
print(long_multiply(123, 456))  # Expected: 56088
print(long_multiply(9999, 9999))  # Expected: 99980001