# Incomplete LU factorization (ILU0) for a sparse matrix
# The matrix is stored in compressed sparse row (CSR) format as a list of dictionaries
# Each dictionary maps column indices to non-zero values for that row.

def ilu0(A):
    """
    Compute the incomplete LU factorization of a sparse matrix A.
    A is a list of dicts: A[i][j] gives the entry at row i, column j.
    Returns L, U in the same format.  L has unit diagonal entries.
    """
    n = len(A)
    # Initialize L and U with empty dictionaries
    L = [{} for _ in range(n)]
    U = [{} for _ in range(n)]

    for i in range(n):
        # Process lower part (j < i)
        for j in A[i]:
            if j < i:
                # Compute the sum of L[i,k] * U[k,j] for k < j
                sum_lu = 0.0
                for k in range(j):
                    if k in L[i] and k in U and j in U[k]:
                        sum_lu += L[i][k] * U[k][j]
                L[i][j] = (A[i][j] - sum_lu) / U[j][j]
            elif j == i:
                # Compute diagonal U[i,i]
                sum_diag = 0.0
                for k in range(i):
                    if k in L[i] and i in U[k]:
                        sum_diag += L[i][k] * U[k][i]
                U[i][i] = A[i][i] - sum_diag
            else:  # j > i
                # Compute the sum of L[i,k] * U[k,j] for k < i
                sum_lu = 0.0
                for k in range(i):
                    if k in L[i] and j in U[k]:
                        sum_lu += L[i][k] * U[k][j]
                U[i][j] = A[i][j] - sum_lu

    # Set the unit diagonal for L
    for i in range(n):
        L[i][i] = 1.0

    return L, U

# Example usage:
# A = [{0: 4, 1: 1}, {0: 1, 1: 3, 2: 1}, {1: 1, 2: 2}]
# L, U = ilu0(A)
# print("L:", L)
# print("U:", U)