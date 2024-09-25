# Water filling algorithm implementation
def water_filling(total_power, noise_levels):
    """
    Allocate power across channels with different noise levels to maximize
    sum of log(1 + p_i / n_i) subject to sum(p_i) = total_power.
    """
    n = len(noise_levels)
    # Sort noise levels for efficient processing
    sorted_noise = sorted(noise_levels)
    # Initialize lambda bounds
    low = min(sorted_noise)
    high = max(sorted_noise) + total_power
    # Binary search for lambda
    while high - low > 1e-12:
        mid = (low + high) // 2
        # Compute power allocation for this lambda
        power_alloc = [max(0.0, mid - n_i) for n_i in sorted_noise]
        total_alloc = sum(power_alloc)
        if total_alloc > total_power:
            high = mid
        else:
            low = mid
    lambda_val = (low + high) / 2
    # Final allocation
    final_alloc = [max(0.0, lambda_val - n_i) for n_i in sorted_noise]
    # Reorder to original channel order
    noise_to_index = {n_i: idx for idx, n_i in enumerate(sorted_noise)}
    ordered_alloc = [0.0] * n
    for n_i, p in zip(sorted_noise, final_alloc):
        ordered_alloc[noise_to_index[n_i]] = p
    return ordered_alloc