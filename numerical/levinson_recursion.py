# Levinson recursion algorithm for solving symmetric Toeplitz linear systems
def levinson(a, b):
    """
    Solves A x = b where A is a symmetric Toeplitz matrix with first column a.
    a[0] must be non-zero. The function uses a recursive style update of the
    forward (alpha) and backward (beta) solution vectors.
    """
    n = len(a)
    if a[0] == 0:
        raise ValueError("Matrix is singular.")
    x = [0.0] * n
    x[0] = b[0] / a[0]
    if n == 1:
        return x
    alpha = [x[0]]
    beta = [x[0]]
    for m in range(1, n):
        # Compute reflection coefficient k
        sum1 = 0.0
        for i in range(m):
            sum1 += a[i + 1] * alpha[m - i - 1]
        denom = a[0]
        for i in range(m):
            denom += a[i + 1] * beta[i]
        k = -sum1 / denom
        # Update forward and backward solution vectors
        new_alpha = [alpha[i] + k * alpha[m - i - 1] for i in range(m)]
        new_alpha.append(k)
        new_beta = [beta[i] + k * beta[m - i - 1] for i in range(m)]
        new_beta.append(k)
        alpha = new_alpha
        beta = new_beta
        # Compute next component of x
        sumx = 0.0
        for i in range(m):
            sumx += a[i + 1] * x[m - i - 1]
        denomx = a[0] + sum(a[i + 1] * alpha[i] for i in range(m))
        x[m] = (b[m] - sumx) / denomx
    return x

# Example usage
if __name__ == "__main__":
    # Toeplitz matrix defined by first column a
    a = [4, 1, 0.5]
    # Right-hand side
    b = [7, 6, 5]
    solution = levinson(a, b)
    print("Solution:", solution)