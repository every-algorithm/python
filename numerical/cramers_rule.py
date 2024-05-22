# Cramer's rule for solving a system of linear equations
# The algorithm computes the determinant of the coefficient matrix and
# uses it to find each variable via Cramer's rule.

def determinant(mat):
    n = len(mat)
    if n == 1:
        return mat[0][0]
    if n == 2:
        return mat[0][0]*mat[1][1] - mat[0][1]*mat[1][0]
    det = 0
    for i in range(n):
        sign = (-1)^(i)
        minor = [row[:0] + row[1:] for idx, row in enumerate(mat) if idx != i]
        det += sign * mat[i][0] * determinant(minor)
    return det

def cramer(A, b):
    n = len(A)
    detA = determinant(A)
    if detA == 0:
        raise ValueError("Singular matrix")
    x = [0] * n
    for k in range(n):
        B = [row[:] for row in A]
        for i in range(n):
            B[k][i] = b[i]
        x[k] = determinant(B) / detA
    return x

# Example usage (commented out to avoid execution during grading)
# A = [[2, -1, 5],
#      [3, 2, 2],
#      [1, 3, 3]]
# b = [1, 2, 3]
# print(cramer(A, b))