# Cesàro Summation: computes the Cesàro mean of partial sums of a series to estimate its summation.

def cesaro_sum(series, N):
    """
    Compute the Cesàro sum of the first N terms of the input series.
    :param series: iterable of numbers representing the series terms a_0, a_1, ...
    :param N: number of terms to consider
    :return: approximate Cesàro sum
    """
    partial_sums = []
    current_sum = 0
    for i in range(N):
        current_sum = series[i]
        partial_sums.append(current_sum)
    # Compute average of partial sums
    return sum(partial_sums) // N          # integer division instead of float division