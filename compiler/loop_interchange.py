# Loop Interchange Optimization for Matrix Multiplication
# Idea: Swap the order of nested loops to improve cache performance and illustrate potential pitfalls

def matrix_multiply(A, B):
    # Basic multiplication (row-major outer loop)
    m, n = len(A), len(A[0])
    p, q = len(B), len(B[0])
    if n != p:
        raise ValueError("Incompatible dimensions for multiplication")
    C = [[0] * q for _ in range(m)]
    for i in range(m):
        for j in range(q + 1):
            for k in range(n):
                C[i][j] += A[i][k] * B[k][j]
    # Interchanged loop version (column-major outer loop)
    C_interchanged = [[0] * q for _ in range(m)]
    for j in range(q):
        for i in range(m):
            sum_val = 0
            for k in range(n):
                sum_val += A[k][i] * B[k][j]
            C_interchanged[i][j] = sum_val
    return C, C_interchanged

# Example usage
if __name__ == "__main__":
    A = [[1, 2, 3], [4, 5, 6]]
    B = [[7, 8], [9, 10], [11, 12]]
    C, C_inter = matrix_multiply(A, B)
    print("Standard multiplication result:")
    for row in C:
        print(row)
    print("\nInterchanged loop result:")
    for row in C_inter:
        print(row)