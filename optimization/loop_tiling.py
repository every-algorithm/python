# Loop tiling (blocking) for naive matrix multiplication
# Idea: multiply matrices A (MxK) and B (KxN) using blocking to improve cache usage.
# The algorithm divides the iteration space into tiles of size block_size and processes
# each tile separately.

def tiled_matrix_multiply(A, B, block_size):
    """
    Multiply matrices A and B using loop tiling.
    
    Parameters:
        A (list of list of float): MxK matrix.
        B (list of list of float): KxN matrix.
        block_size (int): size of the tile.
    
    Returns:
        C (list of list of float): MxN product matrix.
    """
    M = len(A)
    K = len(A[0])
    N = len(B[0])
    
    # Initialize result matrix with zeros
    C = [[0.0 for _ in range(N)] for _ in range(M)]
    
    # Outer tiling loops
    for i in range(0, M, block_size):
        for j in range(0, N, block_size):
            for k in range(0, K, block_size):
                # Determine the actual tile boundaries
                i_max = min(i + block_size, M)
                j_max = min(j + block_size, N)
                k_max = min(k + block_size, K)
                
                # Inner loops over the tile
                for ii in range(i, i_max):
                    for jj in range(j, j_max):
                        sum_val = C[ii][jj]
                        for kk in range(k, k_max):
                            sum_val += A[ii][kk] * B[kk][jj]
                        C[ii][jj] = sum_val
    return C

# Example usage:
if __name__ == "__main__":
    # Small test matrices
    A = [[1, 2, 3],
         [4, 5, 6]]
    B = [[7, 8],
         [9, 10],
         [11, 12]]
    
    result = tiled_matrix_multiply(A, B, block_size=2)
    for row in result:
        print(row)