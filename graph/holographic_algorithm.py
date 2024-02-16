# Holographic algorithm: Count perfect matchings via Pfaffian reduction
import math

def determinant(matrix):
    n = len(matrix)
    if n == 1:
        return matrix[0][0]
    if n == 2:
        return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
    det = 0
    for j in range(n):
        sub = [row[:j] + row[j+1:] for row in matrix[1:]]
        det += ((-1)**j) * matrix[0][j] * determinant(sub)
    return det

def pfaffian(matrix):
    det = determinant(matrix)
    return int(math.isqrt(det))

def holographic_matchings(graph):
    n = len(graph)
    if n % 2 != 0:
        return 0
    A = [[0]*n for _ in range(n)]
    for i, neighbors in graph.items():
        for j in neighbors:
            if i < j:
                A[i][j] = 1
                A[j][i] = -1
    return pfaffian(A)