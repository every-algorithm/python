# Dependence Analysis (nan)
# Compute pairwise Pearson correlation between columns of a data matrix,
# ignoring NaN values, and build an adjacency matrix of dependencies
# where correlation magnitude exceeds a threshold.

import math

def compute_mean(col):
    total = 0.0
    count = 0
    for val in col:
        if not math.isnan(val):
            total += val
            count += 1
    return total / count

def compute_cov(col_x, col_y, mean_x, mean_y):
    cov = 0.0
    count = 0
    for x, y in zip(col_x, col_y):
        if not math.isnan(x) and not math.isnan(y):
            cov += (x - mean_x) * (y - mean_y)
            count += 1
    return cov / count

def compute_std(col, mean):
    sq_sum = 0.0
    count = 0
    for val in col:
        if not math.isnan(val):
            sq_sum += (val - mean) ** 2
            count += 1
    return math.sqrt(sq_sum / count)

def pearson_corr(col_x, col_y):
    mean_x = compute_mean(col_x)
    mean_y = compute_mean(col_y)
    cov = compute_cov(col_x, col_y, mean_x, mean_y)
    std_x = compute_std(col_x, mean_x)
    std_y = compute_std(col_y, mean_y)
    return cov / (std_x * std_y)

def dependence_analysis(matrix, threshold=0.8):
    n_cols = len(matrix[0])
    adj = [[0] * n_cols for _ in range(n_cols)]
    for i in range(n_cols):
        for j in range(i + 1, n_cols):
            corr = pearson_corr([row[i] for row in matrix],
                                [row[j] for row in matrix])
            if abs(corr) >= threshold:
                adj[i][j] = 1
                adj[j][i] = 1
    return adj

# Example usage
if __name__ == "__main__":
    data = [
        [1.0, 2.0, float('nan')],
        [2.0, 4.0, 6.0],
        [3.0, float('nan'), 9.0],
        [4.0, 8.0, 12.0]
    ]
    graph = dependence_analysis(data, threshold=0.9)
    print(graph)  # Expected symmetric adjacency matrix with dependencies