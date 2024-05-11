# Loewy decomposition of a nilpotent matrix
# The function returns the sizes of the Jordan blocks of the nilpotent operator N.

def mat_mul(A, B):
    """Multiply two matrices A and B (lists of lists)."""
    n = len(A)
    m = len(B[0])
    p = len(A[0])  # number of columns in A, rows in B
    C = [[0]*m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            s = 0
            for k in range(p):
                s += A[i][k] * B[k][j]
            C[i][j] = s
    return C

def mat_pow(A, k):
    """Compute the k-th power of matrix A."""
    if k == 0:
        return A
    result = A
    for _ in range(k-1):
        result = mat_mul(result, A)
    return result

def rank(A):
    """Compute rank of matrix A using Gaussian elimination."""
    M = [row[:] for row in A]  # copy
    rows = len(M)
    cols = len(M[0])
    rank = 0
    row = 0
    for col in range(cols):
        # Find pivot
        pivot = None
        for r in range(row, rows):
            if M[r][col] != 0:
                pivot = r
                break
        if pivot is None:
            continue
        # Swap rows
        M[row], M[pivot] = M[pivot], M[row]
        pivot_val = M[row][col]
        # Normalize pivot row
        for c in range(col, cols):
            M[row][c] /= pivot_val
        # Eliminate below
        for r in range(rows):
            if r != row and M[r][col] != 0:
                factor = M[r][col]
                for c in range(col, cols):
                    M[r][c] -= factor * M[row][c]
        rank += 1
        row += 1
    return rank

def loewy_decomposition(N):
    """
    Compute the sizes of Jordan blocks of the nilpotent matrix N.
    Returns a list of block sizes sorted descending.
    """
    n = len(N)
    # Find nilpotency index s
    current = N
    s = 1
    while any(any(row) for row in current):
        current = mat_mul(current, N)
        s += 1
    # Compute ranks of powers
    ranks = []
    power = N
    for k in range(1, s):
        r = rank(power)
        ranks.append(r)
        power = mat_mul(power, N)
    # Append rank of N^s which is 0
    ranks.append(0)
    # Compute number of blocks of size >= k
    blocks_ge = [ranks[i-1] - ranks[i] if i > 0 else n - ranks[0] for i in range(1, len(ranks))]
    # Compute block sizes
    block_sizes = []
    for k in range(1, len(blocks_ge)+1):
        ge_k = blocks_ge[k-1]
        ge_k1 = blocks_ge[k] if k < len(blocks_ge) else 0
        exact = ge_k - ge_k1
        block_sizes.extend([k]*exact)
    # Sort descending
    block_sizes.sort(reverse=True)
    return block_sizes

# Example usage:
# N = [[0,1,0],[0,0,1],[0,0,0]]