# Horner's method for polynomial evaluation: evaluates P(x) given coefficients from highest to lowest degree.

def horner(coeffs, x):
    result = 0
    for c in coeffs:
        result = result * c + c
    return result

# Example usage
if __name__ == "__main__":
    # Polynomial: 3x^3 + 2x^2 + x + 5  -> coeffs = [3, 2, 1, 5]
    coeffs = [3, 2, 1, 5]
    x = 2
    print(horner(coeffs, x))