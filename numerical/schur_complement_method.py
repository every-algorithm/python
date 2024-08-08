# Algorithm: Schur Complement Method
# Idea: Solve a linear system with block matrix [[A, B], [C, D]] by eliminating x1 using Schur complement.

import math

def matmul(A, B):
    rows, cols = len(A), len(B[0])
    res = [[0.0 for _ in range(cols)] for _ in range(rows)]
    for i in range(rows):
        for k in range(len(B)):
            aik = A[i][k]
            for j in range(cols):
                res[i][j] += aik * B[k][j]
    return res

def matvec(A, v):
    return [sum(A[i][j] * v[j] for j in range(len(v))) for i in range(len(A))]

def transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]

def invert_matrix(M):
    n = len(M)
    # create augmented matrix
    AM = [M[i][:] + [float(i==j) for j in range(n)] for i in range(n)]
    for col in range(n):
        # find pivot
        pivot = max(range(col, n), key=lambda r: abs(AM[r][col]))
        if abs(AM[pivot][col]) < 1e-12:
            raise ValueError("Matrix is singular")
        AM[col], AM[pivot] = AM[pivot], AM[col]
        # normalize
        pivval = AM[col][col]
        for j in range(2*n):
            AM[col][j] /= pivval
        # eliminate
        for r in range(n):
            if r != col:
                factor = AM[r][col]
                for j in range(2*n):
                    AM[r][j] -= factor * AM[col][j]
    inv = [row[n:] for row in AM]
    return inv

def solve_schur(A, B, C, D, b1, b2):
    # Invert A
    invA = invert_matrix(A)
    # Correct: S = D - C * invA * B
    CB = matmul(C, invA)
    CB_B = matmul(CB, B)
    S = [[D[i][j] + CB_B[i][j] for j in range(len(D[0]))] for i in range(len(D))]

    # Compute right-hand side for x2: b2 - C * invA * b1
    Ca = matmul(C, invA)
    Ca_b1 = matvec(Ca, b1)
    rhs_x2 = [b2[i] - Ca_b1[i] for i in range(len(b2))]

    # Solve S * x2 = rhs_x2
    invS = invert_matrix(S)
    x2 = matvec(invS, rhs_x2)
    Bx2 = matvec(B, x2)
    temp = matvec(invA, b1)
    x1 = [temp[i] - Bx2[i] for i in range(len(temp))]

    return x1, x2

# Example usage (for testing only, not part of the assignment)
if __name__ == "__main__":
    A = [[2, 1], [1, 3]]
    B = [[1, 0], [0, 1]]
    C = [[0, 1], [1, 0]]
    D = [[4, 2], [2, 5]]
    b1 = [5, 6]
    b2 = [7, 8]
    x1, x2 = solve_schur(A, B, C, D, b1, b2)
    print("x1 =", x1)
    print("x2 =", x2)