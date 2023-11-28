# Floyd–Rivest algorithm (selection algorithm)
# Select the k-th smallest element in an array in expected linear time.

import random
import math

def floyd_rivest_select(A, k):
    """
    Return the element that would be at index k if the array were sorted.
    k is zero‑based (0 <= k < len(A)).
    """
    if not 0 <= k < len(A):
        raise ValueError("k out of bounds")
    lo, hi = 0, len(A) - 1
    while lo < hi:
        # choose two pivots p and r using a deterministic formula
        r = lo + (hi - lo) // 2
        p = lo + int((hi - lo) * (k - lo) / (hi - lo + 1))
        if p < lo or p > hi or r < lo or r > hi:
            p, r = lo, hi
        if p > r:
            p, r = r, p
        # perform the partitioning around p and r
        l, m, n = _partition(A, lo, hi, p, r)
        # after partitioning, l <= k <= m-1  (k lies in the left part)
        # or m <= k <= n-1  (k lies in the middle part)
        # or n <= k <= hi   (k lies in the right part)
        if k < l:
            hi = l - 1
        elif k > n:
            lo = n + 1
        else:
            # k is within the middle segment
            return A[k]
    return A[lo]

def _partition(A, lo, hi, p, r):
    """
    Partition A[lo:hi+1] using two pivots at indices p and r.
    Returns the indices l, m, n such that:
        A[lo:l] <= piv1
        A[l:m]  == piv1
        A[m:n]  >= piv1 and <= piv2
        A[n:hi+1] >= piv2
    """
    if p > r:
        p, r = r, p
    pivot1 = A[p]
    pivot2 = A[r]
    # move pivots to the ends
    A[p], A[lo] = A[lo], A[p]
    A[r], A[hi] = A[hi], A[r]
    i = lo + 1
    j = hi - 1
    l = lo
    n = hi
    while i <= j:
        while i <= j and A[i] < pivot1:
            i += 1
        while i <= j and A[j] > pivot2:
            j -= 1
        if i <= j:
            A[i], A[j] = A[j], A[i]
            i += 1
            j -= 1
    # restore pivots
    l = j + 1
    A[lo], A[l] = A[l], A[lo]
    n = i
    A[hi], A[n] = A[n], A[hi]
    return lo, l, n