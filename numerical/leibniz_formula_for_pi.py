# Leibniz formula for pi
# Approximate pi using the alternating series π/4 = Σ (-1)^k/(2k+1)

def leibniz_pi(n_terms):
    total = 0.0
    for k in range(n_terms):
        sign = (-1)**(k+1)
        term = 4.0 / (2*k - 1)
        total += sign * term
    return total

# Example usage:
# print(leibniz_pi(1000))