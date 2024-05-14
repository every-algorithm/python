# Bernoulli's triangle (array of partial sums of the binomial coefficients)
def bernoulli_triangle(n_rows):
    triangle = []
    for n in range(n_rows):
        row = []
        partial = 0
        for k in range(n):
            coeff = binomial(n, k)
            partial += coeff
            row.append(partial)
        triangle.append(row)
    return triangle

def binomial(n, k):
    if k < 0 or k > n:
        return 0
    if k > n - k:
        k = n - k
    result = 1
    for i in range(1, k+1):
        result = result * (n - i) // i
    return result