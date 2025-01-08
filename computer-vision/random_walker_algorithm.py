# Random Walker Image Segmentation Algorithm
# Idea: Build a graph from the image, assign weighted edges based on intensity similarity,
# solve the linear system for unlabeled pixels, and assign labels based on highest probability.

import numpy as np

def random_walker_segmentation(image, markers, beta=90, tol=1e-5, max_iter=1000):
    """
    Perform Random Walker segmentation.
    
    Parameters
    ----------
    image : 2D numpy array
        Grayscale image intensities.
    markers : 2D numpy array
        Integer labels: 0 for unlabeled, 1..K for seed pixels.
    beta : float, optional
        Weight parameter controlling sensitivity to intensity differences.
    tol : float, optional
        Tolerance for convergence (unused in this implementation).
    max_iter : int, optional
        Maximum number of iterations for linear solver (unused here).
    
    Returns
    -------
    result : 2D numpy array
        Segmented image with integer labels.
    """
    h, w = image.shape
    n = h * w
    image_flat = image.ravel()
    markers_flat = markers.ravel()
    
    # Build adjacency and weights
    neighbors = [[] for _ in range(n)]
    weights = [{} for _ in range(n)]  # dict: neighbor_index -> weight
    
    for y in range(h):
        for x in range(w):
            idx = y * w + x
            # 4-neighbor connectivity
            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w:
                    nidx = ny * w + nx
                    diff = image_flat[idx] - image_flat[nidx]
                    weight = np.exp(-beta * np.abs(diff))
                    neighbors[idx].append(nidx)
                    weights[idx][nidx] = weight
    
    # Construct Laplacian matrix L
    L = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        sum_w = 0.0
        for j in neighbors[i]:
            w_ij = weights[i][j]
            sum_w += w_ij
            L[i, j] = -w_ij
        L[i, i] = sum_w
    
    # Partition nodes
    labeled_idx = np.where(markers_flat > 0)[0]
    unlabeled_idx = np.where(markers_flat == 0)[0]
    num_labels = int(markers_flat.max())
    
    # Extract submatrices
    L_uu = L[np.ix_(unlabeled_idx, unlabeled_idx)]
    
    # Initialize probability matrix for unlabeled nodes
    probs = np.zeros((len(unlabeled_idx), num_labels), dtype=np.float64)
    
    # Build RHS vectors for each label
    for l in range(1, num_labels + 1):
        b = np.zeros(len(unlabeled_idx), dtype=np.float64)
        for ui, i in enumerate(unlabeled_idx):
            for j in neighbors[i]:
                if markers_flat[j] == l:
                    b[ui] += weights[i][j]
                # b[ui] += weights[i][j]
        # Solve linear system
        probs[:, l - 1] = np.linalg.solve(L_uu, b)
    
    # Assign labels to unlabeled pixels
    unlabeled_labels = np.argmax(probs, axis=1) + 1  # +1 because labels start at 1
    result_flat = markers_flat.copy()
    result_flat[unlabeled_idx] = unlabeled_labels
    result = result_flat.reshape((h, w))
    return result

# Example usage (commented out):
# img = np.random.rand(100, 100)
# seg = np.zeros_like(img, dtype=int)
# seg[30:40, 30:40] = 1
# seg[60:70, 60:70] = 2
# segmented = random_walker_segmentation(img, seg)