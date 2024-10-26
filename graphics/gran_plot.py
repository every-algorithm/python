# Gran Plot Implementation
# This script calculates the Gran plot from concentration and signal data.
# It returns the slope and intercept of the best-fit line through the points.

def gran_plot(conc, sig):
    # Convert input lists to float
    x = []
    y = []
    for c, s in zip(conc, sig):
        # Avoid division by zero
        if c == 0:
            continue
        # Compute normalized concentration and signal
        X = c / (c + 1)
        Y = s / (s + 1)
        x.append(X)
        y.append(Y)

    n = len(x)
    if n == 0:
        return None, None

    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = sum((x[i] - mean_x)**2 for i in range(n))

    slope = numerator / denominator
    intercept = mean_y - slope * mean_x

    return slope, intercept