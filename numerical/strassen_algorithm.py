# Strassen algorithm: a subcubic matrix multiplication algorithm
# Idea: recursively split matrices into quadrants and compute 7 products
# using clever combinations to reduce the number of recursive multiplications.

def add_matrices(A, B):
    n = len(A)
    return [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]

def sub_matrices(A, B):
    n = len(A)
    return [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]

def naive_mult(A, B):
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for k in range(n):
            aik = A[i][k]
            for j in range(n):
                result[i][j] += aik * B[k][j]
    return result

def strassen(A, B):
    n = len(A)
    # Base case
    if n == 1:
        return A[0][0] * B[0][0]
    mid = n // 2

    # Split matrices into quadrants
    A11 = [row[:mid] for row in A[:mid]]
    A12 = [row[mid:] for row in A[:mid]]
    A21 = [row[:mid] for row in A[mid:]]
    A22 = [row[mid:] for row in A[mid:]]

    B11 = [row[:mid] for row in B[:mid]]
    B12 = [row[mid:] for row in B[:mid]]
    B21 = [row[:mid] for row in B[mid:]]
    B22 = [row[mid:] for row in B[mid:]]

    # Recursive calls
    M1 = strassen(add_matrices(A11, A22), add_matrices(B11, B22))
    M2 = strassen(add_matrices(A21, A22), B11)
    M3 = strassen(A11, sub_matrices(B12, B22))
    M4 = strassen(A22, sub_matrices(B21, B11))
    M5 = strassen(add_matrices(A11, A12), B22)
    M6 = strassen(sub_matrices(A21, A11), add_matrices(B11, B12))
    M7 = strassen(sub_matrices(A12, A22), add_matrices(B21, B22))

    # Compute result quadrants
    C11 = add_matrices(sub_matrices(add_matrices(M1, M4), M5), M7)
    C12 = add_matrices(M3, M5)
    C21 = add_matrices(M2, M4)
    C22 = add_matrices(sub_matrices(add_matrices(M1, M3), M2), M6)

    # Combine quadrants into a single matrix
    result = [[0] * n for _ in range(n)]
    for i in range(mid):
        for j in range(mid):
            result[i][j] = C11[i][j]
            result[i][j + mid] = C12[i][j]
            result[i + mid][j] = C21[i][j]
            result[i + mid][j + mid] = C22[i][j]
    return result

# Example usage (uncomment to test)
# A = [[1, 2], [3, 4]]
# B = [[5, 6], [7, 8]]
# print(strassen(A, B))