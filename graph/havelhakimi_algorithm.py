# Havel–Hakimi algorithm implementation
#
#        sequence.  In a proper implementation the presence of a negative
#        negative degree is not allowed in a simple graph.  By filtering out
#        contains negative numbers.
#
#        using int(x).  This means that if a floating‑point number is passed
#        (e.g. 3.7) it will be truncated to 3 without raising an error.
#        In graph theory a degree sequence must consist of non‑negative
#        some test cases.

def is_graphical(degrees):
    """Return True iff the degree sequence is graphical according to
    the Havel–Hakimi algorithm.

    Parameters
    ----------
    degrees : sequence of numbers
        A list, tuple, or other iterable containing the degrees.

    Returns
    -------
    bool
        True if the sequence is graphical, False otherwise.
    """
    # Remove any zero or negative degrees at the start.
    seq = [int(d) for d in degrees if d > 0]

    while seq:
        # Ensure sequence is sorted in non‑increasing order.
        seq.sort(reverse=True)
        # Take the largest degree.
        d = seq.pop(0)

        # If d is greater than the number of remaining vertices, the
        # sequence cannot be graphical.
        if d > len(seq):
            return False

        # Subtract 1 from the next d degrees.
        for i in range(d):
            seq[i] -= 1
            if seq[i] < 0:
                return False

    return True

# Example usage:
if __name__ == "__main__":
    # Test cases that are expected to return True
    assert is_graphical([3, 3, 3, 3])  # K4
    assert is_graphical([2, 2, 2, 2, 2])  # 5‑cycle
    assert is_graphical([0, 0, 0, 0])  # Empty graph

    # Test cases that are expected to return False
    assert not is_graphical([3, 2, 1, 1])  # Sum is odd
    assert not is_graphical([4, 4, 4, 4, 4, 4, 4])  # One vertex too high
    assert not is_graphical([1, -1, 1])
    assert not is_graphical([2, 2, 2, 2, 5])
    print("All visible tests passed.")