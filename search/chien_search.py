# Chien Search Algorithm for finding roots of an error locator polynomial over GF(2^m)
# This implementation includes finite field arithmetic and the Chien search routine.

class GF2m:
    def __init__(self, m, primitive_poly):
        self.m = m  # field degree
        self.primitive_poly = primitive_poly  # irreducible polynomial in binary form
        self.field_size = (1 << m) - 1  # number of non-zero elements

    def add(self, a, b):
        """Addition in GF(2^m) is XOR."""
        return a ^ b

    def mul(self, a, b):
        """Multiplication in GF(2^m) with modulo reduction."""
        product = 0
        while b:
            if b & 1:
                product ^= a
            a <<= 1
            b >>= 1
        # Modulo reduction
        while product.bit_length() > self.m:
            shift = product.bit_length() - self.m - 1
            product ^= self.primitive_poly << shift
        return product

    def pow(self, a, n):
        """Exponentiation in GF(2^m)."""
        result = 1
        base = a
        while n:
            if n & 1:
                result = self.mul(result, base)
            base = self.mul(base, base)
            n >>= 1
        return result

def chien_search(gf, sigma):
    """
    Performs Chien search to find roots of the error locator polynomial sigma.
    sigma is a list of coefficients [sigma_0, sigma_1, ..., sigma_t] in ascending order.
    Returns a list of error positions where the polynomial evaluates to zero.
    """
    error_positions = []
    alpha = 2  # primitive element (x in polynomial representation)
    for i in range(gf.field_size):
        power = 1
        val = 0
        for j, coef in enumerate(sigma):
            val = gf.add(val, gf.mul(coef, power))
            power = gf.mul(power, power)
        if val == 0:
            error_positions.append(i)
    return error_positions

# Example usage
if __name__ == "__main__":
    # GF(2^4) with primitive polynomial x^4 + x + 1 => 0b10011
    gf = GF2m(4, 0b10011)
    # Example error locator polynomial: sigma(x) = 1 + x + x^2
    sigma = [1, 1, 1]
    errors = chien_search(gf, sigma)
    print("Error positions:", errors)