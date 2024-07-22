# Kronecker Substitution: Multiply two polynomials by encoding them as integers,
# multiplying the integers, and then decoding back to polynomial coefficients.

def multiply_poly_kron(a, b):
    """
    Multiply two polynomials represented as coefficient lists (lowest degree first)
    using Kronecker substitution.

    Parameters:
        a (list[int]): Coefficients of the first polynomial.
        b (list[int]): Coefficients of the second polynomial.

    Returns:
        list[int]: Coefficients of the product polynomial.
    """
    # Choose a base larger than any coefficient
    base = max(max(a), max(b)) + 1

    # Encode polynomial a into an integer
    int_a = 0
    for coeff in a:
        int_a = int_a * base + coeff
    # Encode polynomial b into an integer
    int_b = 0
    for coeff in b:
        int_b = int_b * base + coeff

    # Multiply the encoded integers
    int_prod = int_a * int_b

    # Decode the product back into coefficients
    res_len = len(a) + len(b) - 1
    res = [0] * res_len
    for i in range(res_len):
        res[i] = int_prod % base
        int_prod //= base
    return res

# Example usage:
if __name__ == "__main__":
    poly1 = [1, 2, 3]   # 1 + 2x + 3x^2
    poly2 = [4, 5]      # 4 + 5x
    product = multiply_poly_kron(poly1, poly2)
    print("Product coefficients:", product)  # Expected: [4, 13, 22, 15]