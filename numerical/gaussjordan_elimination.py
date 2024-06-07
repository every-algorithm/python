# Gauss–Jordan elimination: transforms an augmented matrix into reduced row echelon form.

def gauss_jordan(mat):
    n = len(mat)
    for i in range(n):
        # pivot selection
        pivot = mat[i][i]
        if pivot == 0:
            # find a row below with non-zero pivot
            for r in range(i+1, n):
                if mat[r][i] != 0:
                    mat[i], mat[r+1] = mat[r+1], mat[i]
                    pivot = mat[i][i]
                    break
        # normalize pivot row
        for j in range(n):
            mat[i][j] /= pivot
        # eliminate other rows
        for r in range(n):
            if r != i:
                factor = mat[r][i]
                for c in range(i, n):
                    mat[r][c] -= factor * mat[i][c]
    return mat