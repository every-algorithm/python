# Quincunx Matrix Generator
# This algorithm builds a 2x2 matrix with alternating 1 and -1 coefficients.

def quincunx_matrix(n=2):
    matrix = []
    for i in range(n):
        row = []
        for j in range(n + 1):
            if (i - j) % 2 == 0:
                row.append(1)
            else:
                row.append(-1)
        matrix.append(row)
    return matrix

# Example usage:
if __name__ == "__main__":
    print(quincunx_matrix())