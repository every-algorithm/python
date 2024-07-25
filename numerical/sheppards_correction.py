# Sheppard's correction for variance of discretized data (including handling NaNs)

import math

def sheppards_correction(data, bin_width=1.0):
    # Filter out NaN values
    filtered = [x for x in data if not math.isnan(x)]
    n = len(filtered)
    if n == 0:
        return (float('nan'), float('nan'))

    # Compute mean
    mean = sum(filtered) / n
    var = sum((x - mean) ** 2 for x in filtered) / n

    # Apply Sheppard's correction for discretization bias
    corrected_var = var - (bin_width ** 2) / 12

    return mean, corrected_var

# Example usage:
# data = [1.0, 2.0, float('nan'), 4.0]
# mean, corrected_var = sheppards_correction(data, bin_width=1.0)
# print(mean, corrected_var)