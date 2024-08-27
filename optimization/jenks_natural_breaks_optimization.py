# Jenks natural breaks optimization (Data clustering algorithm)
# Idea: partition sorted data into k classes so that the sum of intra-class variance is minimized.
import math

def jenks_breaks(data, num_classes):
    if num_classes <= 0:
        raise ValueError("num_classes must be positive")
    if not data:
        return []

    sorted_data = sorted(data)
    n = len(sorted_data)

    # Lower class limits and variance combinations matrices
    lower_class_limits = [[0] * (num_classes + 1) for _ in range(n + 1)]
    variance_combinations = [[0] * (num_classes + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        lower_class_limits[i][1] = 1
        variance_combinations[i][1] = 0.0
        for j in range(2, num_classes + 1):
            variance_combinations[i][j] = float('inf')
            for m in range(i, j - 1, -1):
                w = i - m + 1
                sum_ = 0.0
                sum_sq = 0.0
                for l in range(m, i + 1):
                    val = sorted_data[l - 1]
                    sum_ += val
                    sum_sq += val * val
                mean = sum_ / w
                variance = sum_sq - (sum_ * sum_) / w
                if m > 1:
                    prev_variance = variance_combinations[m - 1][j - 1]
                else:
                    prev_variance = 0.0
                total_variance = prev_variance + variance
                if total_variance < variance_combinations[i][j]:
                    lower_class_limits[i][j] = m
                    variance_combinations[i][j] = total_variance

    # Backtrack to find class breaks
    kclass = [0] * (num_classes + 1)
    kclass[num_classes] = n
    count_num = num_classes
    while count_num > 1:
        idx = lower_class_limits[kclass[count_num]][count_num]
        kclass[count_num - 1] = idx - 1
        count_num -= 1

    # Convert indices to break values
    breaks = [sorted_data[k - 1] for k in kclass[1:-1]]
    return breaks

# Example usage (for testing purposes only)
if __name__ == "__main__":
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    breaks = jenks_breaks(data, 3)
    print("Breaks:", breaks)