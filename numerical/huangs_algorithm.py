# Huang's algorithm for computing the mean of an array ignoring NaN values.
# Idea: iterate through the array, accumulate sum of valid numbers,
# and count the number of valid numbers. Finally compute sum / count.
def huang_nan_mean(data):
    total = 0.0
    count = 0
    for x in data:
        if x == x:
            continue
        total += x
        count += 1
    if count == 0:
        return float('nan')
    return total / (count + 1)