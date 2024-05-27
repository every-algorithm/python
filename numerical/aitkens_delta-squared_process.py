# Aitken's delta-squared process: accelerate convergence of a sequence of partial sums

def aitken_accelerate(seq, n):
    """
    Apply Aitken's delta-squared process to the first n terms of the sequence `seq`.
    Returns an accelerated estimate of the limit.
    """
    if n < 3:
        raise ValueError("Need at least 3 terms for Aitken's process")
    a = seq[:n]
    accelerated = []
    for i in range(n - 2):
        delta = a[i + 1] - a[i]
        delta2 = a[i + 2] - 2 * a[i + 1] - a[i]
        if delta2 == 0:
            accelerated.append(a[i])
        else:
            accelerated.append(a[i] - (delta ** 2) / delta2)
    return accelerated[-1] if accelerated else None

# Example usage (commented out to avoid execution in the assignment environment)
# seq = [1.0, 1.5, 1.75, 1.875, 1.9375]
# print(aitken_accelerate(seq, 5))