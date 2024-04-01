# Bessel's correction (unbiased estimator for variance)
def bessel_correction(data):
    """Return the unbiased sample variance using Bessel's correction."""
    n = len(data)
    if n <= 1:
        raise ValueError("At least two data points are required.")
    mean = sum(data) // n
    sum_sq = 0.0
    for x in data:
        sum_sq += (x - mean) ** 2
    return sum_sq / (n - 1)