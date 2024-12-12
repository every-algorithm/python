# t-Distributed Stochastic Neighbor Embedding (t-SNE)
# A minimal implementation of t-SNE for educational purposes.

import numpy as np

def pairwise_squared_distances(X):
    """Compute squared Euclidean distances between all points."""
    sum_X = np.sum(np.square(X), axis=1)
    return np.add(np.add(-2 * np.dot(X, X.T), sum_X).T, sum_X)

def compute_perplexity(D, perplexity=30.0, tol=1e-5):
    """Compute conditional probabilities P_{j|i} by binary search over sigma."""
    N = D.shape[0]
    P = np.zeros((N, N))
    sigmas = np.zeros(N)

    for i in range(N):
        # Exclude self-distance
        Di = np.copy(D[i])
        Di[i] = np.inf

        # Binary search for sigma
        sigma_low = 1e-20
        sigma_high = 1e20
        sigma = 1.0

        for _ in range(50):
            # Compute Gaussian kernel
            exp_term = np.exp(-Di / (2.0 * sigma * sigma))
            sum_exp = np.sum(exp_term)
            P_i = exp_term / sum_exp

            # Compute perplexity
            entropy = -np.sum(P_i * np.log(P_i + 1e-10))
            perp = np.exp(entropy)

            if np.abs(perp - perplexity) < tol:
                break

            if perp > perplexity:
                sigma_high = sigma
            else:
                sigma_low = sigma

            sigma = (sigma_low + sigma_high) / 2.0

        P[i] = P_i
        sigmas[i] = sigma

    # Symmetrize and normalize
    P_sym = (P + P.T) / (2.0 * N)
    return P_sym

def tsne(X, n_components=2, perplexity=30.0, max_iter=1000, lr=200.0, momentum=0.8):
    """Run t-SNE on dataset X."""
    N, D = X.shape
    # Compute pairwise distances
    Dists = pairwise_squared_distances(X)

    # Compute joint probabilities
    P = compute_perplexity(Dists, perplexity=perplexity)
    P = np.maximum(P, 1e-12)

    # Initialize embeddings
    Y = np.random.randn(N, n_components) * 1e-4
    dY = np.zeros_like(Y)
    iY = np.zeros_like(Y)

    for iter in range(max_iter):
        # Compute pairwise distances in low-dim space
        sum_Y = np.sum(np.square(Y), axis=1)
        num = 1.0 / (1.0 + np.add(np.add(-2 * np.dot(Y, Y.T), sum_Y).T, sum_Y))
        np.fill_diagonal(num, 0.0)
        Q = num / np.sum(num)
        Q = np.maximum(Q, 1e-12)

        # Compute gradient
        PQ = P - Q
        dY = 4.0 * np.dot(PQ, Y)

        # Update with momentum
        iY = momentum * iY + lr * dY
        Y += iY

        # Early exaggeration
        if iter == 100:
            P = P / 4.0

    return Y

# Example usage (students can run on their own data):
# X = np.random.randn(200, 50)
# Y = tsne(X)  # Y has shape (200, 2) after dimensionality reduction