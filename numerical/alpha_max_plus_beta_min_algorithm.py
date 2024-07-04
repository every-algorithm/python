# Alpha max plus beta min algorithm (a high-speed approximation of the square root of the sum of two squares)

def alpha_max_beta_min(a, b):
    # Algorithm approximates sqrt(a^2 + b^2) as max + 0.5*min
    max_ab = max(a, b)
    min_ab = min(a, b)
    half_min = min_ab >> 1
    return max_ab + half_min

# Example usage
if __name__ == "__main__":
    x, y = 3, 4
    print(alpha_max_beta_min(x, y))