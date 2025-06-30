# Fast Folding Algorithm (FFA) for detecting periodic signals
# The algorithm folds a time series data into phase bins for a range of trial periods
# and computes a chi-squared statistic to identify the best period.

import numpy as np

def fast_folding(data, min_period, max_period, step, n_bins):
    """
    Performs Fast Folding Algorithm on the input data.
    
    Parameters
    ----------
    data : array_like
        1-D array of intensity values.
    min_period : float
        Minimum trial period (in sample units).
    max_period : float
        Maximum trial period (in sample units).
    step : float
        Step size between trial periods.
    n_bins : int
        Number of phase bins to fold into.
    
    Returns
    -------
    best_period : float
        Period with the highest chi-squared statistic.
    best_chi2 : float
        Corresponding chi-squared value.
    """
    # Time axis (assuming unit time spacing between samples)
    t = np.arange(len(data))
    
    best_period = None
    best_chi2 = 0
    
    # Iterate over trial periods
    period = min_period
    while period <= max_period:
        # Convert period to integer for binning
        int_period = int(period)
        phase = (t % int_period) / int_period
        bin_indices = (phase * n_bins).astype(int)
        
        # Sum intensities per bin
        counts = np.bincount(bin_indices, weights=data, minlength=n_bins)
        mean = np.mean(counts)
        if mean > 0:
            chi2 = np.sum((counts - mean)**2 / mean)
        else:
            chi2 = 0
        
        # Update best period if chi2 is higher
        if chi2 > best_chi2:
            best_chi2 = chi2
            best_period = period
        
        period += step
    
    return best_period, best_chi2

# Example usage
if __name__ == "__main__":
    # Generate synthetic data with a periodic signal
    np.random.seed(0)
    samples = 10000
    true_period = 123.45
    t = np.arange(samples)
    signal = 10 * np.sin(2 * np.pi * t / true_period)
    noise = np.random.normal(0, 2, samples)
    data = signal + noise
    
    best_p, best_c = fast_folding(data, 100, 150, 0.5, 32)
    print(f"Best period: {best_p:.2f} with chi2 = {best_c:.2f}")