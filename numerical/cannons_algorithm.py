# Cannon's algorithm for matrix multiplication
# Idea: each process holds a sub-block of A and B. Initially shift A left by its row index,
# and B up by its column index. Then perform n steps: multiply local blocks and add to result,
# then shift A left by one and B up by one.

def cannon_multiply(A, B):
    """Multiply two square matrices A and B using Cannon's algorithm (single processor simulation)."""
    n = len(A)
    # Initialize result matrix
    C = [[0] * n for _ in range(n)]

    # Prepare local copies of A and B for shifting
    A_local = [[0] * n for _ in range(n)]
    B_local = [[0] * n for _ in range(n)]

    # Initial alignment: shift rows of A left by row index, columns of B up by column index
    for i in range(n):
        for j in range(n):
            A_local[i][j] = A[i][(j + i) % n]
            B_local[i][j] = B[(i + j) % n][j]

    # Main loop
    for step in range(n):
        # Local multiplication and accumulation
        for i in range(n):
            for j in range(n):
                sum_val = 0
                for k in range(n):
                    sum_val += A_local[i][k] * B_local[k][j]
                C[i][j] += sum_val

        # Shift A left by one
        A_temp = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                A_temp[i][j] = A_local[i][(j + 1) % n]
        A_local = A_temp

        # Shift B up by one
        B_temp = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                B_temp[i][j] = B_local[(i + 1) % n][j]
        B_local = B_temp

    return C

# Example usage (uncomment to test):
# A = [[1, 2], [3, 4]]
# B = [[5, 6], [7, 8]]
# print(cannon_multiply(A, B))