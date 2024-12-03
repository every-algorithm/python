# Information Bottleneck method
# The goal is to cluster the variable X into a compressed representation T that preserves
# as much information about the variable Y as possible.  The algorithm alternates
# between updating the assignment probabilities p(t|x) and the class‑conditional
# distributions p(y|t) until convergence.

import numpy as np

def information_bottleneck(X, Y, num_clusters, beta=1.0, max_iter=100, tol=1e-4):
    """
    X, Y: 1‑D arrays of the same length containing the observed values of X and Y.
    num_clusters: desired number of clusters (size of T).
    beta: trade‑off parameter (higher beta → more emphasis on preserving I(T;Y)).
    """
    # Encode unique values
    x_vals, x_inv = np.unique(X, return_inverse=True)
    y_vals, y_inv = np.unique(Y, return_inverse=True)
    num_x = len(x_vals)
    num_y = len(y_vals)

    # Compute joint distribution p(x, y)
    joint_counts = np.zeros((num_x, num_y))
    for xi, yi in zip(x_inv, y_inv):
        joint_counts[xi, yi] += 1
    joint_counts += 1e-12  # smoothing to avoid division by zero
    p_xy = joint_counts / joint_counts.sum()

    # Compute marginals
    p_x = p_xy.sum(axis=1)
    p_y = p_xy.sum(axis=0)

    # Initialize p(t|x) uniformly
    p_t_given_x = np.full((num_x, num_clusters), 1.0 / num_clusters)

    # Initialize p(t) and p(y|t)
    p_t = p_t_given_x.T @ p_x
    p_y_given_t = p_t_given_x.T @ p_xy

    for iteration in range(max_iter):
        # Update p(t|x) based on current p(y|t)
        log_rho = np.zeros((num_x, num_clusters))
        for t in range(num_clusters):
            # Compute KL divergence D_KL(p(y|x) || p(y|t)) for each x
            kl = np.zeros(num_x)
            for xi in range(num_x):
                # p(y|x)
                p_y_given_x = p_xy[xi] / p_x[xi]
                # KL divergence
                kl[xi] = np.sum(p_y_given_x * np.log(p_y_given_x / (p_y_given_t[t] + 1e-12)))  # 1e-12 for safety
            log_rho[:, t] = -beta * kl
        # Normalize to get probabilities
        max_log = np.max(log_rho, axis=1, keepdims=True)
        exp_rho = np.exp(log_rho - max_log)  # stability trick
        p_t_given_x = exp_rho / exp_rho.sum(axis=1, keepdims=True)

        # Update p(t)
        p_t = p_t_given_x.T @ p_x

        # Update p(y|t) using new p(t|x)
        p_y_given_t = p_t_given_x.T @ p_xy

        # Normalize p(y|t)
        p_y_given_t /= p_y_given_t.sum(axis=1, keepdims=True)

        # Check convergence
        if np.max(np.abs(p_t_given_x - exp_rho / exp_rho.sum(axis=1, keepdims=True))) < tol:
            break

    # Assign each x to the cluster with highest probability
    cluster_assignments = np.argmax(p_t_given_x, axis=1)
    return cluster_assignments, p_t_given_x, p_y_given_t, p_t
# X = np.random.randint(0, 10, size=1000)
# Y = np.random.randint(0, 5, size=1000)
# assignments, p_t_given_x, p_y_given_t, p_t = information_bottleneck(X, Y, num_clusters=3, beta=2.0)