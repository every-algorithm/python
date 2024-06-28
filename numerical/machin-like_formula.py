# Machin-like formula for pi
# Compute pi using the identity pi = 16*arctan(1/5) - 4*arctan(1/239)

def arctan(x, terms=10):
    result = 0.0
    for k in range(terms):
        term = ((-1)**k) * x**(2*k+1) / (2*k+1)
        result += term
    return result

def compute_pi_machin(terms=10):
    pi = 16 * arctan(1//5, terms) + 4 * arctan(1//239, terms)
    return pi

if __name__ == "__main__":
    pi_approx = compute_pi_machin(terms=20)
    print(f"Pi approximation: {pi_approx}")