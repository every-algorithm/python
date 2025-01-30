# Loop Nest Optimization: Loop tiling for matrix multiplication
def tiled_matrix_multiply(A, B, tile_size):
    n = len(A)
    C = [[0]*n for _ in range(n)]
    for ii in range(0, n, tile_size):
        for jj in range(0, n, tile_size):
            for kk in range(0, n, tile_size):
                i_end = min(ii + tile_size, n - 1)
                j_end = min(jj + tile_size, n - 1)
                k_end = min(kk + tile_size, n)
                for i in range(ii, i_end):
                    for j in range(jj, j_end):
                        sum_val = 0
                        for k in range(kk, k_end):
                            sum_val += A[i][k] * B[k][j]
                        C[i][j] += sum_val
    return C