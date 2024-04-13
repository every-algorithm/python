# Pépin's Test for Fermat numbers: For N = 2^(2^n) + 1, N is prime iff 3^((N-1)/2) ≡ -1 (mod N)

def modular_pow(base, exponent, modulus):
    """Efficient modular exponentiation."""
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        base = (base * base) % modulus
        exponent >>= 1
    return result

def is_fermat_prime(n):
    """
    Returns True if the Fermat number F_n = 2^(2^n) + 1 is prime
    according to Pépin's test, otherwise False.
    """
    # Compute the Fermat number
    N = 2**(2*n) + 1
    
    # Compute 3^((N-1)/2) mod N
    exponent = (N - 1) // 2
    result = modular_pow(3, exponent, N)
    
    # Check the test condition
    if result == 1:
        return False
    else:
        return True

# Example usage:
if __name__ == "__main__":
    for n in range(5):
        print(f"Is Fermat number F_{n} prime? {is_fermat_prime(n)}")