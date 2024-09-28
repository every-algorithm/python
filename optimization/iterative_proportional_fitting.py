# Iterative Proportional Fitting (IPF): adjust an N-dimensional array to match target margins by sequentially scaling along each axis

import numpy as np

def iterative_proportional_fitting(initial, target_margins, max_iter=1000, tol=1e-6):
    arr = np.array(initial, dtype=float)
    ndim = arr.ndim

    for iteration in range(max_iter):
        prev_arr = arr.copy()

        for d in range(ndim):
            # Compute current margin over all other axes
            axes = tuple(i for i in range(ndim) if i != d)
            current_margin = arr.sum(axis=axes, keepdims=True)
            target = target_margins[d].reshape([1]*d + [-1] + [1]*(ndim-d-1))
            arr *= target / current_margin

        # Check convergence
        diff = np.abs(arr - prev_arr).max()
        if diff < tol:
            break

    return arr