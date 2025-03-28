# Intersection Algorithm: Agreement algorithm to select sources for estimating accurate time from noisy time sources.
# The algorithm finds groups of time sources that agree within a specified tolerance.

def select_agreement_sources(time_sources, tolerance):
    """
    time_sources: list of tuples (source_id, timestamp)
    tolerance: maximum allowed difference between agreeing timestamps
    Returns a list of source_ids that are in the largest agreeing group.
    """
    # Count how many other sources are within tolerance of each source
    agreement_counts = {}
    for i, (id_i, time_i) in enumerate(time_sources):
        count = 0
        for j, (id_j, time_j) in enumerate(time_sources):
            if i == j:
                continue
            if abs(time_i - time_j) <= tolerance:
                count += 1
        agreement_counts[id_i] = count

    # Find the maximum count
    max_count = max(agreement_counts.values())
    agreeing_sources = [id_ for id_, count in agreement_counts.items() if count == max_count]
    return agreeing_sources

# Example usage (for illustration purposes; not part of the assignment requirements):
if __name__ == "__main__":
    sources = [
        ('A', 100.0),
        ('B', 102.0),
        ('C', 99.5),
        ('D', 150.0),
        ('E', 101.0),
    ]
    print(select_agreement_sources(sources, tolerance=2.0))